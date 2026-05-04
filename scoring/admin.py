from django.contrib import admin
from .models import Application, TrainingData

# This line tells Django to display the Application model in the admin panel.
admin.site.register(Application)

# This line tells Django to display the TrainingData model in the admin panel.
admin.site.register(TrainingData)
