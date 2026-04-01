from django.db import models
from django.utils.translation import gettext_lazy as _


class MaritalStatus(models.TextChoices):
    SINGLE = 'Single', _('Ամուսնացած չէ')
    MARRIED = 'Married', _('Ամուսնացած')
    DIVORCED = 'Divorced', _('Ամուսնալուծված')
    WIDOWED = 'Widowed', _('Այրի')


class EducationLevel(models.TextChoices):
    HIGH_SCHOOL = 'High School', _('Միջնակարգ')
    BACHELORS = 'Bachelors', _('Բակալավր')
    MASTERS = 'Masters', _('Մագիստրոս')
    PHD = 'PhD', _('Դոկտոր')


class EmploymentType(models.TextChoices):
    FULL_TIME = 'Full-time', _('Լրիվ դրույք')
    PART_TIME = 'Part-time', _('Կես դրույք')
    SELF_EMPLOYED = 'Self-employed', _('Ինքնազբաղված')
    UNEMPLOYED = 'Unemployed', _('Գործազուրկ')


class LoanPurpose(models.TextChoices):
    DEBT_CONSOLIDATION = 'Debt Consolidation', _('Վարկերի միավորում')
    HOME_IMPROVEMENT = 'Home Improvement', _('Տան վերանորոգում')
    BUSINESS = 'Business', _('Բիզնես')
    STUDENT_LOAN = 'Student Loan', _('Ուսանողական վարկ')
    MEDICAL_EXPENSES = 'Medical Expenses', _('Բժշկական ծախսեր')


class Application(models.Model):
    class Sex(models.TextChoices):
        MALE = 'Male', _('Male')
        FEMALE = 'Female', _('Female')

    class ApplicationStatus(models.TextChoices):
        PENDING = 'Pending', _('Pending')
        ACCEPTED = 'Accepted', _('Accepted')
        REJECTED = 'Rejected', _('Rejected')

    # Existing Fields
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

    # New Fields for Better Prediction
    marital_status = models.CharField(max_length=20, choices=MaritalStatus.choices, null=True, blank=True)
    education_level = models.CharField(max_length=20, choices=EducationLevel.choices, null=True, blank=True)
    employment_type = models.CharField(max_length=20, choices=EmploymentType.choices, null=True, blank=True)
    work_experience_months = models.PositiveIntegerField(default=0)
    other_monthly_income = models.PositiveIntegerField(default=0)
    existing_loans_amount = models.PositiveIntegerField(default=0)
    existing_monthly_payments = models.PositiveIntegerField(default=0)
    monthly_expenses = models.PositiveIntegerField(default=0)
    loan_purpose = models.CharField(max_length=30, choices=LoanPurpose.choices, null=True, blank=True)
    has_guarantor = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class TrainingData(models.Model):
    class Sex(models.TextChoices):
        MALE = 'Male', _('Male')
        FEMALE = 'Female', _('Female')

    class ApplicationStatus(models.TextChoices):
        ACCEPTED = 'Accepted', _('Accepted')
        REJECTED = 'Rejected', _('Rejected')

    # Existing Fields
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

    # New Fields for Better Prediction
    marital_status = models.CharField(max_length=20, choices=MaritalStatus.choices, null=True, blank=True)
    education_level = models.CharField(max_length=20, choices=EducationLevel.choices, null=True, blank=True)
    employment_type = models.CharField(max_length=20, choices=EmploymentType.choices, null=True, blank=True)
    work_experience_months = models.PositiveIntegerField(default=0)
    other_monthly_income = models.PositiveIntegerField(default=0)
    existing_loans_amount = models.PositiveIntegerField(default=0)
    existing_monthly_payments = models.PositiveIntegerField(default=0)
    monthly_expenses = models.PositiveIntegerField(default=0)
    loan_purpose = models.CharField(max_length=30, choices=LoanPurpose.choices, null=True, blank=True)
    has_guarantor = models.BooleanField(default=False)
