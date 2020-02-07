from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

# This class is just a helper for dealing with some Django features quickly during development
# and will at some point be removed. Please ignore.
from rest_framework.exceptions import ValidationError
from rest_framework.utils import json


class ModelHelper:
    model_fields: dict = {}
    model_sorts: dict = {}
    model_displays: dict = {}
    model_filter_ons: dict = {}
    model_search_ons: dict = {}
    model_do_not_serializes: dict = {}
    model_text_types: dict = {}
    model_foreigns: dict = {}

    admin_to_register: list = []

    dicts = [model_fields, model_sorts, model_displays, model_filter_ons, model_search_ons, model_do_not_serializes,
             model_text_types, model_foreigns]

    @classmethod
    def inherit(cls, parent, child):
        for d in cls.dicts:
            if parent in d.keys():
                d[child] = d[parent].copy()
            else:
                if d is cls.model_fields:
                    d[child] = []
                else:
                    d[child] = {}

    @classmethod
    def get_(cls, dic: dict, key):
        if key not in dic.keys():
            if dic is cls.model_fields:
                dic[key] = []
            else:
                dic[key] = {}
        return dic[key]

    @classmethod
    def register(cls, model, field, priority, to_display=True, to_filter=False, to_search=False, to_serialize=True,
                 text_type=None, foreign=None):
        model_fields: list = cls.get_(cls.model_fields, model)
        model_sorts: dict = cls.get_(cls.model_sorts, model)
        model_displays: dict = cls.get_(cls.model_displays, model)
        model_filter_ons: dict = cls.get_(cls.model_filter_ons, model)
        model_search_ons: dict = cls.get_(cls.model_search_ons, model)
        model_do_not_serializes: dict = cls.get_(cls.model_do_not_serializes, model)
        model_text_types: dict = cls.get_(cls.model_text_types, model)
        model_foreigns: dict = cls.get_(cls.model_foreigns, model)

        model_fields.append(field)
        model_sorts[field] = priority
        model_displays[field] = to_display
        model_filter_ons[field] = to_filter
        model_search_ons[field] = to_search
        model_do_not_serializes[field] = not to_serialize
        model_text_types[field] = text_type
        model_foreigns[field] = foreign

    @classmethod
    def to_admin(cls, model):
        cls.admin_to_register.append(model)

    @classmethod
    def serialize(cls, model):
        if not isinstance(model, str):
            key = model.__name__
        else:
            key = model

        model_fields: list = cls.get_(cls.model_fields, key)
        model_sorts: dict = cls.get_(cls.model_sorts, key)
        model_do_not_serializes: dict = cls.get_(cls.model_do_not_serializes, key)
        model_text_types: dict = cls.get_(cls.model_text_types, key)
        model_foreigns: dict = cls.get_(cls.model_foreigns, key)

        temp = [f for f in model_fields if not model_do_not_serializes[f]]

        temp.sort(key=lambda x: -model_sorts[x])

        return temp


class Text(models.Model):
    _name = 'Text'  # internal name

    id = models.BigAutoField(editable=False, primary_key=True)
    value = models.TextField(blank=False, help_text="The English value.")

    def __str__(self):
        return self.value[0:min(len(self.value), 12)] + ("" if len(self.value) < 15 else "...") + f" ({self.id})"

    # Used with views and serializers
    ModelHelper.register(_name, 'id', 100, to_serialize=False, to_search=True)
    ModelHelper.register(_name, 'value', 75, to_search=True)


class String(models.Model):
    _name = 'String'  # internal name

    id = models.BigAutoField(editable=False, primary_key=True)
    value = models.CharField(max_length=100, blank=False, help_text="The English value.")

    def __str__(self):
        return self.value + f" ({self.id})"

    # Used with views and serializers
    ModelHelper.register(_name, 'id', 100, to_serialize=False, to_search=True)
    ModelHelper.register(_name, 'value', 75, to_search=True)


class StringGroup(models.Model):
    _name = 'StringGroup'  # internal name

    id = models.BigAutoField(editable=False, primary_key=True)
    values = models.TextField(blank=False, help_text="The English values in a JSON.")

    def __str__(self):
        return self.values + f" ({self.id})"

    # Used with views and serializers
    ModelHelper.register(_name, 'id', 100, to_serialize=False, to_search=True)
    ModelHelper.register(_name, 'values', 75, to_search=True, text_type='JSON')


class ModelBase(models.Model):
    _name = 'ModelBase'  # internal name

    id = models.BigAutoField(editable=False, primary_key=True)

    # This is here to provide a flexible way to annotate entries in the future, as may be required.
    flags = models.TextField(blank=False, help_text="This field is here as a stopgap measure for any extra information "
                                                    + "that needs to be noted with an entry. This should be a JSON.",
                             default="{}")

    creation_time = models.DateTimeField(auto_now_add=True, null=False)
    update_time = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        abstract = True

    # Used with views and serializers
    ModelHelper.register(_name, 'id', 100, to_serialize=False, to_search=True)
    ModelHelper.register(_name, 'flags', 25, False, to_serialize=False, to_search=True, text_type='JSON')
    ModelHelper.register(_name, 'creation_time', 5, to_filter=True, to_serialize=False)
    ModelHelper.register(_name, 'update_time', 5, to_filter=True, to_serialize=False)


class Profile(ModelBase):
    _name = 'Profile'  # internal name
    _parent = 'ModelBase'  # internal name

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class GenderType(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        OTHER = 'O', _('Other')  # This will require a more detailed translation solution...
        NOT_DISCLOSED = 'N', _('Prefer Not To Disclose')

    first_name = models.CharField(max_length=40, blank=False)
    middle_name = models.CharField(max_length=40, null=False, blank=True, verbose_name="Middle Name(s)")
    last_name = models.CharField(max_length=40, blank=False, db_index=True)

    date_of_birth = models.DateField(null=False, db_index=True)
    gender = models.CharField(max_length=1, blank=False, choices=GenderType.choices)

    phone_number = models.CharField(max_length=40, blank=False, help_text="The primary contact number.", db_index=True)
    phone_number_alt = models.CharField(max_length=40, null=False, blank=True,
                                        help_text="A secondary contact number.",
                                        verbose_name="Alternate Phone Number")
    email = models.EmailField(blank=False, help_text="The contact email address.")

    # Abstract into an address object?
    street_address = models.CharField(max_length=200, blank=False)
    city = models.CharField(max_length=100, blank=False)
    province = models.CharField(max_length=50, blank=False)
    country = models.CharField(max_length=25, blank=False)
    postal_code = models.CharField(max_length=10, blank=False, db_index=True)

    ec_first_name = models.CharField(max_length=40, null=False, blank=True,
                                     verbose_name="Emergency Contact First Name")
    ec_middle_name = models.CharField(max_length=40, null=False, blank=True,
                                      verbose_name="Emergency Contact Middle Name(s)")
    ec_last_name = models.CharField(max_length=40, null=False, blank=True, verbose_name="Emergency Contact Last Name")
    ec_phone_number = models.CharField(max_length=40, null=False, blank=True,
                                       verbose_name="Emergency Contact Phone Number")

    physician = models.CharField(max_length=40, null=False, blank=True)

    points = models.BigIntegerField(null=False, verbose_name="Health Currency", default=0)  # Int or Decimal?
    personal_message = models.CharField(max_length=280, blank=True, null=False)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)

    password_flag = models.BooleanField(null=False, verbose_name="Password Reset Flag",
                                        help_text="True if the password needs to be reset.", default=True)

    # To be used to store any user based preference information required.
    preferences = models.TextField(blank=False, default="{}",
                                   help_text="This should be a JSON containing user preference information.")

    # To be used by administrators to annotate user accounts.
    notes = models.TextField(blank=True, null=False)

    def __str__(self):
        if len(self.middle_name) > 0:
            return f"{self.first_name} {self.middle_name} {self.last_name} {self.id}"
        else:
            return f"{self.first_name} {self.last_name} {self.id}"

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'user', 99, to_search=True, foreign=User)
    ModelHelper.register(_name, 'first_name', 80, to_filter=True, to_search=True)
    ModelHelper.register(_name, 'middle_name', 80)
    ModelHelper.register(_name, 'last_name', 80, to_filter=True, to_search=True)
    ModelHelper.register(_name, 'date_of_birth', 75, to_filter=True, to_search=True)
    ModelHelper.register(_name, 'gender', 75, to_filter=True)
    ModelHelper.register(_name, 'phone_number', 70, to_search=True)
    ModelHelper.register(_name, 'phone_number_alt', 70)
    ModelHelper.register(_name, 'email', 70, to_search=True)
    ModelHelper.register(_name, 'street_address', 70, to_search=True)
    ModelHelper.register(_name, 'city', 70, to_search=True)
    ModelHelper.register(_name, 'province', 70)
    ModelHelper.register(_name, 'country', 70)
    ModelHelper.register(_name, 'postal_code', 70)
    ModelHelper.register(_name, 'ec_first_name', 65)
    ModelHelper.register(_name, 'ec_middle_name', 65)
    ModelHelper.register(_name, 'ec_last_name', 65)
    ModelHelper.register(_name, 'ec_phone_number', 65)
    ModelHelper.register(_name, 'physician', 65)
    ModelHelper.register(_name, 'points', 50)
    ModelHelper.register(_name, 'personal_message', 50)
    ModelHelper.register(_name, 'profile_picture', 50, False)
    ModelHelper.register(_name, 'points', 50)
    ModelHelper.register(_name, 'password_flag', 40, False)
    ModelHelper.register(_name, 'preferences', 28, False)
    ModelHelper.register(_name, 'notes', 30, to_serialize=False)

    def submissions(self):
        return Submission.objects.filter(user=self.user)

    def completed_forms(self, form_id):
        return Submission.objects.filter(user=self.user, form__id=form_id)

    def completed_surveys(self, survey_id):
        return Submission.objects.filter(user=self.user, form__surveys__id=survey_id)


class Nameable(ModelBase):
    _name = 'Nameable'  # internal name
    _parent = 'ModelBase'  # internal name

    name = models.ForeignKey(String, on_delete=models.SET_NULL, null=True,  # related_name='strings',
                             help_text="The name of this entry.")
    description = models.ForeignKey(Text, on_delete=models.SET_NULL, null=True,  # related_name='texts',
                                    help_text="The description of this entry.")

    notes = models.TextField(blank=True, null=False, help_text="The notes associated with this entry.")

    class Meta:
        abstract = True

    def __str__(self):
        return self.name.value + f" ({self.id})"

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'name', 85, to_filter=True, to_search=True, foreign=String)
    ModelHelper.register(_name, 'description', 35, foreign=Text)
    ModelHelper.register(_name, 'notes', 30, to_serialize=False)


class Processable(Nameable):
    _name = 'Processable'  # internal name
    _parent = 'Nameable'  # internal name

    # This will be used by the data validation subsystem
    specification = models.TextField(blank=False, default="{}",
                                     help_text="This should be a JSON containing a specification of this entry.")

    # This will be used by the data analysis/processing subsystems
    analysis = models.TextField(blank=False, default="{}",
                                help_text="This should be a JSON containing the analysis hooks for this entry.")

    class Meta:
        abstract = True

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'specification', 27, False, to_serialize=False, text_type='JSON')
    ModelHelper.register(_name, 'analysis', 27, False, to_serialize=False, text_type='JSON')


class Displayable(Processable):
    _name = 'Displayable'  # internal name
    _parent = 'Processable'  # internal name

    # This will be used to store any information required for display
    display = models.TextField(blank=False, help_text="This should be a JSON of information used by the front end.",
                               default={})

    class Meta:
        abstract = True

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'display', 27, False, text_type='JSON')


class Form(Displayable):
    _name = 'Form'  # internal name
    _parent = 'Displayable'  # internal name

    class FormType(models.TextChoices):
        UNKNOWN = '?', _('Unknown')
        SURVEY = 'S', _('Survey')
        MEDICAL_TEST = 'M', _('Medical Test')
        DIETARY_JOURNAL = 'D', _('Dietary Journal Entry')

    type = models.CharField(max_length=1, blank=False, choices=FormType.choices, default=FormType.UNKNOWN)

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'type', 85, to_filter=True, to_search=True)

    @staticmethod
    def all_surveys():
        return Form.objects.filter(type=Form.FormType.SURVEY.value)

    def get_survey(self):
        if self.type is not Form.FormType.SURVEY.value:
            return None

        return Survey.objects.get(form=self.pk)


class Survey(ModelBase):
    _name = 'Survey'  # internal name
    _parent = 'ModelBase'  # internal name

    form = models.OneToOneField(Form, on_delete=models.SET_NULL, null=True, related_name='surveys')

    def __str__(self):
        return str(self.form.name) + f" ({self.id})"

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'form', 85, to_serialize=False, foreign=Form)


class FormElement(Displayable):
    _name = 'FormElement'  # internal name
    _parent = 'Displayable'  # internal name

    # Element order in form
    number = models.IntegerField(null=False)

    class Meta:
        abstract = True

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'number', 80)


class TextElement(FormElement):
    _name = 'TextElement'  # internal name
    _parent = 'FormElement'  # internal name

    # can't inherit
    form = models.ForeignKey(Form, on_delete=models.SET_NULL, null=True, related_name='text_elements', db_index=True)

    text = models.ForeignKey(Text, on_delete=models.SET_NULL, null=True, related_name='text_elements',
                             help_text="The text of this text element.")

    class Meta:
        unique_together = (('form', 'number'),)
        index_together = (('form', 'number'),)

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'form', 85, to_serialize=False, foreign=Form)
    ModelHelper.register(_name, 'text', 75, foreign=Text)


class QuestionGroup(FormElement):
    _name = 'QuestionGroup'  # internal name
    _parent = 'FormElement'  # internal name

    class DataType(models.TextChoices):
        UNKNOWN = '?', _('Unknown')
        TEXT = 'T', _('Text')
        INT = 'I', _('Integer')
        FLOAT = 'D', _('Decimal')
        INT_RANGE = 'R', _('Integer Range')
        BOOLEAN = 'B', _('Boolean')
        EXCLUSIVE = 'X', _('Exclusive Choices')
        CHOICES = 'M', _('Multiple Choices')
        FLOAT_RANGE = 'S', _('Decimal Range')

    class ResponseType(models.TextChoices):
        UNKNOWN = '?', _('Unknown')
        TEXT = 'T', _('Text')
        INT = 'I', _('Integer')
        FLOAT = 'D', _('Decimal')

    type = models.CharField(max_length=1, blank=False, choices=DataType.choices, default=DataType.UNKNOWN)

    # can't inherit
    form = models.ForeignKey(Form, on_delete=models.SET_NULL, null=True, related_name='question_groups',
                             db_index=True)

    text = models.ForeignKey(Text, on_delete=models.SET_NULL, null=True, related_name='question_groups',
                             help_text="The text of this question group.")

    # Used for units, format hints, etc.
    annotations = models.ForeignKey(StringGroup, on_delete=models.SET_NULL, null=True, related_name='question_groups',
                                    help_text="The annotation of this question group.", default="{}")

    class Meta:
        unique_together = (('form', 'number'),)
        index_together = (('form', 'number'),)

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'type', 85, to_filter=True, to_search=True)
    ModelHelper.register(_name, 'form', 85, to_serialize=False, foreign=Form)
    ModelHelper.register(_name, 'text', 75, foreign=Text)
    ModelHelper.register(_name, 'annotations', 70)

    def questions(self):
        return Question.objects.filter(group=self.pk)

    @staticmethod
    def data_classes() -> list:
        return [TextQuestion, IntQuestion, FloatQuestion, IntRangeQuestion, BooleanChoiceQuestion,
                ExclusiveChoiceQuestion, MultiChoiceQuestion, FloatRangeQuestion]

    @staticmethod
    def data_class_of(type):
        if type is QuestionGroup.DataType.TEXT.value:
            return TextQuestion
        elif type is QuestionGroup.DataType.INT.value:
            return IntQuestion
        elif type is QuestionGroup.DataType.FLOAT.value:
            return FloatQuestion
        elif type is QuestionGroup.DataType.INT_RANGE.value:
            return IntRangeQuestion
        elif type is QuestionGroup.DataType.BOOLEAN.value:
            return BooleanChoiceQuestion
        elif type is QuestionGroup.DataType.EXCLUSIVE.value:
            return ExclusiveChoiceQuestion
        elif type is QuestionGroup.DataType.CHOICES.value:
            return MultiChoiceQuestion
        elif type is QuestionGroup.DataType.FLOAT_RANGE.value:
            return FloatRangeQuestion

    def data_class(self):
        if self.type is QuestionGroup.DataType.TEXT.value:
            return TextQuestion
        elif self.type is QuestionGroup.DataType.INT.value:
            return IntQuestion
        elif self.type is QuestionGroup.DataType.FLOAT.value:
            return FloatQuestion
        elif self.type is QuestionGroup.DataType.INT_RANGE.value:
            return IntRangeQuestion
        elif self.type is QuestionGroup.DataType.BOOLEAN.value:
            return BooleanChoiceQuestion
        elif self.type is QuestionGroup.DataType.EXCLUSIVE.value:
            return ExclusiveChoiceQuestion
        elif self.type is QuestionGroup.DataType.CHOICES.value:
            return MultiChoiceQuestion
        elif self.type is QuestionGroup.DataType.FLOAT_RANGE.value:
            return FloatRangeQuestion

    def response_type(self):
        if self.type is QuestionGroup.DataType.TEXT.value:
            return self.ResponseType.TEXT
        elif self.type in [QuestionGroup.DataType.INT.value, QuestionGroup.DataType.INT_RANGE.value,
                           QuestionGroup.DataType.BOOLEAN.value, QuestionGroup.DataType.EXCLUSIVE.value,
                           QuestionGroup.DataType.CHOICES.value]:
            return self.ResponseType.INT
        elif self.type in [QuestionGroup.DataType.FLOAT.value, QuestionGroup.DataType.FLOAT_RANGE.value]:
            return FloatQuestion

    def data(self) -> 'QuestionType':
        return self.data_class().objects.get(group=self.pk)


class Question(Displayable):
    _name = 'Question'  # internal name
    _parent = 'Displayable'  # internal name

    # QuestionGroup order in question
    number = models.IntegerField(null=False)
    optional = models.BooleanField(null=False, default=False)

    group = models.ForeignKey(QuestionGroup, on_delete=models.SET_NULL, null=True,
                              related_name='inputs', db_index=True)

    text = models.ForeignKey(Text, on_delete=models.SET_NULL, null=True, related_name='questions',
                             help_text="The text of this question.")

    # Used for units, format hints, etc.
    annotations = models.ForeignKey(StringGroup, on_delete=models.SET_NULL, null=True, related_name='questions',
                                    help_text="The annotation of this question.", default={})

    class Meta:
        unique_together = (('group', 'number'),)
        index_together = (('group', 'number'),)

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'group', 85, to_serialize=False, foreign=QuestionGroup)
    ModelHelper.register(_name, 'number', 80)
    ModelHelper.register(_name, 'text', 75, foreign=Text)
    ModelHelper.register(_name, 'annotations', 70)
    ModelHelper.register(_name, 'optional', 65, )


class QuestionType(ModelBase):
    _name = 'QuestionType'  # internal name
    _parent = 'ModelBase'  # internal name

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self._name} data for {str(self.group)}"

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)


class SingleInputQuestion(QuestionType):
    _name = 'SingleInputQuestion'  # internal name
    _parent = 'QuestionType'  # internal name

    class Meta:
        abstract = True

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)


class TextQuestion(SingleInputQuestion):
    _name = 'TextQuestion'  # internal name
    _parent = 'SingleInputQuestion'  # internal name

    min_length = models.IntegerField(null=False)
    max_length = models.IntegerField(null=False)

    # Can't inherit
    group = models.OneToOneField(QuestionGroup, on_delete=models.SET_NULL, null=True,
                                 related_name='text_group', db_index=True)

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'group', 85, to_serialize=False, foreign=QuestionGroup)
    ModelHelper.register(_name, 'min_length', 75, to_filter=True)
    ModelHelper.register(_name, 'max_length', 75, to_filter=True)

    def validate(self, value: str) -> bool:
        return self.min_length < len(value) < self.max_length


class IntQuestion(SingleInputQuestion):
    _name = 'IntQuestion'  # internal name
    _parent = 'SingleInputQuestion'  # internal name

    min = models.IntegerField(null=False)
    max = models.IntegerField(null=False)

    # Can't inherit
    group = models.OneToOneField(QuestionGroup, on_delete=models.SET_NULL, null=True,
                                 related_name='int_group', db_index=True)

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'group', 85, to_serialize=False, foreign=QuestionGroup)
    ModelHelper.register(_name, 'min_length', 75, to_filter=True)
    ModelHelper.register(_name, 'max_length', 75, to_filter=True)
    ModelHelper.register(_name, 'min', 75, to_filter=True)
    ModelHelper.register(_name, 'max', 75, to_filter=True)

    def validate(self, value: int) -> bool:
        return self.min < value < self.max


class FloatQuestion(SingleInputQuestion):
    _name = 'FloatQuestion'  # internal name
    _parent = 'SingleInputQuestion'  # internal name

    min = models.FloatField(null=False)
    max = models.FloatField(null=False)

    # Can't inherit
    group = models.OneToOneField(QuestionGroup, on_delete=models.SET_NULL, null=True,
                                 related_name='float_group', db_index=True)

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'group', 85, to_serialize=False, foreign=QuestionGroup)
    ModelHelper.register(_name, 'min_length', 75, to_filter=True)
    ModelHelper.register(_name, 'max_length', 75, to_filter=True)
    ModelHelper.register(_name, 'min', 75, to_filter=True)
    ModelHelper.register(_name, 'max', 75, to_filter=True)

    def validate(self, value: float) -> bool:
        return self.min < value < self.max


class FiniteChoiceQuestion(QuestionType):
    _name = 'FiniteChoiceQuestion'  # internal name
    _parent = 'QuestionType'  # internal name

    num_possibilities = models.IntegerField(null=False)
    initial = models.IntegerField(null=False)

    class Meta:
        abstract = True

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'num_possibilities', 75, to_filter=True)
    ModelHelper.register(_name, 'initial', 75, to_filter=True)


class IntRangeQuestion(FiniteChoiceQuestion):
    _name = 'IntRangeQuestion'  # internal name
    _parent = 'FiniteChoiceQuestion'  # internal name

    min = models.IntegerField(null=False)
    max = models.IntegerField(null=False)
    step = models.IntegerField(null=False, default=1)

    labels = models.ForeignKey(StringGroup, on_delete=models.SET_NULL, null=True, related_name='int_range_questions',
                               help_text="The labels of this question's categories.")

    # Can't inherit
    group = models.OneToOneField(QuestionGroup, on_delete=models.SET_NULL, null=True,
                                 related_name='int_range_group', db_index=True)

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'group', 85, to_serialize=False, foreign=QuestionGroup)
    ModelHelper.register(_name, 'labels', 70, text_type='JSON', foreign=StringGroup)
    ModelHelper.register(_name, 'min', 75, to_filter=True)
    ModelHelper.register(_name, 'max', 75, to_filter=True)
    ModelHelper.register(_name, 'step', 75, to_filter=True)

    def validate(self, value: int) -> bool:
        return self.min < value < self.max \
               and (self.step == 1 or value - self.min % self.step == 0)


class BooleanChoiceQuestion(FiniteChoiceQuestion):
    _name = 'BooleanChoiceQuestion'  # internal name
    _parent = 'FiniteChoiceQuestion'  # internal name

    labels = models.ForeignKey(StringGroup, on_delete=models.SET_NULL, null=True,
                               related_name='boolean_choice_questions',
                               help_text="The labels of this question's categories.")

    # Can't inherit
    group = models.OneToOneField(QuestionGroup, on_delete=models.SET_NULL, null=True,
                                 related_name='boolean_choice_group', db_index=True)

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'group', 85, to_serialize=False, foreign=QuestionGroup)
    ModelHelper.register(_name, 'labels', 70, text_type='JSON', foreign=StringGroup)

    #  This is not very useful but is required to fit the expected interface
    @staticmethod
    def validate(self, value: bool) -> bool:
        return isinstance(value, bool)


class ExclusiveChoiceQuestion(FiniteChoiceQuestion):
    _name = 'ExclusiveChoiceQuestion'  # internal name
    _parent = 'FiniteChoiceQuestion'  # internal name

    labels = models.ForeignKey(StringGroup, on_delete=models.SET_NULL, null=True,
                               related_name='exclusive_choice_questions',
                               help_text="The labels of this question's categories.")

    # Can't inherit
    group = models.OneToOneField(QuestionGroup, on_delete=models.SET_NULL, null=True,
                                 related_name='exclusive_choice_group', db_index=True)

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'group', 85, to_serialize=False, foreign=QuestionGroup)
    ModelHelper.register(_name, 'labels', 70, text_type='JSON', foreign=StringGroup)

    def validate(self, value: int) -> bool:
        return 0 <= value <= self.num_possibilities


class MultiChoiceQuestion(FiniteChoiceQuestion):
    _name = 'MultiChoiceQuestion'  # internal name
    _parent = 'FiniteChoiceQuestion'  # internal name

    min_choices = models.IntegerField(null=False)
    max_choices = models.IntegerField(null=False)

    labels = models.ForeignKey(StringGroup, on_delete=models.SET_NULL, null=True,
                               related_name='multi_choice_questions',
                               help_text="The labels of this question's categories.")

    # Can't inherit
    group = models.OneToOneField(QuestionGroup, on_delete=models.SET_NULL, null=True,
                                 related_name='multi_choice_group', db_index=True)

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'group', 85, to_serialize=False, foreign=QuestionGroup)
    ModelHelper.register(_name, 'labels', 70, text_type='JSON', foreign=StringGroup)
    ModelHelper.register(_name, 'min_choices', 75, to_filter=True)
    ModelHelper.register(_name, 'max_choices', 75, to_filter=True)

    @staticmethod
    def count_bits(bits: int) -> int:
        n: int = bits
        count: int = 0
        while n:
            count += n & 1
            n >>= 1
        return count

    def validate(self, value: int) -> bool:
        if self.min_choices > 0:
            return (0 < value < 2 ** self.max_choices) \
                   and self.count_bits(value) < self.max_choices


class ContinuousChoiceQuestion(QuestionType):
    _name = 'ContinuousChoiceQuestion'  # internal name
    _parent = 'QuestionType'  # internal name

    range = models.FloatField(null=False)
    initial = models.FloatField(null=False)

    class Meta:
        abstract = True

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'range', 75, to_filter=True)
    ModelHelper.register(_name, 'initial', 75, to_filter=True)


class FloatRangeQuestion(ContinuousChoiceQuestion):
    _name = 'FloatRangeQuestion'  # internal name
    _parent = 'FiniteChoiceQuestion'  # internal name

    min = models.FloatField(null=False)
    max = models.FloatField(null=False)

    labels = models.ForeignKey(StringGroup, on_delete=models.SET_NULL, null=True,
                               related_name='float_range_questions',
                               help_text="The labels of this question's categories.")

    # Can't inherit
    group = models.OneToOneField(QuestionGroup, on_delete=models.SET_NULL, null=True,
                                 related_name='float_range_group', db_index=True)

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'group', 85, to_serialize=False, foreign=QuestionGroup)
    ModelHelper.register(_name, 'labels', 70, text_type='JSON', foreign=StringGroup)
    ModelHelper.register(_name, 'min', 75, to_filter=True)
    ModelHelper.register(_name, 'max', 75, to_filter=True)

    def validate(self, value: int) -> bool:
        return self.min < value < self.max


class Submission(ModelBase):
    _name = 'Submission'  # internal name
    _parent = 'ModelBase'  # internal name

    # profile = models.ForeignKey('Profile', on_delete=models.CASCADE, null=False, related_name='submissions')

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='submissions')
    form = models.ForeignKey(Form, on_delete=models.SET_NULL, null=True, related_name='submissions')

    time = models.DateTimeField(null=False)

    raw_data = models.TextField(blank=False, help_text="This should be a JSON.")

    notes = models.TextField(blank=True, null=False)

    def __str__(self):
        return f"{self.form.name} by {str(self.user.profile)} for {self.time}"

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    # ModelHelper.register(_name, 'profile', 85, foreign=Profile)
    ModelHelper.register(_name, 'user', 85, foreign=User)
    ModelHelper.register(_name, 'form', 85, foreign=Form)
    ModelHelper.register(_name, 'time', 75, to_filter=True)
    ModelHelper.register(_name, 'raw_data', 60, False, text_type='JSON')
    ModelHelper.register(_name, 'notes', 30, to_serialize=False)

    def validate(self, data) -> bool:
        decoded = json.load(data)  # TODO


class ResponseType(ModelBase):
    _name = 'ResponseType'  # internal name
    _parent = 'ModelBase'  # internal name

    #  Subclasses must have a question field pointing to their question instance

    left_blank = models.BooleanField(blank=False, default=False)

    class Meta:
        abstract = True

    def __str__(self, name=_name):
        return f"{name} for {str(self.question)} in {str(self.submission)}"

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'left_blank', 40)

    # Delegated
    def validate(self, value: str) -> bool:
        if self.question.group.optional and self.left_blank:
            return False
        elif self.left_blank:
            raise ValidationError(_('Question must be answered.'))
        return self.question.group.data_class().validate(value)


class TextResponse(ResponseType):
    _name = 'TextResponse'  # internal name
    _parent = 'ResponseType'  # internal name

    submission = models.ForeignKey(Submission, on_delete=models.SET_NULL, null=True, related_name='text_responses')

    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True,
                                 related_name='text_responses')

    value = models.TextField(null=False)  # , validators=['validate']

    class Meta:
        unique_together = (('submission', 'question'),)
        index_together = (('submission', 'question'),)

    def __str__(self):
        return super.__str__(self._name)

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'submission', 85, foreign=Submission)
    ModelHelper.register(_name, 'question', 85, foreign=Question)
    ModelHelper.register(_name, 'value', 75, to_filter=True, to_search=True)


class IntResponse(ResponseType):
    _name = 'IntResponse'  # internal name
    _parent = 'ResponseType'  # internal name

    submission = models.ForeignKey(Submission, on_delete=models.SET_NULL, null=True, related_name='int_responses')

    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True,
                                 related_name='int_responses')

    value = models.IntegerField(null=False)

    class Meta:
        unique_together = (('submission', 'question'),)
        index_together = (('submission', 'question'),)

    def __str__(self):
        return super.__str__(self._name)

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'submission', 85, foreign=Submission)
    ModelHelper.register(_name, 'question', 85, foreign=Question)
    ModelHelper.register(_name, 'value', 75, to_filter=True, to_search=True)


class FloatResponse(ResponseType):
    _name = 'FloatResponse'  # internal name
    _parent = 'ResponseType'  # internal name

    submission = models.ForeignKey(Submission, on_delete=models.SET_NULL, null=True, related_name='float_responses')

    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True,
                                 related_name='float_responses')

    value = models.FloatField(null=False)

    class Meta:
        unique_together = (('submission', 'question'),)
        index_together = (('submission', 'question'),)

    def __str__(self):
        return super.__str__(self._name)

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'submission', 85, foreign=Submission)
    ModelHelper.register(_name, 'question', 85, foreign=Question)
    ModelHelper.register(_name, 'value', 75, to_filter=True, to_search=True)

# TODO send messages with validation to explain failure?
# TODO text references should be one to one, but that will complicate testing
