from datetime import datetime
from json import JSONDecodeError

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.utils import json

from Revitalize.data_analysis_system import DataAnalysisSystem


print_debug = False


def validate_json(j: str):
    try:
        return json.loads(j) is not None
    except JSONDecodeError as e:
        raise ValidationError(e)


def pre_validate_json(j: str):
    try:
        return json.loads(j)
    except JSONDecodeError as e:
        raise ValidationError(e)


class LangCode(models.TextChoices):
    UNKNOWN = '?', _('Unknown')
    ENGLISH = 'EN', _('English')


def _str(entry, lang=LangCode.ENGLISH, default=None):
    return entry.value if entry is not None else default


# This class is just a helper for dealing with some Django features quickly during development
# and will at some point be removed. Please ignore.
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

        temp.sort(key=lambda x: model_sorts[x], reverse=True)

        return temp


class String(models.Model):
    _name = 'String'  # internal name

    id = models.BigAutoField(editable=False, primary_key=True)
    value = models.CharField(max_length=100, blank=False, help_text="The English value.")

    def __str__(self):
        return self.value + f" ({self.id})"

    # Delegate to contained string
    def __len__(self):
        return self.value.__len__()

    # Delegate to contained string
    def __getitem__(self, item):
        return self.value.__getitem__(item)

    # Used with views and serializers
    ModelHelper.register(_name, 'id', 100, to_serialize=False, to_search=True)
    ModelHelper.register(_name, 'value', 75, to_search=True)


class Text(models.Model):
    _name = 'Text'  # internal name

    id = models.BigAutoField(editable=False, primary_key=True)
    value = models.TextField(blank=False, help_text="The English value.")

    def __str__(self):
        return self.value[0:min(len(self.value), 12)] + ("" if len(self.value) < 15 else "...") + f" ({self.id})"

    # Delegate to contained string
    def __len__(self):
        return self.value.__len__()

    # Delegate to contained string
    def __getitem__(self, item):
        return self.value.__getitem__(item)

    # Used with views and serializers
    ModelHelper.register(_name, 'id', 100, to_serialize=False, to_search=True)
    ModelHelper.register(_name, 'value', 75, to_search=True)


class StringGroup(models.Model):
    _name = 'StringGroup'  # internal name

    id = models.BigAutoField(editable=False, primary_key=True)
    value = models.TextField(blank=False, help_text="The English values in a JSON.", validators=[validate_json])

    def __str__(self):
        return self.value + f" ({self.id})"

    # Delegate to contained string
    def __len__(self):
        return self.value.__len__()

    # Delegate to contained string
    def __getitem__(self, item):
        return self.value.__getitem__(item)

    # Used with views and serializers
    ModelHelper.register(_name, 'id', 100, to_serialize=False, to_search=True)
    ModelHelper.register(_name, 'value', 75, to_search=True, text_type='JSON')

    @classmethod
    def is_empty(cls, sg: 'StringGroup'):
        if sg is None or len(sg.value) < 3:
            return True

        data = json.loads(sg.value)

        if isinstance(data, dict) and len(data.keys()) < 1 or \
                isinstance(data, list) and len(data) < 1:
            return True

        return False

    @classmethod
    def size(cls, sg: 'StringGroup'):
        if sg is None or len(sg.value) < 3:
            return 0

        data = json.loads(sg.value)

        if isinstance(data, dict):
            return len(data.keys())
        if isinstance(data, list):
            return len(data)

        return -1

    @staticmethod
    def as_structure(value):
        return json.loads(value)




class ModelBase(models.Model):
    _name = 'ModelBase'  # internal name

    id = models.BigAutoField(editable=False, primary_key=True)

    # This is here to provide a flexible way to annotate entries in the future, as may be required.
    flags = models.TextField(blank=False, help_text="This field is here as a stopgap measure for any extra information "
                                                    + "that needs to be noted with an entry. This should be a JSON.",
                             default="{}", validators=[validate_json])

    creation_time = models.DateTimeField(auto_now_add=True, null=False)
    update_time = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        abstract = True

    # Used with views and serializers
    ModelHelper.register(_name, 'id', 100, to_serialize=False, to_search=True)
    ModelHelper.register(_name, 'flags', 10, False, to_serialize=False, to_search=True, text_type='JSON')
    ModelHelper.register(_name, 'creation_time', 5, to_filter=True, to_serialize=False)
    ModelHelper.register(_name, 'update_time', 5, to_filter=True, to_serialize=False)


class Address(ModelBase):
    _name = 'Address'  # internal name
    _parent = 'ModelBase'  # internal name

    class Country(models.TextChoices):
        CANADA = 'CA', _('Canada')

    country = models.CharField(max_length=2, blank=False, choices=Country.choices, default=Country.CANADA)

    def __str__(self):
        return self.address.__str__()

    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'country', 40)


class CanadianAddress(ModelBase):
    _name = 'CanadianAddress'  # internal name
    _parent = 'ModelBase'  # internal name

    base = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='address')

    class Province(models.TextChoices):
        ONTARIO = 'ON', _('Ontario')
        QUEBEC = 'QC', _('Quebec')
        NOVA_SCOTIA = 'NS', _('Nova Scotia')
        NEW_BRUNSWICK = 'NB', _('New Brunswick')
        MANITOBA = 'MB', _('Manitoba')
        BRITISH_COLUMBIA = 'BC', _('British Columbia')
        PRINCE_EDWARD_ISLAND = 'PE', _('Prince Edward Island')
        SASKATCHEWAN = 'SK', _('Saskatchewan')
        ALBERTA = 'AB', _('Alberta')
        NEWFOUNDLAND_AND_LABRADOR = 'NL', _('Newfoundland and Labrador')
        NORTHWEST_TERRITORIES = 'NT', _('Northwest Territories')
        YUKON = 'YT', _('Yukon')
        NUNAVUT = 'NU', _('Nunavut')

    street_address = models.CharField(max_length=250, blank=False)
    city = models.CharField(max_length=125, blank=False)
    province = models.CharField(max_length=50, blank=False, choices=Province.choices)
    postal_code = models.CharField(max_length=6, blank=False, db_index=True)

    def __str__(self):
        return f"{self.street_address} {self.city} {self.province} {self.postal_code} {self.base.country}"

    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'street_address', 58)
    ModelHelper.register(_name, 'city', 56)
    ModelHelper.register(_name, 'province', 54)
    ModelHelper.register(_name, 'postal_code', 52)
    ModelHelper.register(_name, 'base', 50, foreign=Address)


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
    gender = models.CharField(max_length=1, blank=False, choices=GenderType.choices, default=GenderType.NOT_DISCLOSED)

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
    preferences = models.TextField(blank=False, default="{}", validators=[validate_json],
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

    def submission(self, id):
        return Submission.objects.filter(user=self.user, id=id)

    def submissions(self):
        return Submission.objects.filter(user=self.user)

    def all_completed_forms(self):
        return Submission.objects.filter(user=self.user)

    def all_completed_surveys(self):
        return Submission.objects.filter(user=self.user)

    def submitted_forms(self, id):
        return Submission.objects.filter(user=self.user, form__id=id)

    def submitted_surveys(self, id):
        return Submission.objects.filter(user=self.user, form__surveys__id=id)


class Nameable(ModelBase):
    _name = 'Nameable'  # internal name
    _parent = 'ModelBase'  # internal name

    # TODO The on delete should be sorted and the keys may want to be one to one
    name = models.ForeignKey(String, on_delete=models.SET_NULL, null=True,  # related_name='strings',
                             help_text="The name of this entry.")
    description = models.ForeignKey(Text, on_delete=models.SET_NULL, null=True,  # related_name='texts',
                                    help_text="The description of this entry.")

    notes = models.TextField(blank=True, null=False, help_text="The notes associated with this entry.")

    class Meta:
        abstract = True

    def __str__(self):
        return (self.name.value if self.name is not None else "(unnamed)") + f" ({self.id})"

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'name', 85, to_filter=True, to_search=True, foreign=String)
    ModelHelper.register(_name, 'description', 35, foreign=Text)
    ModelHelper.register(_name, 'notes', 30, to_serialize=False)


class Processable(Nameable):
    _name = 'Processable'  # internal name
    _parent = 'Nameable'  # internal name

    # This will be used by the data validation subsystem
    specification = models.TextField(blank=False, default="{}", validators=[validate_json],
                                     help_text="This should be a JSON containing a specification of this entry.")

    # This will be used by the data analysis/processing subsystems
    # It is vitally important that no external input is passed to this JSON as it is impossible to fully prevent
    # certain (obscure) attacks.
    analysis = models.TextField(blank=False, default="{}", validators=[validate_json],
                                help_text="This should be a JSON containing the analysis hooks for this entry.")

    class Meta:
        abstract = True

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'specification', 27, False, to_serialize=False, text_type='JSON')
    ModelHelper.register(_name, 'analysis', 27, False, to_serialize=False, text_type='JSON')

    @staticmethod
    def validate_calculation(calculation: str):
        if calculation is None or not isinstance(calculation, str):
            raise ValidationError("Not a string.")

        if calculation.find('__') != -1:
            raise ValidationError("Calculations may not contain __")

    def analyse(self, user: User, time: datetime, data: dict, source: 'Submission', testing=False):
        analysis: dict = json.loads(self.analysis)

        points = []  # Possibly needed for recursion
        debug = []

        if 'outputs' in analysis.keys():
            for out in analysis['outputs']:
                if not isinstance(out, dict):
                    debug.append(('outputs', out, "Not a dictionary"))
                    continue

                out: dict

                if 'type' not in out.keys():
                    debug.append(('outputs', out, "Unknown type"))
                    continue

                if out['type'] == Indicator.internal_name:

                    if 'calculation' not in out.keys():
                        debug.append(('outputs', out, "No calculation provided"))
                        continue

                    calculation: str = out['calculation']

                    if calculation is None or not isinstance(calculation, str):
                        debug.append(('outputs', out, "Invalid calculation", calculation))
                        continue

                    # This is here to prevent certain types of injections that should never be possible
                    if calculation.find('__'):
                        debug.append(('outputs', out, "Calculations may not contain __", calculation))
                        continue

                    if 'id' not in out.keys():
                        debug.append(('outputs', out, "No indicator id"))
                        continue

                    ind_id = out['id']

                    try:
                        indicator = Indicator.objects.get(id=ind_id)
                        if indicator is None:
                            debug.append(('output_indicators', ind_id, "Indicator not found"))
                            continue

                        # May need dynamic data addition here...

                        value = DataAnalysisSystem.process(calculation, data)

                        if value is None:
                            debug.append(('output_indicators', ind_id, "No value"))
                            continue

                        if not isinstance(value, int) and not isinstance(value, float):
                            debug.append(('output_indicators', ind_id, "Invalid value type", value))
                            continue

                        # This should be unnecessary, but is prudent
                        if indicator.is_int():
                            value = int(value)
                        elif indicator.is_float():
                            value = float(value)

                        valid = indicator.validate(value)

                        if not valid:
                            debug.append(('output_indicators', ind_id, "Value failed to validate", value))
                            continue

                        point = None

                        if testing:
                            time = datetime.today()
                            user = User.objects.get(id=1)

                        if indicator.is_int():
                            point = IntDataPoint.objects.create(indicator=indicator, time=time, value=value,
                                                                validated=True, processed=False,
                                                                user=user, source=source)
                        elif indicator.is_float():
                            point = FloatDataPoint.objects.create(indicator=indicator, time=time, value=value,
                                                                  validated=True, processed=False,
                                                                  user=user, source=source)

                        if point is None:
                            debug.append(('output_indicators', ind_id, "Failed to create point", value))
                            continue

                        points.append(point)

                    except Exception as e:
                        debug.append(('outputs', ind_id, e))

        for p in points:
            p.analyse(user, time, data, source)


class Displayable(Processable):
    _name = 'Displayable'  # internal name
    _parent = 'Processable'  # internal name

    # This will be used to store any information required for display
    display = models.TextField(blank=False, default="{}", validators=[validate_json],
                               help_text="This should be a JSON of information used by the front end.")

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
        MEDICAL_LAB = 'L', _('Medical Lab')
        DIETARY_JOURNAL = 'D', _('Dietary Journal Entry')

    tag = models.CharField(max_length=10, blank=True)

    type = models.CharField(max_length=1, blank=False, choices=FormType.choices, default=FormType.UNKNOWN)

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'tag', 90, to_filter=True, to_search=True)
    ModelHelper.register(_name, 'type', 85, to_filter=True, to_search=True)

    @staticmethod
    def all_surveys():
        return Form.objects.filter(type=Form.FormType.SURVEY.value)

    def is_survey(self):
        return self.type == self.FormType.SURVEY.value

    def is_lab(self):
        return self.type == self.FormType.MEDICAL_LAB.value

    def is_dietary(self):
        return self.type == self.FormType.DIETARY_JOURNAL.value

    def get_survey(self):
        if not self.is_survey():
            return None

        return Survey.objects.get(form=self.pk)

    def get_lab(self):
        if not self.is_lab():
            return None

        return MedicalLab.objects.get(form=self.pk)

    # This is here for now, to be put where it belongs later
    def creation_cascade(self, data):
        if self.is_survey():
            survey = Survey.objects.create(form=self.pk)
        elif self.is_lab():
            lab = MedicalLab.objects.create(form=self.pk)

    def respond(self, data: dict, submission: 'Submission'):
        if print_debug: print(f"respond({data}, {submission})")
        if "elements" not in data.keys():
            raise KeyError("elements")

        groups = self.question_groups.order_by('number').all()

        if print_debug: print(f"\trespond groups: {groups}")

        n = 0
        for e in data["elements"]:
            if not isinstance(e, dict):
                raise TypeError(f"Element #{n} is not a dictionary. {e}")

            e: dict

            if print_debug: print(f"\trespond-#{n} e: {e}")

            if "element_type" not in e.keys():
                raise KeyError(f"Element #{n} is missing a type. {e}")

            if e["element_type"] == QuestionGroup.element_type:
                group: QuestionGroup = None
                bad_id = None

                if print_debug: print(f"\trespond {e['element_type']} == {QuestionGroup.element_type}")

                if "id" in e.keys():
                    group = groups.get(id=e["id"])

                    if group is None:
                        bad_id = e["id"]

                if group is None:
                    group = groups[n]

                if group is None:
                    if bad_id is not None:
                        raise LookupError(f"Unable to find question group #{n} with id {bad_id}")
                    raise LookupError(f"Unable to find question group #{n}")

                if print_debug: print(f"\trespond group {group}")

                group.respond(data, submission, e)
            elif print_debug: print(f"\trespond {e['element_type']} =/= {QuestionGroup.element_type}")
        if print_debug: print(f"/respond")


class Survey(ModelBase):
    _name = 'Survey'  # internal name
    _parent = 'ModelBase'  # internal name

    prefix = models.CharField(max_length=10, blank=True)

    form = models.OneToOneField(Form, on_delete=models.SET_NULL, null=True, related_name='surveys')

    def __str__(self):
        return str(self.form.name) + f" ({self.id})"

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'prefix', 90)
    ModelHelper.register(_name, 'form', 85, to_serialize=False, foreign=Form)


class MedicalLab(ModelBase):
    _name = 'MedicalLab'  # internal name
    _parent = 'ModelBase'  # internal name

    prefix = models.CharField(max_length=10, blank=True)

    form = models.OneToOneField(Form, on_delete=models.SET_NULL, null=True, related_name='labs')

    def __str__(self):
        return str(self.form.name) + f" ({self.id})"

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'prefix', 90)
    ModelHelper.register(_name, 'form', 85, to_serialize=False, foreign=Form)


class FormElement(Displayable):
    _name = 'FormElement'  # internal name
    _parent = 'Displayable'  # internal name

    # Element order in form
    number = models.IntegerField(null=False)

    prefix = models.CharField(max_length=10, blank=True)

    class Meta:
        abstract = True

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'prefix', 90)
    ModelHelper.register(_name, 'number', 80)


class TextElement(FormElement):
    _name = 'TextElement'  # internal name
    _parent = 'FormElement'  # internal name

    element_type = "text"

    # can't inherit
    form = models.ForeignKey(Form, on_delete=models.SET_NULL, null=True, related_name='text_elements', db_index=True)

    text = models.ForeignKey(Text, on_delete=models.SET_NULL, null=True, related_name='text_elements',
                             help_text="The text of this text element.")

    help_text = models.ForeignKey(Text, on_delete=models.SET_NULL, null=True, related_name='text_elements_h',
                                  help_text="The help text of this question.")

    screen_reader_text = models.ForeignKey(Text, on_delete=models.SET_NULL, null=True, related_name='text_elements_sr',
                                           help_text="The screen reader text of this question.")

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

    element_type = "question_group"

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

    # Determined by above
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

    help_text = models.ForeignKey(Text, on_delete=models.SET_NULL, null=True, related_name='question_groups_h',
                                  help_text="The help text of this question group.")

    screen_reader_text = models.ForeignKey(Text, on_delete=models.SET_NULL, null=True,
                                           related_name='question_groups_sr',
                                           help_text="The screen reader text of this question group.")

    internal_name = models.CharField(max_length=10, blank=True)

    # Used for units, format hints, etc.
    annotations = models.ForeignKey(StringGroup, on_delete=models.SET_NULL, null=True,
                                    validators=[validate_json], related_name='question_groups',
                                    help_text="The annotation of this question group.")

    class Meta:
        unique_together = (('form', 'number'),)
        index_together = (('form', 'number'),)

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'type', 85, to_filter=True, to_search=True)
    ModelHelper.register(_name, 'form', 85, to_serialize=False, foreign=Form)
    ModelHelper.register(_name, 'text', 75, foreign=Text)
    ModelHelper.register(_name, 'help_text', 74, foreign=Text)
    ModelHelper.register(_name, 'screen_reader_text', 73, foreign=Text)
    ModelHelper.register(_name, 'annotations', 70)
    ModelHelper.register(_name, 'internal_name', 69)

    def get_questions(self):
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

    @staticmethod
    def response_type_of(type):
        if type is QuestionGroup.DataType.TEXT.value:
            return QuestionGroup.ResponseType.TEXT
        elif type in [QuestionGroup.DataType.INT.value, QuestionGroup.DataType.INT_RANGE.value,
                      QuestionGroup.DataType.BOOLEAN.value, QuestionGroup.DataType.EXCLUSIVE.value,
                      QuestionGroup.DataType.CHOICES.value]:
            return QuestionGroup.ResponseType.INT
        elif type in [QuestionGroup.DataType.FLOAT.value, QuestionGroup.DataType.FLOAT_RANGE.value]:
            return QuestionGroup.ResponseType.FLOAT

    @staticmethod
    def response_class_of(type):
        if type is QuestionGroup.DataType.TEXT.value:
            return TextResponse
        elif type in [QuestionGroup.DataType.INT.value, QuestionGroup.DataType.INT_RANGE.value,
                      QuestionGroup.DataType.BOOLEAN.value, QuestionGroup.DataType.EXCLUSIVE.value,
                      QuestionGroup.DataType.CHOICES.value]:
            return IntResponse
        elif type in [QuestionGroup.DataType.FLOAT.value, QuestionGroup.DataType.FLOAT_RANGE.value]:
            return FloatResponse

    def data_class(self):
        return self.data_class_of(self.type)

    def response_type(self):
        return self.response_type_of(self.type)

    def response_class(self):
        return self.response_class_of(self.type)

    def data(self) -> 'QuestionType':
        return self.data_class().objects.get(group=self.pk)

    def respond(self, submission_data: dict, submission: 'Submission', data: dict):
        if print_debug: print(f"respond({submission_data}, {submission}, {data})")

        if "questions" not in data.keys():
            raise KeyError("questions")

        questions = self.questions.order_by('number').all()

        errors = []
        errored_q = []

        n = 0

        for q in data["questions"]:
            q: dict

            if print_debug: print(f"\trespond q: {q}")

            value = q["value"]

            if print_debug: print(f"\trespond value: {value}")

            try:
                self.data().validate_value(value)

                if print_debug: print(f"\trespond value: valid")

                question: Question = None
                bad_id = None

                if "id" in q.keys():
                    question = questions.get(id=q["id"])

                    if question is None:
                        bad_id = q['id']

                if question is None:
                    question = questions[n]

                if question is None:
                    if bad_id is not None:
                        raise LookupError(f"Unable to find question #{n} with id {bad_id}")
                    raise LookupError(f"Unable to find question #{n}")

                if print_debug: print(f"\trespond question: {question}")

                question.respond(submission, value)

            except (ValidationError, LookupError) as e:
                errors.append(e)
                errored_q.append(q)

            n += 1

        if len(errors) > 0:
            raise ValidationError(errors)

        if print_debug: print(f"/respond")


class Question(Displayable):
    _name = 'Question'  # internal name
    _parent = 'Displayable'  # internal name

    prefix = models.CharField(max_length=10, blank=True)

    # QuestionGroup order in question
    number = models.IntegerField(null=False)
    optional = models.BooleanField(null=False, default=False)

    group = models.ForeignKey(QuestionGroup, on_delete=models.SET_NULL, null=True,
                              related_name='questions', db_index=True)

    text = models.ForeignKey(Text, on_delete=models.SET_NULL, null=True, related_name='questions',
                             help_text="The text of this question.")

    help_text = models.ForeignKey(Text, on_delete=models.SET_NULL, null=True, related_name='questions_h',
                                  help_text="The help text of this question.")

    screen_reader_text = models.ForeignKey(Text, on_delete=models.SET_NULL, null=True, related_name='questions_sr',
                                           help_text="The help text of this question.")

    internal_name = models.CharField(max_length=10, blank=True)

    # Used for units, format hints, etc.
    annotations = models.ForeignKey(StringGroup, on_delete=models.SET_NULL, null=True,
                                    validators=[validate_json], related_name='questions',
                                    help_text="The annotation of this question.")

    class Meta:
        unique_together = (('group', 'number'),)
        index_together = (('group', 'number'),)

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'prefix', 90)
    ModelHelper.register(_name, 'group', 85, to_serialize=False, foreign=QuestionGroup)
    ModelHelper.register(_name, 'number', 80)
    ModelHelper.register(_name, 'text', 75, foreign=Text)
    ModelHelper.register(_name, 'help_text', 74, foreign=Text)
    ModelHelper.register(_name, 'screen_reader_text', 73, foreign=Text)
    ModelHelper.register(_name, 'annotations', 70)
    ModelHelper.register(_name, 'internal_name', 69)
    ModelHelper.register(_name, 'optional', 65, )

    def respond(self, submission: 'Submission', value):
        self.group.response_class().objects.create(submission=submission, question=self, value=value)


class QuestionType(ModelBase):
    _name = 'QuestionType'  # internal name
    _parent = 'ModelBase'  # internal name

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self._name} data for {str(self.group)}"

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)

    def validate_value(self, value):
        raise ValidationError("Not Implemented")


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

    question_group_type = "text"

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

    def validate_value(self, value: str) -> bool:
        return self.min_length < len(value) < self.max_length


class IntQuestion(SingleInputQuestion):
    _name = 'IntQuestion'  # internal name
    _parent = 'SingleInputQuestion'  # internal name

    question_group_type = "integer"

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

    def validate_value(self, value: int) -> bool:
        return self.min < value < self.max


class FloatQuestion(SingleInputQuestion):
    _name = 'FloatQuestion'  # internal name
    _parent = 'SingleInputQuestion'  # internal name

    question_group_type = "decimal"

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

    def validate_value(self, value: float) -> bool:
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

    def default_labels(self):
        return json.dumps([str(n) for n in range(1, self.num_possibilities + 1)])


class IntRangeQuestion(FiniteChoiceQuestion):
    _name = 'IntRangeQuestion'  # internal name
    _parent = 'FiniteChoiceQuestion'  # internal name

    question_group_type = "integer_range"

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

    def validate_value(self, data: int):
        if not isinstance(data, int):
            try:
                value = int(data)
            except ValueError:
                raise ValidationError(_("Expected int, received %(value)") % {"value": value})
        else:
            value = data
        if not (self.min < data < self.max):
            raise ValidationError(_("Value %(value) is out of range: %(min) - %(max)")
                                  % {"value": value, "min": self.min, "max": self.max})
        elif not (self.step == 1 or value - self.min % self.step == 0):
            raise ValidationError(_("Value %(value) is not allowed with step size %(step)")
                                  % {"value": value, "step": self.step})


class BooleanChoiceQuestion(FiniteChoiceQuestion):
    _name = 'BooleanChoiceQuestion'  # internal name
    _parent = 'FiniteChoiceQuestion'  # internal name

    question_group_type = "boolean"
    _default_labels = json.dumps(["yes", "no"])

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
    def validate_value(self, value: bool) -> bool:
        return isinstance(value, bool)

    def default_labels(self):
        return self._default_labels


class ExclusiveChoiceQuestion(FiniteChoiceQuestion):
    _name = 'ExclusiveChoiceQuestion'  # internal name
    _parent = 'FiniteChoiceQuestion'  # internal name

    question_group_type = "exclusive_choices"

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

    def validate_value(self, value: int) -> bool:
        return 0 <= value <= self.num_possibilities


class MultiChoiceQuestion(FiniteChoiceQuestion):
    _name = 'MultiChoiceQuestion'  # internal name
    _parent = 'FiniteChoiceQuestion'  # internal name

    question_group_type = "multi_choices"

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

    def validate_value(self, value: int) -> bool:
        if self.min_choices > 0:
            return (0 < value < 2 ** self.max_choices) \
                   and self.count_bits(value) < self.max_choices

    def validate_value(self, data: float):
        if not isinstance(data, float):
            try:
                value = float(data)
            except ValueError:
                raise ValidationError(_("Expected float, received %(value)") % {"value": value})
        else:
            value = data
        if not (self.min < data < self.max):
            raise ValidationError(_("Value %(value) is out of range: %(min) - %(max)")
                                  % {"value": value, "min": self.min, "max": self.max})


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

    question_group_type = "decimal_range"

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

    def validate_value(self, data: float):
        if not isinstance(data, float):
            try:
                value = float(data)
            except ValueError:
                raise ValidationError(_("Expected float, received %(value)") % {"value": value})
        else:
            value = data
        if not (self.min < data < self.max):
            raise ValidationError(_("Value %(value) is out of range: %(min) - %(max)")
                                  % {"value": value, "min": self.min, "max": self.max})


class Submission(ModelBase):
    _name = 'Submission'  # internal name
    _parent = 'ModelBase'  # internal name

    # profile = models.ForeignKey('Profile', on_delete=models.CASCADE, null=False, related_name='submissions')

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='submissions')
    form = models.ForeignKey(Form, on_delete=models.SET_NULL, null=True, related_name='submissions')
    submitter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='submissions_s')

    time = models.DateTimeField(null=False, db_index=True)

    # Intentionally not validated
    raw_data = models.TextField(blank=False, help_text="This should be a JSON.")

    # Should be set when validated
    validated = models.BooleanField(blank=False, default=False)
    parsed = models.BooleanField(blank=False, default=False)
    processed = models.BooleanField(blank=False, default=False)

    notes = models.TextField(blank=True, null=False)

    def __str__(self):
        return f"{self.form.name} by {str(self.user.profile)} for {self.time}"

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    # ModelHelper.register(_name, 'profile', 85, foreign=Profile)
    ModelHelper.register(_name, 'user', 85, foreign=User)
    ModelHelper.register(_name, 'form', 85, foreign=Form)
    ModelHelper.register(_name, 'submitter', 84, foreign=User)
    ModelHelper.register(_name, 'time', 75, to_filter=True)
    ModelHelper.register(_name, 'raw_data', 60, False, text_type='JSON')
    ModelHelper.register(_name, 'notes', 30, to_serialize=False)
    ModelHelper.register(_name, 'validated', 10, False, to_serialize=False, to_search=True)
    ModelHelper.register(_name, 'parsed', 10, False, to_serialize=False, to_search=True)
    ModelHelper.register(_name, 'processed', 10, False, to_serialize=False, to_search=True)

    def validate(self):
        return json.loads(self.raw_data)
        # TODO
        pass

    def process(self, data=None):
        if print_debug: print(f"process({data})")
        try:
            if data is None:
                data = json.loads(self.raw_data)

            if print_debug: print(f"\tprocess 1")

            self.form.respond(data, self)

            if print_debug: print(f"\tprocess form responded")

            self.form.analyse(self.user, self.time, data, self)

            if print_debug: print(f"\tprocess analysed")

        except Exception as e:
            raise ValueError(f"Unable to parse data ({e})")
        if print_debug: print(f"/process")


class ResponseType(ModelBase):
    _name = 'ResponseType'  # internal name
    _parent = 'ModelBase'  # internal name

    DATA_TAG = "data"

    #  Subclasses must have a question field pointing to their question instance

    left_blank = models.BooleanField(blank=False, default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self._name} for {str(self.question)} in {str(self.submission)}"

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'left_blank', 40)

    def validate_data(self, data: dict) -> bool:
        # In case value passed directly
        if not isinstance(data, dict):
            return self.validate_value(data)

        if self.question.group.optional and self.left_blank:
            return True
        elif self.left_blank:
            raise ValidationError(_("Question not answered."))
        elif self.DATA_TAG not in data.keys():
            raise ValueError(_("No value provided."))
        return self.validate_value(data[self.DATA_TAG])

    def validate_data_return(self, data: dict):
        if self.question.group.optional and self.left_blank:
            return None
        elif self.left_blank:
            raise ValidationError(_("Question not answered."))
        elif self.DATA_TAG not in data.keys():
            raise ValueError(_("No value provided."))
        return self.validate_value_return(data[self.DATA_TAG])

    # Delegated
    def validate_value(self, value) -> bool:
        return self.question.group.data_class().validate_value(value)

    def validate_value_return(self, value):
        return self.question.group.data_class().validate_return(value)

    def parse_response(self, response: dict, optional=False) -> int:
        if not optional and self.DATA_TAG not in response.keys():
            raise ValueError(_("No data value(s) present."))

        value = int(response[self.DATA_TAG])
        if not self.validate(value):
            raise ValidationError(value)
        return value


class TextResponse(ResponseType):
    _name = 'TextResponse'  # internal name
    _parent = 'ResponseType'  # internal name

    submission = models.ForeignKey(Submission, on_delete=models.SET_NULL, null=True, related_name='text_responses')

    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True,
                                 related_name='text_responses')

    value = models.TextField(null=False, validators=[ResponseType.validate_value])

    class Meta:
        unique_together = (('submission', 'question'),)
        index_together = (('submission', 'question'),)

    # Delegate to contained string
    def __len__(self):
        return self.value.__len__()

    # Delegate to contained string
    def __getitem__(self, item):
        return self.value.__getitem__(item)

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

    value = models.IntegerField(null=False, validators=[ResponseType.validate_value])

    class Meta:
        unique_together = (('submission', 'question'),)
        index_together = (('submission', 'question'),)

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

    value = models.FloatField(null=False, validators=[ResponseType.validate_value])

    class Meta:
        unique_together = (('submission', 'question'),)
        index_together = (('submission', 'question'),)

    # Used with views and serializers
    ModelHelper.inherit(_parent, _name)
    ModelHelper.register(_name, 'submission', 85, foreign=Submission)
    ModelHelper.register(_name, 'question', 85, foreign=Question)
    ModelHelper.register(_name, 'value', 75, to_filter=True, to_search=True)


class Indicator(Displayable):
    _name = 'Indicator'  # internal name
    _parent = 'Displayable'  # internal name

    # Determined by above
    class DataType(models.TextChoices):
        UNKNOWN = '?', _('Unknown')
        INT = 'I', _('Integer')
        FLOAT = 'D', _('Decimal')

    type = models.CharField(max_length=1, blank=False, choices=DataType.choices, default=DataType.UNKNOWN)

    ModelHelper.register(_name, 'type', 85, to_filter=True, to_search=True)

    def is_int(self):
        return self.type == self.DataType.INT.value

    def is_float(self):
        return self.type == self.DataType.FLOAT.value

    def validate(self, value):
        if value is None or \
                self.is_int() and not isinstance(value, int) or \
                self.is_float() and not isinstance(value, float):
            return False

        # TODO

        return True

    @property
    def internal_name(self):
        return self._name


class IndicatorDataPoint(Displayable):
    _name = 'IndicatorDataPoint'  # internal name
    _parent = 'Displayable'  # internal name

    time = models.DateTimeField(null=False, db_index=True)

    # Should be set when validated
    validated = models.BooleanField(blank=False, default=False)
    processed = models.BooleanField(blank=False, default=False)

    notes = models.TextField(blank=True, null=False)

    class Meta:
        abstract = True

    ModelHelper.register(_name, 'time', 75, to_filter=True)
    ModelHelper.register(_name, 'notes', 30, to_serialize=False)
    ModelHelper.register(_name, 'validated', 10, False, to_serialize=False, to_search=True)
    ModelHelper.register(_name, 'processed', 10, False, to_serialize=False, to_search=True)


class IntDataPoint(IndicatorDataPoint):
    _name = 'IntDataPoint'  # internal name
    _parent = 'IndicatorDataPoint'  # internal name

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='int_data_points')

    indicator = models.ForeignKey(Indicator, on_delete=models.SET_NULL, null=True, related_name='int_data_points')
    value = models.IntegerField(null=False)

    # Optional submission which triggered this point
    source = models.ForeignKey(Submission, on_delete=models.SET_NULL, null=True, related_name='int_data_points')

    ModelHelper.register(_name, 'user', 85, foreign=User)
    ModelHelper.register(_name, 'indicator', 85, foreign=Indicator)
    ModelHelper.register(_name, 'value', 75, to_filter=True, to_search=True)


class FloatDataPoint(IndicatorDataPoint):
    _name = 'FloatDataPoint'  # internal name
    _parent = 'IndicatorDataPoint'  # internal name

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='float_data_points')

    indicator = models.ForeignKey(Indicator, on_delete=models.SET_NULL, null=True, related_name='float_data_points')
    value = models.FloatField(null=False)

    # Optional submission which triggered this point
    source = models.ForeignKey(Submission, on_delete=models.SET_NULL, null=True, related_name='float_data_points')

    ModelHelper.register(_name, 'user', 85, foreign=User)
    ModelHelper.register(_name, 'indicator', 85, foreign=Indicator)
    ModelHelper.register(_name, 'value', 75, to_filter=True, to_search=True)

# TODO send messages with validation to explain failure?
# TODO text references should be one to one, but that will complicate testing
