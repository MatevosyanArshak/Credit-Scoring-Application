# Credit Scoring Application

This is a Django-based web application for credit scoring. It uses a pre-trained Logistic Regression model to predict the probability of default for a loan application.

## Features

- **Web-based Interface**: A user-friendly web form for submitting loan applications.
- **Pre-trained Machine Learning Model**: Comes with a `model.pkl` file, so no training is needed for standard use.
- **Database Integration**: Stores all applications in a database.
- **Application Management**: Allows for viewing and deleting accepted and rejected applications.
- **Optional Model Training**: Includes management commands for developers who wish to retrain or improve the model.

## Quick Start (Running the Application)

Follow these steps to get the application up and running on your local machine.

### 1. Prerequisites

- Ensure you have Python installed.
- Make sure the `model.pkl` file is in the root project directory.

### 2. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone <your-repository-url>
cd <your-project-directory>
```

### 3. Create and Activate a Virtual Environment

It is highly recommended to use a virtual environment to manage the project's dependencies.

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\\Scripts\\activate
# On macOS/Linux
source venv/bin/activate
```

### 4. Install Dependencies

Install all the required packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 5. Apply Database Migrations

Run the following command to apply the database migrations and create the necessary tables:

```bash
python manage.py migrate
```

### 6. Run the Development Server

Finally, start the Django development server:

```bash
python manage.py runserver
```

The application will now be running at `http://127.0.0.1:8000/`.

## How to Use

1.  **Submit an Application**: Open your web browser and navigate to `http://127.0.0.1:8000/`. Fill out the application form and click "Submit."
2.  **View Results**: After submitting, you will be taken to a results page showing whether the application was accepted or rejected.
3.  **View Application Lists**: From the main page, you can click on "Accepted Applications" or "Rejected Applications" to view the lists of all submitted applications.
4.  **Delete Applications**: In the application lists, you can click the "Delete" button to remove an application.

---

## For Developers: Retraining the Model (Optional)

If you want to modify the model or retrain it on new data, follow these steps.

### 1. Populate the Database with New Data

To generate a new set of sample data for training, run the following management command. This will delete all existing data.

```bash
python manage.py populate_db
```

### 2. Train the Model

Train the Logistic Regression model on the newly generated data. This will overwrite the existing `model.pkl` file.

```bash
python manage.py train_model
```
