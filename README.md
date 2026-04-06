# Credit Scoring Application

Django-based credit scoring app that predicts `prob_default` (probability of default) for each submitted loan application.

## Features

- Web form for creating loan applications
- Logistic Regression model stored in `model.pkl`
- SQLite storage for applications and synthetic training data
- Views for accepted/rejected/pending applications
- Batch decisioning using risk threshold + budget + expected profit

## Quick Start

### 1) Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Apply migrations

```bash
python manage.py migrate
```

### 4) Ensure model exists

If `model.pkl` is missing (or stale after schema/form changes), retrain it:

```bash
python manage.py populate_db
python manage.py train_model
```

### 5) Run server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Probability and Approval Logic

- `prob_default` means **risk of default** (lower is better)
- Model output is clamped to `[1e-9, 0.99]` in `scoring/views.py`
- Hard risk cutoff is `MAX_DEFAULT_RATE = 0.30` in `credit_scoring/settings.py`
  - `prob_default >= 0.30` -> rejected
  - below that threshold -> may be accepted if budget allows and expected profit is positive
- Batch decisioning is triggered in `process_pending_applications()` when pending applications reach 20

## Retraining After Form/Schema Changes

When you change input fields (for example, removing `loan_purpose`), retrain so inference matches training features.

### Recommended reset flow

```bash
rm -f model.pkl
rm -f db.sqlite3
python manage.py migrate
python manage.py populate_db
python manage.py train_model
```

Then restart the server and submit new applications.

## Management Commands

- `python manage.py populate_db`  
  Recreates synthetic rows in `TrainingData`.
- `python manage.py train_model`  
  Trains Logistic Regression and overwrites `model.pkl`.
- `python manage.py clean_applications`  
  Removes legacy generated application rows matching old naming pattern.
- `python manage.py update_probabilities`  
  Recomputes stored probabilities for existing applications. Use with caution: keep this command aligned with `scoring/views.py` feature engineering and thresholds.

## Notes for Developers

- Keep feature order in `scoring/views.py::predict_default()` and `scoring/management/commands/train_model.py` identical.
- If you add/remove fields in `Application` or `TrainingData`, update:
  - form template (`scoring/templates/form.html`)
  - request parsing in `scoring/views.py`
  - training preprocessing in `train_model.py`
  - migrations

