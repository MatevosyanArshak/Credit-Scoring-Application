import pickle
import pandas as pd
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Sum, Avg
from .models import Application, MaritalStatus, EducationLevel, EmploymentType
from django.conf import settings
# Lazily load and cache the trained model when it is first needed.
model = None
def get_model():
    global model
    if model is None:
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
    return model
def predict_default(application):
    # This list MUST be in the exact same order as in train_model.py
    features_order = [
        'age', 'sex', 'family_members', 'monthly_income', 'credit_history',
        'loan_type', 'loan_term', 'loan_amount', 'mortgage_type',
        'marital_status', 'education_level', 'employment_type',
        'work_experience_months', 'other_monthly_income',
        'existing_loans_amount', 'existing_monthly_payments',
        'monthly_expenses', 'has_guarantor',
        'loan_to_income_ratio', 'expense_to_income_ratio',
    ]
    safe_income = application.monthly_income if application.monthly_income > 0 else 1
    # Prepare the application data for the model
    data = {
        'age': [application.age],
        'sex': [1 if application.sex == Application.Sex.MALE else 0],
        'family_members': [application.family_members],
        'monthly_income': [application.monthly_income],
        'credit_history': [application.credit_history],
        'loan_type': [application.loan_type],
        'loan_term': [application.loan_term],
        'loan_amount': [application.loan_amount],
        'mortgage_type': [application.mortgage_type],
        'marital_status': [[c[0] for c in MaritalStatus.choices].index(application.marital_status)],
        'education_level': [[c[0] for c in EducationLevel.choices].index(application.education_level)],
        'employment_type': [[c[0] for c in EmploymentType.choices].index(application.employment_type)],
        'work_experience_months': [application.work_experience_months],
        'other_monthly_income': [application.other_monthly_income],
        'existing_loans_amount': [application.existing_loans_amount],
        'existing_monthly_payments': [application.existing_monthly_payments],
        'monthly_expenses': [application.monthly_expenses],
        'has_guarantor': [1 if application.has_guarantor else 0],
        'loan_to_income_ratio': [application.loan_amount / safe_income],
        'expense_to_income_ratio': [application.monthly_expenses / safe_income],
    }
    df = pd.DataFrame(data)
    # Enforce the correct feature order
    df = df[features_order]
    # Logistic regression can extrapolate to extreme values. Keep an upper cap to
    # avoid exact 1.0 but preserve low-risk differentiation.
    prob_default = get_model().predict_proba(df)[0][1]
    prob_default = max(1e-9, min(0.99, prob_default))
    return prob_default
def process_pending_applications():
    """Accept/reject pending applications based solely on default probability threshold."""
    pending_applications = Application.objects.filter(status=Application.ApplicationStatus.PENDING)
    if not pending_applications.exists():
        return
    for app in pending_applications:
        if app.prob_default is not None and app.prob_default >= settings.MAX_DEFAULT_RATE:
            app.status = Application.ApplicationStatus.REJECTED
        else:
            app.status = Application.ApplicationStatus.ACCEPTED
        app.save()
def build_optimal_portfolio(available_budget):
    """Greedy selection of accepted applications by expected_profit within budget."""
    accepted_applications = Application.objects.filter(
        status=Application.ApplicationStatus.ACCEPTED
    )
    sorted_apps = sorted(
        accepted_applications,
        key=lambda app: app.expected_profit if app.expected_profit is not None else 0,
        reverse=True
    )
    selected = []
    remaining = available_budget
    for app in sorted_apps:
        if app.loan_amount <= remaining and (app.expected_profit or 0) > 0:
            selected.append(app)
            remaining -= app.loan_amount
    return selected, available_budget - remaining


def home(request):
    return render(request, 'home.html')


def application_form(request):
    context = {
        'sex_choices': Application.Sex.choices,
        'marital_status_choices': MaritalStatus.choices,
        'education_level_choices': EducationLevel.choices,
        'employment_type_choices': EmploymentType.choices,
    }
    if request.method == 'POST':
        try:
            age = int(request.POST['age'])
            monthly_income = int(request.POST['income'])
            family_members = int(request.POST['family'])
            if age < 18:
                context['error'] = 'Դիմորդը պետք է լինի 18 տարեկանից բարձր'
                return render(request, 'form.html', context)
            if monthly_income <= 0:
                context['error'] = 'Ամսական եկամուտը պետք է լինի 0-ից մեծ'
                return render(request, 'form.html', context)
            if family_members <= 0:
                context['error'] = 'Ընտանիքի անդամների թիվը պետք է լինի 0-ից մեծ'
                return render(request, 'form.html', context)
            application = Application(
                first_name=request.POST['fname'],
                last_name=request.POST['lname'],
                father_name=request.POST['faname'],
                age=age,
                sex=request.POST['sex'],
                family_members=family_members,
                monthly_income=monthly_income,
                credit_history=int(request.POST['history']),
                loan_type=int(request.POST['type']),
                loan_term=int(request.POST['service']),
                loan_amount=int(request.POST['worth']),
                mortgage_type=int(request.POST['mortgage']),
                marital_status=request.POST['marital_status'],
                education_level=request.POST['education_level'],
                employment_type=request.POST['employment_type'],
                work_experience_months=int(request.POST['work_experience_months']),
                other_monthly_income=int(request.POST.get('other_monthly_income', 0)),
                existing_loans_amount=int(request.POST.get('existing_loans_amount', 0)),
                existing_monthly_payments=int(request.POST.get('existing_monthly_payments', 0)),
                monthly_expenses=int(request.POST['monthly_expenses']),
                has_guarantor='has_guarantor' in request.POST,
            )
            # Calculate profitability and save with Pending status
            prob_default = predict_default(application)
            application.prob_default = prob_default
            # Annual interest rate rises with risk; multiply by loan duration in years
            interest_rate = settings.BASE_INTEREST_RATE + (prob_default * settings.RISK_PREMIUM_FACTOR)
            loan_term_years = settings.LOAN_TERM_YEARS.get(application.loan_term, 1.5)
            expected_return = application.loan_amount * interest_rate * loan_term_years
            expected_loss = application.loan_amount * prob_default
            expected_profit = expected_return - expected_loss
            application.expected_profit = expected_profit
            application.save()
            return render(request, 'result.html', {'msg': 'Ձեր հայտը հաջողությամբ ուղարկվել է և գտնվում է դիտարկման մեջ։'})
        except FileNotFoundError:
            context['error'] = 'Մոդելը բացակայում է։ Խնդրում ենք վերամարզել այն (Training model...)։'
            return render(request, 'form.html', context)
        except (ValueError, KeyError) as e:
            context['error'] = f'Խնդրում ենք ճիշտ լրացնել բոլոր դաշտերը։ Սխալի մանրամասներ: {e}'
            return render(request, 'form.html', context)
    return render(request, 'form.html', context)
def accepted_applications(request):
    applications = Application.objects.filter(status=Application.ApplicationStatus.ACCEPTED)
    total_profit = applications.aggregate(Sum('expected_profit'))['expected_profit__sum'] or 0
    mean_default = applications.aggregate(Avg('prob_default'))['prob_default__avg'] or 0
    budget_error = request.GET.get('budget_error')
    budget_value = request.GET.get('budget', '')
    return render(request, 'applications.html', {
        'applications': applications,
        'title': 'Բавараrvats Нayterə',
        'page_type': 'accepted',
        'total_profit': total_profit,
        'mean_default': mean_default,
        'budget_error': budget_error,
        'budget_value': budget_value,
    })
def rejected_applications(request):
    applications = Application.objects.filter(status=Application.ApplicationStatus.REJECTED)
    return render(request, 'applications.html', {
        'applications': applications,
        'title': 'Մերժված հայտեր',
        'page_type': 'rejected',
    })
def pending_applications(request):
    applications = Application.objects.filter(status=Application.ApplicationStatus.PENDING)
    return render(request, 'applications.html', {
        'applications': applications,
        'title': 'Սպասվող հայտեր',
        'page_type': 'pending',
    })
def process_applications(request):
    """Manually triggered: accept/reject pending apps based on default probability."""
    if request.method == 'POST':
        process_pending_applications()
    return redirect('pending_applications')
def optimal_portfolio(request):
    """Show optimal portfolio. POST from accepted page to compute; GET to display from session."""
    if request.method == 'POST':
        try:
            budget = int(request.POST['budget'])
            if budget <= 0:
                raise ValueError('Budget must be positive')
            selected, total_used = build_optimal_portfolio(budget)
            if not selected:
                # Budget too small — go back to accepted page with error
                url = reverse('accepted_applications') + f'?budget_error=1&budget={budget}'
                return redirect(url)
            # Move selected apps from ACCEPTED → PORTFOLIO status
            for app in selected:
                app.status = Application.ApplicationStatus.PORTFOLIO
                app.save()
            request.session['portfolio_budget'] = budget
            request.session['portfolio_used'] = total_used
        except (ValueError, KeyError):
            pass
        return redirect('optimal_portfolio')

    # GET: display portfolio (from PORTFOLIO status in DB, supplemented by session stats)
    portfolio_ids = request.session.get('portfolio_ids', [])
    budget = request.session.get('portfolio_budget', 0)
    total_used = request.session.get('portfolio_used', 0)
    applications = list(Application.objects.filter(status=Application.ApplicationStatus.PORTFOLIO))
    total_profit = sum(a.expected_profit or 0 for a in applications)
    mean_default = sum(a.prob_default or 0 for a in applications) / len(applications) if applications else 0
    return render(request, 'portfolio.html', {
        'applications': applications,
        'budget': budget,
        'total_used': total_used,
        'remaining_budget': max(0, budget - total_used),
        'total_profit': total_profit,
        'mean_default': mean_default,
    })
def remove_from_portfolio(request, pk):
    """Move an application back from Portfolio → Accepted status."""
    try:
        application = Application.objects.get(pk=pk, status=Application.ApplicationStatus.PORTFOLIO)
        application.status = Application.ApplicationStatus.ACCEPTED
        application.save()
    except Application.DoesNotExist:
        pass
    return redirect('optimal_portfolio')


def delete_application(request, pk):
    try:
        application = Application.objects.get(pk=pk)
        application.delete()
    except Application.DoesNotExist:
        pass
    return redirect(request.META.get('HTTP_REFERER', '/'))
