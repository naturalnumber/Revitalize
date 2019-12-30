from django.db import models
from django.utils.translation import gettext_lazy as _


# from django_mysql import models


class AbstractIndicator(models.Model):
    class DataType(models.TextChoices):
        UNKNOWN = '?', _('Unknown')
        INTEGER = 'I', _('Integer')
        FLOAT = 'F', _('Decimal')
        BOOLEAN = 'B', _('Boolean')
        CATEGORY = 'C', _('Category')

    id = models.AutoField(editable=False, primary_key=True)
    type = models.CharField(max_length=40, blank=False, choices=DataType.choices, default=DataType.UNKNOWN,
                            help_text="This should be a data type.")
    specification = models.TextField(blank=False, help_text="This should be a JSON.")
    analysis = models.TextField(blank=False, help_text="This should be a JSON.")

    class Meta:
        abstract = True


class AbstractDataPoint(models.Model):
    id = models.BigAutoField(editable=False, primary_key=True)
    creation_time = models.DateTimeField(auto_now_add=True, null=False)
    time = models.DateTimeField(null=False)
    value = models.TextField(blank=False, help_text="This should be a JSON.")

    class Meta:
        abstract = True


class Client(models.Model):
    id = models.AutoField(editable=False, primary_key=True)
    username = models.EmailField(blank=False, unique=True, help_text="The email address a user will log in with.")
    first_name = models.CharField(max_length=40, blank=False)
    middle_name = models.CharField(max_length=40, null=False, blank=True)
    last_name = models.CharField(max_length=40, blank=False)  # db_index=True
    birth_date = models.DateField(null=False)
    creation_time = models.DateTimeField(auto_now_add=True, null=False)
    points = models.BigIntegerField(null=False, verbose_name="Health Currency")  # Int or Decimal?
    password_flag = models.BooleanField(null=False, verbose_name="Password Reset Flag",
                                        help_text="True if the password needs to be reset.", default=True)


class Cohort(models.Model):
    id = models.AutoField(editable=False, primary_key=True)
    name = models.CharField(max_length=40, blank=False, unique=True)
    clients = models.ManyToManyField('Client', db_table='cohort_membership')


class Form(models.Model):
    class FormType(models.TextChoices):
        UNKNOWN = '?', _('Unknown')
        SURVEY = 'S', _('Survey')
        MEDICAL_TEST = 'M', _('Medical Test')
        DIETARY_JOURNAL = 'D', _('Dietary Journal Entry')

    id = models.AutoField(editable=False, primary_key=True)
    name = models.CharField(max_length=40, blank=False, unique=True)
    type = models.CharField(max_length=40, blank=False, choices=FormType.choices, default=FormType.UNKNOWN)
    display = models.TextField(blank=False, help_text="This should be a JSON.")
    specification = models.TextField(blank=False, help_text="This should be a JSON.")
    analysis = models.TextField(blank=False, help_text="This should be a JSON.")


class Submission(models.Model):
    id = models.BigAutoField(editable=False, primary_key=True)
    client = models.ForeignKey('Client', on_delete=models.CASCADE, null=False)  # related_name='+'
    form = models.ForeignKey('Form', on_delete=models.SET_NULL, null=True)
    creation_time = models.DateField(auto_now_add=True, null=False)
    time = models.DateTimeField(null=False)
    values = models.TextField(blank=False, help_text="This should be a JSON.")


class Indicator(AbstractIndicator):
    name = models.CharField(max_length=40, blank=False, unique=True)


class DataPoint(AbstractDataPoint):
    client = models.ForeignKey('Client', on_delete=models.CASCADE, null=False)  # related_name='+'
    indicator = models.ForeignKey('Indicator', on_delete=models.SET_NULL, null=True)


class Goal(models.Model):
    id = models.BigAutoField(editable=False, primary_key=True)
    client = models.ForeignKey('Client', on_delete=models.CASCADE, null=False)  # related_name='+'
    indicator = models.ForeignKey('Indicator', on_delete=models.SET_NULL, null=True)
    creation_time = models.DateTimeField(auto_now_add=True, null=False)
    start = models.DateTimeField(null=False)
    target = models.TextField(blank=False, help_text="This should be a JSON.")
    completed = models.BooleanField(null=False, default=False)


class AnonymizedIndicator(AbstractIndicator):
    indicator = models.ForeignKey('Indicator', on_delete=models.SET_NULL, null=True)


class CohortDataPoint(AbstractDataPoint):
    cohort = models.ForeignKey('Cohort', on_delete=models.CASCADE, null=False)  # related_name='+'
    a_indicator = models.ForeignKey('AnonymizedIndicator', on_delete=models.SET_NULL, null=True)
    a_client_id = models.IntegerField(null=False)
