import random
from django.core.management.base import BaseCommand
from scoring.models import TrainingData

class Command(BaseCommand):
    help = 'Populates the database with a more realistic, balanced set of sample training data'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing training data...')
        TrainingData.objects.all().delete()

        self.stdout.write('Populating database with new training data...')
        
        statuses = ['Accepted'] * 50 + ['Rejected'] * 50
        random.shuffle(statuses)

        for status in statuses:
            # Create more overlapping and realistic data
            if status == 'Accepted':
                # Good profiles, but with some variation
                monthly_income = random.randint(150000, 600000)
                credit_history = random.randint(2, 5) # Can have average history
                loan_amount = random.randint(100000, 7000000)
            else:
                # Weaker profiles, but not always terrible
                monthly_income = random.randint(50000, 350000)
                credit_history = random.randint(1, 4) # Can have decent history
                loan_amount = random.randint(500000, 12000000)

            training_instance = TrainingData(
                age=random.randint(18, 70),
                sex=random.choice(['male', 'female']),
                family_members=random.randint(0, 10),
                monthly_income=monthly_income,
                credit_history=credit_history,
                loan_type=random.randint(1, 6),
                loan_term=random.randint(1, 5),
                loan_amount=loan_amount,
                mortgage_type=random.randint(1, 3),
                status=status
            )
            training_instance.save()
            
        self.stdout.write(self.style.SUCCESS('Successfully populated the TrainingData table with 100 new instances.'))
