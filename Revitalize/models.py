from django.db import models
from django.utils.translation import gettext_lazy as _


class ModelBase(models.Model):
    rm_fields: list = ['id', 'flags', 'creation_time', 'update_time']
    rm_fields_display: list = ['id']
    rm_fields_filter: list = ['id']
    rm_fields_search: list = ['id']
    rm_fields_serialize: list = rm_fields.copy()

    id = models.AutoField(editable=False, primary_key=True)
    flags = models.TextField(blank=False, help_text="This should be a JSON.", default="{}")

    creation_time = models.DateTimeField(auto_now_add=True, null=False)
    update_time = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        abstract = True


class ModelMore(ModelBase):
    rm_fields: list = ModelBase.rm_fields.copy()
    rm_fields_display: list = ModelBase.rm_fields.copy()
    rm_fields_filter: list = ModelBase.rm_fields.copy()
    rm_fields_search: list = ModelBase.rm_fields.copy()
    rm_fields_serialize: list = ModelBase.rm_fields.copy()

    rm_fields.extend(['name', 'description', 'notes'])
    rm_fields_display.extend(['name'])
    rm_fields_filter.extend(['name'])
    rm_fields_search.extend(['name'])
    rm_fields_serialize.extend(['name', 'description', 'notes'])

    name = models.CharField(max_length=40, blank=False, unique=True)
    description = models.TextField(blank=True, null=False)
    notes = models.TextField(blank=True, null=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class ModelProcessable(ModelMore):
    rm_fields: list = ModelMore.rm_fields.copy()
    rm_fields_display: list = ModelMore.rm_fields.copy()
    rm_fields_filter: list = ModelMore.rm_fields.copy()
    rm_fields_search: list = ModelMore.rm_fields.copy()
    rm_fields_serialize: list = ModelMore.rm_fields.copy()

    rm_fields.extend(['specification', 'analysis'])
    rm_fields_serialize.extend(['specification', 'analysis'])

    specification = models.TextField(blank=False, help_text="This should be a JSON.")
    analysis = models.TextField(blank=False, help_text="This should be a JSON.")

    class Meta:
        abstract = True


class AbstractIndicator(ModelProcessable):
    rm_fields: list = ModelProcessable.rm_fields.copy()
    rm_fields_display: list = ModelProcessable.rm_fields.copy()
    rm_fields_filter: list = ModelProcessable.rm_fields.copy()
    rm_fields_search: list = ModelProcessable.rm_fields.copy()
    rm_fields_serialize: list = ModelProcessable.rm_fields.copy()

    rm_fields.extend(['type'])
    rm_fields_display.extend(['type'])
    rm_fields_filter.extend(['type'])
    rm_fields_search.extend(['type'])
    rm_fields_serialize.extend(['type'])

    class DataType(models.TextChoices):
        UNKNOWN = '?', _('Unknown')
        INTEGER = 'I', _('Integer')
        FLOAT = 'F', _('Decimal')
        BOOLEAN = 'B', _('Boolean')
        CATEGORY = 'C', _('Category')

    type = models.CharField(max_length=1, blank=False, choices=DataType.choices, default=DataType.UNKNOWN,
                            help_text="This should be a data type.")

    class Meta:
        abstract = True


class AbstractDataPoint(ModelBase):
    rm_fields: list = ModelBase.rm_fields.copy()
    rm_fields_display: list = ModelBase.rm_fields.copy()
    rm_fields_filter: list = ModelBase.rm_fields.copy()
    rm_fields_search: list = ModelBase.rm_fields.copy()
    rm_fields_serialize: list = ModelBase.rm_fields.copy()

    rm_fields.extend(['time', 'value', 'notes'])
    rm_fields_display.extend(['time', 'value'])
    rm_fields_filter.extend(['time', 'value'])
    rm_fields_search.extend(['time', 'value'])
    rm_fields_serialize.extend(['time', 'description', 'notes'])

    time = models.DateTimeField(null=False)
    value = models.TextField(blank=False, help_text="This should be a JSON.", default="{}")

    notes = models.TextField(blank=True, null=False)

    class Meta:
        abstract = True


class Client(ModelBase):
    rm_fields: list = ModelBase.rm_fields.copy()
    rm_fields_display: list = ModelBase.rm_fields.copy()
    rm_fields_filter: list = ModelBase.rm_fields.copy()
    rm_fields_search: list = ModelBase.rm_fields.copy()
    #rm_fields_serialize: list = ModelBase.rm_fields.copy()

    rm_fields.extend(['username', 'first_name', 'middle_name', 'last_name', 'birth_date', 'gender',
                      'phone_number', 'phone_number_alt', 'email',
                      'street_address', 'city', 'province', 'country', 'postal_code',
                      'ec_first_name', 'ec_middle_name', 'ec_last_name', 'ec_phone_number',
                      'physician', 'points', 'password_flag', 'preferences', 'notes'])
    rm_fields_display.extend(['username', 'first_name', 'middle_name', 'last_name', 'birth_date', 'gender',
                              'phone_number', 'phone_number_alt', 'email',
                              'street_address', 'city', 'province', 'country', 'postal_code',
                              'physician', 'points'])
    rm_fields_filter.extend(['username', 'first_name', 'last_name', 'birth_date', 'gender',
                             'city', 'province', 'country', 'postal_code',
                             'physician', 'points'])
    rm_fields_search.extend(['username', 'first_name', 'last_name', 'birth_date', 'gender',
                             'phone_number', 'phone_number_alt', 'email',
                             'street_address', 'city', 'province', 'country', 'postal_code',
                             'physician', 'points'])
    rm_fields_serialize = rm_fields.copy()

    class GenderType(models.TextChoices):
        Male = 'M', _('Male')
        Female = 'F', _('Female')
        Other = 'O', _('Other')

    username = models.CharField(max_length=40, blank=False, unique=True, help_text="The name a user will log in with.")

    first_name = models.CharField(max_length=40, blank=False)
    middle_name = models.CharField(max_length=40, null=False, blank=True)
    last_name = models.CharField(max_length=40, blank=False)  # db_index=True

    birth_date = models.DateField(null=False)
    gender = models.CharField(max_length=1, blank=False, choices=GenderType.choices)

    phone_number = models.CharField(max_length=40, blank=False)
    phone_number_alt = models.CharField(max_length=40, null=False, blank=True)
    email = models.EmailField(blank=False, help_text="The email address for a user.") #, unique=True

    street_address = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=100, blank=False)
    province = models.CharField(max_length=100, blank=False)
    country = models.CharField(max_length=100, blank=False)
    postal_code = models.CharField(max_length=10, blank=False) # Abstract into an address object?

    ec_first_name = models.CharField(max_length=40, null=False, blank=True)
    ec_middle_name = models.CharField(max_length=40, null=False, blank=True)
    ec_last_name = models.CharField(max_length=40, null=False, blank=True)
    ec_phone_number = models.CharField(max_length=40, null=False, blank=True)

    physician = models.CharField(max_length=40, null=False, blank=True)
    points = models.BigIntegerField(null=False, verbose_name="Health Currency", default=0)  # Int or Decimal?

    personal_message = models.CharField(max_length=280, blank=True, null=False)
    picture = models.ImageField(upload_to='profile_pictures/', blank=True)

    password_flag = models.BooleanField(null=False, verbose_name="Password Reset Flag",
                                        help_text="True if the password needs to be reset.", default=True)

    preferences = models.TextField(blank=False, help_text="This should be a JSON.", default="{}")
    notes = models.TextField(blank=True, null=False)

    def __str__(self):
        if len(self.middle_name) > 0:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"

class Cohort(ModelMore):
    rm_fields: list = ModelMore.rm_fields.copy()
    rm_fields_display: list = ModelMore.rm_fields.copy()
    rm_fields_filter: list = ModelMore.rm_fields.copy()
    rm_fields_search: list = ModelMore.rm_fields.copy()
    rm_fields_serialize: list = ModelMore.rm_fields.copy()
    rm_fields_foreign: list = ['clients']

    rm_fields.extend(['type', 'data'])
    rm_fields_display.extend(['type'])
    rm_fields_filter.extend(['type'])
    rm_fields_search.extend(['type'])
    rm_fields_serialize.extend(['type', 'data'])

    class CohortType(models.TextChoices):
        Male = 'PLM', _('Pulminary')
        Female = 'CRD', _('Cardiac')

    type = models.CharField(max_length=3, blank=False, choices=CohortType.choices)

    clients = models.ManyToManyField('Client', db_table='cohort_membership')

    data = models.TextField(blank=False, help_text="This should be a JSON.", default="{}")


class Form(ModelProcessable):
    rm_fields: list = ModelProcessable.rm_fields.copy()
    rm_fields_display: list = ModelProcessable.rm_fields.copy()
    rm_fields_filter: list = ModelProcessable.rm_fields.copy()
    rm_fields_search: list = ModelProcessable.rm_fields.copy()
    rm_fields_serialize: list = ModelProcessable.rm_fields.copy()

    rm_fields.extend(['type', 'display'])
    rm_fields_display.extend(['type'])
    rm_fields_filter.extend(['type'])
    rm_fields_search.extend(['type'])
    rm_fields_serialize.extend(['type', 'display'])

    class FormType(models.TextChoices):
        UNKNOWN = '?', _('Unknown')
        SURVEY = 'S', _('Survey')
        MEDICAL_TEST = 'M', _('Medical Test')
        DIETARY_JOURNAL = 'D', _('Dietary Journal Entry')

    type = models.CharField(max_length=40, blank=False, choices=FormType.choices, default=FormType.UNKNOWN)

    display = models.TextField(blank=False, help_text="This should be a JSON.")


class Submission(ModelBase):
    rm_fields: list = ModelBase.rm_fields.copy()
    rm_fields_display: list = ModelBase.rm_fields.copy()
    rm_fields_filter: list = ModelBase.rm_fields.copy()
    rm_fields_search: list = ModelBase.rm_fields.copy()
    rm_fields_serialize: list = ModelBase.rm_fields.copy()
    rm_fields_foreign: list = ['client', 'form']

    rm_fields.extend(['time', 'values', 'notes'])
    rm_fields_display.extend(['time'])
    rm_fields_filter.extend(['time'])
    rm_fields_search.extend(['time'])
    rm_fields_serialize.extend(['time', 'values', 'notes'])

    client = models.ForeignKey('Client', on_delete=models.CASCADE, null=False)  # related_name='+'
    form = models.ForeignKey('Form', on_delete=models.SET_NULL, null=True)

    time = models.DateTimeField(null=False)
    values = models.TextField(blank=False, help_text="This should be a JSON.")

    notes = models.TextField(blank=True, null=False)

    def __str__(self):
        return f"{self.form.name} by {str(self.client)} for {self.time}"


class Indicator(AbstractIndicator):
    rm_fields: list = AbstractIndicator.rm_fields.copy()
    rm_fields_display: list = AbstractIndicator.rm_fields.copy()
    rm_fields_filter: list = AbstractIndicator.rm_fields.copy()
    rm_fields_search: list = AbstractIndicator.rm_fields.copy()
    rm_fields_serialize: list = AbstractIndicator.rm_fields.copy()


class DataPoint(AbstractDataPoint):
    rm_fields: list = AbstractDataPoint.rm_fields.copy()
    rm_fields_display: list = AbstractDataPoint.rm_fields.copy()
    rm_fields_filter: list = AbstractDataPoint.rm_fields.copy()
    rm_fields_search: list = AbstractDataPoint.rm_fields.copy()
    rm_fields_serialize: list = AbstractDataPoint.rm_fields.copy()
    rm_fields_foreign: list = ['client', 'indicator']

    client = models.ForeignKey('Client', on_delete=models.CASCADE, null=False)  # related_name='+'
    indicator = models.ForeignKey('Indicator', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.indicator.name} by {str(self.client)} for {self.time}"


class Goal(ModelBase):
    rm_fields: list = ModelBase.rm_fields.copy()
    rm_fields_display: list = ModelBase.rm_fields.copy()
    rm_fields_filter: list = ModelBase.rm_fields.copy()
    rm_fields_search: list = ModelBase.rm_fields.copy()
    rm_fields_serialize: list = ModelBase.rm_fields.copy()
    rm_fields_foreign: list = ['client', 'indicator']

    rm_fields.extend(['start', 'target', 'completed', 'notes'])
    rm_fields_display.extend(['start', 'completed'])
    rm_fields_filter.extend(['start', 'completed'])
    rm_fields_search.extend(['start', 'completed'])
    rm_fields_serialize.extend(['start', 'target', 'completed', 'notes'])

    start = models.DateTimeField(null=False)
    target = models.TextField(blank=False, help_text="This should be a JSON.")

    client = models.ForeignKey('Client', on_delete=models.CASCADE, null=False)  # related_name='+'
    indicator = models.ForeignKey('Indicator', on_delete=models.SET_NULL, null=True)

    completed = models.BooleanField(null=False, default=False)

    notes = models.TextField(blank=True, null=False)

    def __str__(self):
        return f"{self.indicator.name} Goal for {str(self.client)}"


class AnonymizedIndicator(AbstractIndicator):
    rm_fields: list = AbstractIndicator.rm_fields.copy()
    rm_fields_display: list = AbstractIndicator.rm_fields.copy()
    rm_fields_filter: list = AbstractIndicator.rm_fields.copy()
    rm_fields_search: list = AbstractIndicator.rm_fields.copy()
    rm_fields_serialize: list = AbstractIndicator.rm_fields.copy()
    rm_fields_foreign: list = ['indicator']

    rm_fields.extend(['anonmization'])
    rm_fields_serialize.extend(['anonmization'])

    indicator = models.ForeignKey('Indicator', on_delete=models.SET_NULL, null=True)

    anonmization = models.TextField(blank=False, help_text="This should be a JSON.")


class CohortDataPoint(AbstractDataPoint):
    rm_fields: list = AbstractDataPoint.rm_fields.copy()
    rm_fields_display: list = AbstractDataPoint.rm_fields.copy()
    rm_fields_filter: list = AbstractDataPoint.rm_fields.copy()
    rm_fields_search: list = AbstractDataPoint.rm_fields.copy()
    rm_fields_serialize: list = AbstractDataPoint.rm_fields.copy()
    rm_fields_foreign: list = ['cohort', 'a_indicator']

    rm_fields.extend(['a_client_id'])
    rm_fields_serialize.extend(['a_client_id'])

    cohort = models.ForeignKey('Cohort', on_delete=models.CASCADE, null=False)  # related_name='+'
    a_indicator = models.ForeignKey('AnonymizedIndicator', on_delete=models.SET_NULL, null=True)

    a_client_id = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.a_indicator.name} in {str(self.cohort)} for {self.time}"
