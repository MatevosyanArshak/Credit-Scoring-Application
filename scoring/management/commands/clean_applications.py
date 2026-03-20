from django.core.management.base import BaseCommand
from scoring.models import Application

class Command(BaseCommand):
    help = 'Deletes old, leftover training data from the main Application table.'

    def handle(self, *args, **options):
        self.stdout.write('Searching for old training data in the Application table...')
        
        # Safely identify old training data by the "FirstName" pattern
        old_training_apps = Application.objects.filter(first_name__startswith='FirstName')
        
        count = old_training_apps.count()
        
        if count > 0:
            self.stdout.write(f'Found {count} old training applications. Deleting them now...')
            old_training_apps.delete()
            self.stdout.write(self.style.SUCCESS('Successfully cleaned the Application table.'))
        else:
            self.stdout.write(self.style.SUCCESS('No old training data found. Your Application table is already clean.'))
