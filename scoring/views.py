import pickle
import pandas as pd
from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import Application, TrainingData

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

def application_form(request):
    if request.method == 'POST':
        try:
            age = int(request.POST['age'])
            if age < 18:
                return render(request, 'form.html', {'error': 'Applicant must be at least 18 years old'})

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
            
            # --- Budget and Profitability Logic ---
            BANK_BUDGET = 20000000
            BASE_INTEREST_RATE = 0.05  # 5%
            RISK_PREMIUM_FACTOR = 0.20 # 20% - higher factor means more penalty for risk

            # 1. Calculate total amount of currently accepted loans
            total_accepted_loans = Application.objects.filter(status='Accepted').aggregate(Sum('loan_amount'))['loan_amount__sum'] or 0

            # 2. Check if the new loan exceeds the budget
            if total_accepted_loans + application.loan_amount > BANK_BUDGET:
                application.status = 'Rejected'
                application.prob_default = predict_default(application) # Predict for info purposes
                application.save()
                msg = f"Application Rejected: Not enough budget remaining. (Available: {BANK_BUDGET - total_accepted_loans})"
                return render(request, 'result.html', {'msg': msg})

            # 3. Calculate profitability
            prob_default = predict_default(application)
            application.prob_default = prob_default

            interest_rate = BASE_INTEREST_RATE + (prob_default * RISK_PREMIUM_FACTOR)
            expected_return = application.loan_amount * interest_rate
            expected_loss = application.loan_amount * prob_default
            expected_profit = expected_return - expected_loss

            # 4. Make a decision based on profitability
            if expected_profit > 0:
                application.status = 'Accepted'
                msg = f"Application Accepted! (Expected Profit: {expected_profit:.2f})"
            else:
                application.status = 'Rejected'
                msg = f"Application Rejected: Not profitable enough. (Expected Profit: {expected_profit:.2f})"
            
            application.save()
            
            return render(request, 'result.html', {'msg': msg})

        except ValueError:
            return render(request, 'form.html', {'error': 'Please fill in all fields correctly.'})
    
    return render(request, 'form.html')

def accepted_applications(request):
    applications = Application.objects.filter(status='Accepted')
    return render(request, 'applications.html', {'applications': applications, 'title': 'Accepted Applications'})

def rejected_applications(request):
    applications = Application.objects.filter(status='Rejected')
    return render(request, 'applications.html', {'applications': applications, 'title': 'Rejected Applications'})

def delete_application(request, pk):
    try:
        application = Application.objects.get(pk=pk)
        application.delete()
    except Application.DoesNotExist:
        pass # Or handle the error appropriately
    # Redirect to the previous page
    return redirect(request.META.get('HTTP_REFERER', '/'))
