import pickle
import pandas as pd
from django.shortcuts import render, redirect
from .models import Application

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
            
            prob_default = predict_default(application)
            application.prob_default = prob_default
            
            if prob_default >= 0.5: # Using 0.5 as the threshold for the trained model
                application.status = 'Rejected'
                msg = 'Application Rejected'
            else:
                application.status = 'Accepted'
                msg = 'Application Accepted'
                
            application.save()
            
            return render(request, 'result.html', {'msg': msg})
        except ValueError:
            return render(request, 'form.html', {'error': 'Please fill in all fields'})
    
    return render(request, 'form.html')

def accepted_applications(request):
    applications = Application.objects.filter(status='Accepted', is_training_data=False)
    return render(request, 'applications.html', {'applications': applications, 'title': 'Accepted Applications'})

def rejected_applications(request):
    applications = Application.objects.filter(status='Rejected', is_training_data=False)
    return render(request, 'applications.html', {'applications': applications, 'title': 'Rejected Applications'})

def delete_application(request, pk):
    application = Application.objects.get(pk=pk)
    application.delete()
    # Redirect to the previous page
    return redirect(request.META.get('HTTP_REFERER', '/'))
