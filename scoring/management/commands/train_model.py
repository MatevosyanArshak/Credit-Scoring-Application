import pickle
import pandas as pd
from django.core.management.base import BaseCommand
from sklearn.linear_model import LogisticRegression
from scoring.models import Application

class Command(BaseCommand):
    help = 'Trains the Logistic Regression model'

    def handle(self, *args, **options):
        self.stdout.write('Training model...')

        # Fetch data from the database
        applications = Application.objects.all()
        if not applications.exists():
            self.stdout.write(self.style.ERROR('No data found in the database. Please run populate_db first.'))
            return

        # Convert queryset to DataFrame
        df = pd.DataFrame(list(applications.values(
            'age', 'family_members', 'monthly_income', 'credit_history',
            'loan_type', 'loan_term', 'loan_amount', 'mortgage_type', 'status'
        )))

        # Prepare data for training
        # Convert categorical 'status' to numerical
        df['status'] = df['status'].apply(lambda x: 1 if x == 'Rejected' else 0)

        # Define features (X) and target (y)
        features = [
            'age', 'family_members', 'monthly_income', 'credit_history',
            'loan_type', 'loan_term', 'loan_amount', 'mortgage_type'
        ]
        X = df[features]
        y = df['status']

        # Train the model
        model = LogisticRegression(max_iter=1000)
        model.fit(X, y)

        # Save the trained model to a file
        with open('model.pkl', 'wb') as f:
            pickle.dump(model, f)

        self.stdout.write(self.style.SUCCESS('Successfully trained and saved the model as model.pkl'))
