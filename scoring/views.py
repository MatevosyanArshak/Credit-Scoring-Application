import pickle
import pandas as pd
from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import Application, MaritalStatus, EducationLevel, EmploymentType, LoanPurpose
from django.conf import settings

# Load the trained model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

def predict_default(application):
    # This list MUST be in the exact same order as in train_model.py
    features_order = [
        'age', 'sex', 'family_members', 'monthly_income', 'credit_history',
        'loan_type', 'loan_term', 'loan_amount', 'mortgage_type',
        'marital_status', 'education_level', 'employment_type',
        'work_experience_months', 'other_monthly_income',
        'existing_loans_amount', 'existing_monthly_payments',
        'monthly_expenses', 'loan_purpose', 'has_guarantor'
    ]

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
        'loan_purpose': [[c[0] for c in LoanPurpose.choices].index(application.loan_purpose)],
        'has_guarantor': [1 if application.has_guarantor else 0],
    }
    df = pd.DataFrame(data)

    # Enforce the correct feature order
    df = df[features_order]

    # Make a prediction
    prob_default = model.predict_proba(df)[0][1]
    return prob_default

def process_pending_applications():
    pending_applications = Application.objects.filter(status=Application.ApplicationStatus.PENDING)
    
    if pending_applications.count() >= 20:
        # Sort applications by expected profit in descending order
        sorted_applications = sorted(pending_applications, key=lambda app: app.expected_profit, reverse=True)
        
        # Get the current budget
        total_accepted_loans = Application.objects.filter(status=Application.ApplicationStatus.ACCEPTED).aggregate(Sum('loan_amount'))['loan_amount__sum'] or 0
        available_budget = settings.BANK_BUDGET - total_accepted_loans
        
        for app in sorted_applications:
            if app.loan_amount <= available_budget and app.expected_profit > 0:
                app.status = Application.ApplicationStatus.ACCEPTED
                available_budget -= app.loan_amount
            else:
                app.status = Application.ApplicationStatus.REJECTED
            app.save()

def application_form(request):
    context = {
        'sex_choices': Application.Sex.choices,
        'marital_status_choices': MaritalStatus.choices,
        'education_level_choices': EducationLevel.choices,
        'employment_type_choices': EmploymentType.choices,
        'loan_purpose_choices': LoanPurpose.choices,
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

            # Handle 'Other' loan purpose
            loan_purpose = request.POST['loan_purpose']
            if loan_purpose == LoanPurpose.OTHER:
                loan_purpose = LoanPurpose.OTHER

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
                loan_purpose=loan_purpose,
                has_guarantor='has_guarantor' in request.POST,
            )
            
            # Calculate profitability and save with Pending status
            prob_default = predict_default(application)
            application.prob_default = prob_default

            interest_rate = settings.BASE_INTEREST_RATE + (prob_default * settings.RISK_PREMIUM_FACTOR)
            expected_return = application.loan_amount * interest_rate
            expected_loss = application.loan_amount * prob_default
            expected_profit = expected_return - expected_loss
            application.expected_profit = expected_profit
            
            application.save() # The default status is 'Pending'
            
            # Process pending applications if the batch size is reached
            process_pending_applications()
            
            return render(request, 'result.html', {'msg': 'Ձեր հայտը հաջողությամբ ուղարկվել է և գտնվում է դիտարկման մեջ։'})

        except (ValueError, KeyError) as e:
            context['error'] = f'Խնդրում ենք ճիշտ լրացնել բոլոր դաշտերը։ Սխալի մանրամասներ: {e}'
            return render(request, 'form.html', context)
    
    return render(request, 'form.html', context)

def accepted_applications(request):
    applications = Application.objects.filter(status=Application.ApplicationStatus.ACCEPTED)
    return render(request, 'applications.html', {'applications': applications, 'title': 'Բավարարված հայտեր'})

def rejected_applications(request):
    applications = Application.objects.filter(status=Application.ApplicationStatus.REJECTED)
    return render(request, 'applications.html', {'applications': applications, 'title': 'Մերժված հայտեր'})

def pending_applications(request):
    applications = Application.objects.filter(status=Application.ApplicationStatus.PENDING)
    return render(request, 'applications.html', {'applications': applications, 'title': 'Սպասվող հայտեր'})

def delete_application(request, pk):
    try:
        application = Application.objects.get(pk=pk)
        application.delete()
    except Application.DoesNotExist:
        pass
    return redirect(request.META.get('HTTP_REFERER', '/'))
