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
class Application(models.Model):
    class Sex(models.TextChoices):
        MALE = 'Male', _('Male')
        FEMALE = 'Female', _('Female')
    class ApplicationStatus(models.TextChoices):
        PENDING = 'Pending', _('Pending')
        ACCEPTED = 'Accepted', _('Accepted')
        REJECTED = 'Rejected', _('Rejected')
        PORTFOLIO = 'Portfolio', _('Portfolio')
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
    has_guarantor = models.BooleanField(default=False)

    CREDIT_HISTORY_LABELS = {
        1: 'Վատ',
        2: 'Ինֆորմացիա չկա',
        3: 'Միջին',
        4: 'Լավ',
        5: 'Գերազանց',
    }
    LOAN_TYPE_LABELS = {
        1: 'Հիփոթեքային վարկ',
        2: 'Ավտոմեքենայի վարկ',
        3: 'Սպառողական վարկ',
        5: 'Ապառիկ վարկ',
        6: 'Տան վերանորոգման վարկ',
    }
    LOAN_TERM_LABELS = {
        1: 'Մինչև 18 ամիս',
        2: '19-24',
        3: '25-60',
        4: '61-120',
        5: '121 և ավել',
    }
    MORTGAGE_TYPE_LABELS = {
        1: 'Առանց գրավի',
        2: 'Մեքենայի գրավով',
        3: 'Անշառժ գույքի գրավով',
    }
    def get_credit_history_display_label(self):
        return self.CREDIT_HISTORY_LABELS.get(self.credit_history, str(self.credit_history))
    def get_loan_type_display_label(self):
        return self.LOAN_TYPE_LABELS.get(self.loan_type, str(self.loan_type))
    def get_loan_term_display_label(self):
        return self.LOAN_TERM_LABELS.get(self.loan_term, str(self.loan_term))
    def get_mortgage_type_display_label(self):
        return self.MORTGAGE_TYPE_LABELS.get(self.mortgage_type, str(self.mortgage_type))
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
    has_guarantor = models.BooleanField(default=False)
