import random
from django.core.management.base import BaseCommand
from scoring.models import TrainingData, MaritalStatus, EducationLevel, EmploymentType

TOTAL_ROWS = 1000

class Command(BaseCommand):
    help = 'Populates the database with realistic, ratio-aware training data'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing training data...')
        TrainingData.objects.all().delete()

        self.stdout.write(f'Populating database with {TOTAL_ROWS} new training instances...')

        statuses = (
            [TrainingData.ApplicationStatus.ACCEPTED] * (TOTAL_ROWS // 2) +
            [TrainingData.ApplicationStatus.REJECTED] * (TOTAL_ROWS // 2)
        )
        random.shuffle(statuses)

        for status in statuses:
            monthly_income = random.randint(100000, 800000)
            other_monthly_income = random.randint(0, 150000)
            total_income = monthly_income + other_monthly_income

            if status == TrainingData.ApplicationStatus.ACCEPTED:
                # Accepted: loan is affordable relative to income (ratio 1–8×)
                loan_to_income_ratio = random.uniform(1, 8)
                credit_history = random.randint(3, 5)
                work_experience_months = random.randint(12, 300)
                # Expenses stay below 50% of income
                monthly_expenses = int(total_income * random.uniform(0.10, 0.45))
                existing_loans_amount = random.randint(0, int(total_income * 6))
                existing_monthly_payments = random.randint(0, int(total_income * 0.25))
                mortgage_type = random.randint(1, 3)
                has_guarantor = random.choice([True, False])
            else:
                # Rejected: loan is burdensome relative to income (ratio 8–100×)
                loan_to_income_ratio = random.uniform(8, 100)
                credit_history = random.randint(1, 3)
                work_experience_months = random.randint(0, 120)
                # Expenses are a high fraction of income
                monthly_expenses = int(total_income * random.uniform(0.45, 0.95))
                existing_loans_amount = random.randint(int(total_income * 5), int(total_income * 80))
                existing_monthly_payments = random.randint(int(total_income * 0.20), int(total_income * 0.80))
                mortgage_type = random.choice([1, 1, 2, 3])  # more likely no collateral
                has_guarantor = random.choice([False, False, False, True])

            loan_amount = int(total_income * loan_to_income_ratio)
            loan_amount = max(loan_amount, 50000)

            training_instance = TrainingData(
                age=random.randint(18, 70),
                sex=random.choice([TrainingData.Sex.MALE, TrainingData.Sex.FEMALE]),
                family_members=random.randint(1, 8),
                monthly_income=monthly_income,
                credit_history=credit_history,
                loan_type=random.randint(1, 6),
                loan_term=random.randint(1, 5),
                loan_amount=loan_amount,
                mortgage_type=mortgage_type,
                status=status,
                marital_status=random.choice(MaritalStatus.choices)[0],
                education_level=random.choice(EducationLevel.choices)[0],
                employment_type=random.choice(EmploymentType.choices)[0],
                work_experience_months=work_experience_months,
                other_monthly_income=other_monthly_income,
                existing_loans_amount=existing_loans_amount,
                existing_monthly_payments=existing_monthly_payments,
                monthly_expenses=monthly_expenses,
                has_guarantor=has_guarantor,
            )
            training_instance.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully populated the TrainingData table with {TOTAL_ROWS} instances.'))
