import pickle
import pandas as pd
from django.core.management.base import BaseCommand
from sklearn.linear_model import LogisticRegression
from scoring.models import TrainingData, MaritalStatus, EducationLevel, EmploymentType, LoanPurpose, Application

class Command(BaseCommand):
    help = 'Trains the Logistic Regression model on the TrainingData table'

    def handle(self, *args, **options):
        self.stdout.write('Training model...')

        # Fetch data from the TrainingData table
        training_data = TrainingData.objects.all()
        if not training_data.exists():
            self.stdout.write(self.style.ERROR('No data found in the TrainingData table. Please run `python manage.py populate_db` first.'))
            return

        # Convert queryset to DataFrame
        df = pd.DataFrame(list(training_data.values()))

        # --- Start of Critical Data Preparation ---

        # Convert categorical 'status' to numerical target
        df['status'] = df['status'].apply(lambda x: 1 if x == TrainingData.ApplicationStatus.REJECTED else 0)
        
        # Convert all categorical features to numerical, matching the prediction logic
        df['sex'] = df['sex'].apply(lambda x: 1 if x == Application.Sex.MALE else 0)
        df['marital_status'] = df['marital_status'].apply(lambda x: [c[0] for c in MaritalStatus.choices].index(x))
        df['education_level'] = df['education_level'].apply(lambda x: [c[0] for c in EducationLevel.choices].index(x))
        df['employment_type'] = df['employment_type'].apply(lambda x: [c[0] for c in EmploymentType.choices].index(x))
        df['loan_purpose'] = df['loan_purpose'].apply(lambda x: [c[0] for c in LoanPurpose.choices].index(x))
        df['has_guarantor'] = df['has_guarantor'].apply(lambda x: 1 if x else 0)

        # This feature list MUST be in the exact same order as in views.py
        features = [
            'age', 'sex', 'family_members', 'monthly_income', 'credit_history',
            'loan_type', 'loan_term', 'loan_amount', 'mortgage_type',
            'marital_status', 'education_level', 'employment_type',
            'work_experience_months', 'other_monthly_income',
            'existing_loans_amount', 'existing_monthly_payments',
            'monthly_expenses', 'loan_purpose', 'has_guarantor'
        ]

        X = df[features]
        y = df['status']

        # --- End of Critical Data Preparation ---

        # Train the model
        model = LogisticRegression(max_iter=2000, solver='liblinear')
        model.fit(X, y)

        # Save the trained model to a file
        with open('model.pkl', 'wb') as f:
            pickle.dump(model, f)

        self.stdout.write(self.style.SUCCESS('Successfully trained and saved the model as model.pkl'))
