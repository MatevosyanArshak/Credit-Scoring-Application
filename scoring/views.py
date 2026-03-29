import pickle
import pandas as pd
from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import Application
from django.conf import settings

# Load the trained model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

def predict_default(application):
    # Prepare the application data for the model
    data = {
        'age': [application.age],
        'family_members': [application.family_members],
        'monthly_income': [application.monthly_income],
        'credit_history': [application.credit_history],
        'loan_type': [application.loan_type],
        'loan_term': [application.loan_term],
        'loan_amount': [application.loan_amount],
        'mortgage_type': [application.mortgage_type]
    }
    df = pd.DataFrame(data)

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
    if request.method == 'POST':
        try:
            age = int(request.POST['age'])
            if age < 18:
                return render(request, 'form.html', {'error': 'Դիմորդը պետք է լինի 18 տարեկանից բարձր', 'sex_choices': Application.Sex.choices})

            application = Application(
                first_name=request.POST['fname'],
                last_name=request.POST['lname'],
                father_name=request.POST['faname'],
                age=age,
                sex=request.POST['sex'],
                family_members=int(request.POST['family']),
                monthly_income=int(request.POST['income']),
                credit_history=int(request.POST['history']),
                loan_type=int(request.POST['type']),
                loan_term=int(request.POST['service']),
                loan_amount=int(request.POST['worth']),
                mortgage_type=int(request.POST['mortgage']),
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

        except ValueError:
            return render(request, 'form.html', {'error': 'Խնդրում ենք ճիշտ լրացնել բոլոր դաշտերը։', 'sex_choices': Application.Sex.choices})
    
    return render(request, 'form.html', {'sex_choices': Application.Sex.choices})

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
