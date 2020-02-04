from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


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

        temp.sort(key=lambda x: model_sorts[x])

        return temp


class String(models.Model):
    _name = 'String'  # internal name

    id = models.BigAutoField(editable=False, primary_key=True)
    value = models.CharField(max_length=100, blank=False, help_text="The English value.")

    # Used with views and serializers
    ModelHelper.register(_name, 'id', 100, to_search=True, to_serialize=False)
    ModelHelper.register(_name, 'value', 75, to_search=True)

    def __str__(self):
        return self.value + f" ({self.id})"


class Text(models.Model):
    _name = 'Text'  # internal name

    id = models.BigAutoField(editable=False, primary_key=True)
    value = models.TextField(blank=False, help_text="The English value.")

    # Used with views and serializers
    ModelHelper.register(_name, 'id', 100, to_search=True, to_serialize=False)
    ModelHelper.register(_name, 'value', 75, to_search=True)

    def __str__(self):
        return self.value + f" ({self.id})"


class StringGroup(models.Model):
    _name = 'StringGroup'  # internal name

    id = models.BigAutoField(editable=False, primary_key=True)
    values = models.TextField(blank=False, help_text="The English values in a JSON.")

    # Used with views and serializers
    ModelHelper.register(_name, 'id', 100, to_search=True, to_serialize=False)
    ModelHelper.register(_name, 'values', 75, to_search=True, text_type='JSON')

    def __str__(self):
        return self.values + f" ({self.id})"


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
    ModelHelper.register(_name, 'id', 100, to_search=True, to_serialize=False)
    ModelHelper.register(_name, 'flags', 25, False, to_search=True, text_type='JSON')
    ModelHelper.register(_name, 'creation_time', 5, to_filter=True, to_serialize=False)
    ModelHelper.register(_name, 'update_time', 5, to_filter=True, to_serialize=False)


class Profile(ModelBase):
    _name = 'Profile'  # internal name
    _parent = 'ModelBase'  # internal name

    user = models.ForeignKey(User, on_delete=models.CASCADE)

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
