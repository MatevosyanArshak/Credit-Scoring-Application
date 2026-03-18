import pickle
import pandas as pd
from django.core.management.base import BaseCommand
from scoring.models import Application

class Command(BaseCommand):
    help = 'Recalculates and updates the probability and status for all existing applications'

    def handle(self, *args, **options):
        self.stdout.write('Loading the trained model...')
        try:
            with open('model.pkl', 'rb') as f:
                model = pickle.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('model.pkl not found. Please train the model first by running `python manage.py train_model`.'))
            return

        self.stdout.write('Fetching all applications from the database...')
        applications = Application.objects.all()

        if not applications.exists():
            self.stdout.write(self.style.WARNING('No applications found in the database.'))
            return

        self.stdout.write(f'Updating probabilities and statuses for {applications.count()} applications...')

        for application in applications:
            # Prepare data for the model
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

            # Predict the probability of default (class 1)
            prob_default = model.predict_proba(df)[0][1]

            # Update the application's probability and status
            application.prob_default = prob_default
            if prob_default >= 0.5:
                application.status = 'Rejected'
            else:
                application.status = 'Accepted'

            application.save()

        self.stdout.write(self.style.SUCCESS('Successfully updated all application probabilities and statuses.'))
