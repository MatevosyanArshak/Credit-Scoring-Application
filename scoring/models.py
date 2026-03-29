from django.db import models
from django.utils.translation import gettext_lazy as _


class Application(models.Model):
    class Sex(models.TextChoices):
        MALE = 'Male', _('Male')
        FEMALE = 'Female', _('Female')

    class ApplicationStatus(models.TextChoices):
        PENDING = 'Pending', _('Pending')
        ACCEPTED = 'Accepted', _('Accepted')
        REJECTED = 'Rejected', _('Rejected')

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    sex = models.CharField(max_length=10, choices=Sex.choices)
    family_members = models.PositiveIntegerField()
    monthly_income = models.PositiveIntegerField()
    credit_history = models.IntegerField()
    loan_type = models.IntegerField()
    loan_term = models.PositiveIntegerField()
    loan_amount = models.PositiveIntegerField()
    mortgage_type = models.IntegerField()
    prob_default = models.FloatField(null=True, blank=True)
    expected_profit = models.FloatField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.PENDING
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class TrainingData(models.Model):
    class Sex(models.TextChoices):
        MALE = 'Male', _('Male')
        FEMALE = 'Female', _('Female')

    class ApplicationStatus(models.TextChoices):
        ACCEPTED = 'Accepted', _('Accepted')
        REJECTED = 'Rejected', _('Rejected')

    age = models.PositiveIntegerField()
    sex = models.CharField(max_length=10, choices=Sex.choices)
    family_members = models.PositiveIntegerField()
    monthly_income = models.PositiveIntegerField()
    credit_history = models.IntegerField()
    loan_type = models.IntegerField()
    loan_term = models.PositiveIntegerField()
    loan_amount = models.PositiveIntegerField()
    mortgage_type = models.IntegerField()
    status = models.CharField(max_length=20, choices=ApplicationStatus.choices, null=True, blank=True)
