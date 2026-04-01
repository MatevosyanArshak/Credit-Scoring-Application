import random
from django.core.management.base import BaseCommand
from scoring.models import TrainingData, MaritalStatus, EducationLevel, EmploymentType, LoanPurpose

class Command(BaseCommand):
    help = 'Populates the database with a more realistic, balanced set of sample training data'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing training data...')
        TrainingData.objects.all().delete()

        self.stdout.write('Populating database with new training data...')
        
        statuses = [TrainingData.ApplicationStatus.ACCEPTED] * 50 + [TrainingData.ApplicationStatus.REJECTED] * 50
        random.shuffle(statuses)

        for status in statuses:
            # Create more overlapping and realistic data
            if status == TrainingData.ApplicationStatus.ACCEPTED:
                # Good profiles, but with some variation
                monthly_income = random.randint(150000, 600000)
                credit_history = random.randint(2, 5) # Can have average history
                loan_amount = random.randint(100000, 7000000)
                work_experience_months = random.randint(12, 120)
                monthly_expenses = random.randint(50000, 150000)
            else:
                # Weaker profiles, but not always terrible
                monthly_income = random.randint(50000, 350000)
                credit_history = random.randint(1, 4) # Can have decent history
                loan_amount = random.randint(500000, 12000000)
                work_experience_months = random.randint(0, 60)
                monthly_expenses = random.randint(100000, 400000)

            training_instance = TrainingData(
                age=random.randint(18, 70),
                sex=random.choice([TrainingData.Sex.MALE, TrainingData.Sex.FEMALE]),
                family_members=random.randint(0, 10),
                monthly_income=monthly_income,
                credit_history=credit_history,
                loan_type=random.randint(1, 6),
                loan_term=random.randint(1, 5),
                loan_amount=loan_amount,
                mortgage_type=random.randint(1, 3),
                status=status,
                marital_status=random.choice(MaritalStatus.choices)[0],
                education_level=random.choice(EducationLevel.choices)[0],
                employment_type=random.choice(EmploymentType.choices)[0],
                work_experience_months=work_experience_months,
                other_monthly_income=random.randint(0, 100000),
                existing_loans_amount=random.randint(0, 5000000),
                existing_monthly_payments=random.randint(0, 200000),
                monthly_expenses=monthly_expenses,
                loan_purpose=random.choice(LoanPurpose.choices)[0],
                has_guarantor=random.choice([True, False]),
            )
            training_instance.save()
            
        self.stdout.write(self.style.SUCCESS('Successfully populated the TrainingData table with 100 new instances.'))
