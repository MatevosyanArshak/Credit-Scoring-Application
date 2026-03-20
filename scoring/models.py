from django.db import models

class Application(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    age = models.IntegerField()
    sex = models.CharField(max_length=10)
    family_members = models.IntegerField()
    monthly_income = models.IntegerField()
    credit_history = models.IntegerField()
    loan_type = models.IntegerField()
    loan_term = models.IntegerField()
    loan_amount = models.IntegerField()
    mortgage_type = models.IntegerField()
    prob_default = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class TrainingData(models.Model):
    age = models.IntegerField()
    sex = models.CharField(max_length=10)
    family_members = models.IntegerField()
    monthly_income = models.IntegerField()
    credit_history = models.IntegerField()
    loan_type = models.IntegerField()
    loan_term = models.IntegerField()
    loan_amount = models.IntegerField()
    mortgage_type = models.IntegerField()
    status = models.CharField(max_length=20, null=True, blank=True)
