from django.db import models
from django.utils.translation import gettext_lazy as _

class ModelBase(models.Model):
    rm_fields: list = ['id', 'flags', 'creation_time', 'update_time']
    rm_fields_display: list = ['id']
    rm_fields_filter: list = ['id']
    rm_fields_search: list = ['id']
    rm_fields_serialize: list = rm_fields.copy()

    id = models.BigAutoField(editable=False, primary_key=True)

    # This is here to provide a flexible way to annotate entries in the future, as may be required.
    flags = models.TextField(blank=False, help_text="This field is here as a stopgap measure for any extra information "
                                                    + "that needs to be noted with an entry. This should be a JSON.",
                             default="{}")

    creation_time = models.DateTimeField(auto_now_add=True, null=False)
    update_time = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        abstract = True


class Profile(ModelBase):
    rm_fields: list = ['first_name', 'middle_name', 'last_name', 'date_of_birth', 'gender',
                       'phone_number', 'phone_number_alt', 'email',
                       'street_address', 'city', 'province', 'country', 'postal_code',
                       'ec_first_name', 'ec_middle_name', 'ec_last_name', 'ec_phone_number',
                       'physician', 'points', 'password_flag', 'preferences', 'notes']
    rm_fields_display: list = ['first_name', 'middle_name', 'last_name', 'date_of_birth', 'gender',
                               'phone_number', 'phone_number_alt', 'email',
                               'street_address', 'city', 'province', 'country', 'postal_code',
                               'physician', 'points']
    rm_fields_filter: list = ['first_name', 'last_name', 'date_of_birth', 'gender',
                              'city', 'province', 'country', 'postal_code',
                              'physician', 'points']
    rm_fields_search: list = ['first_name', 'last_name', 'date_of_birth', 'gender',
                              'phone_number', 'phone_number_alt', 'email',
                              'street_address', 'city', 'province', 'country', 'postal_code',
                              'physician', 'points']
    rm_fields_serialize = rm_fields.copy()

    rm_fields.extend(ModelBase.rm_fields)
    rm_fields_display.extend(ModelBase.rm_fields_display)
    rm_fields_filter.extend(ModelBase.rm_fields_filter)
    rm_fields_search.extend(ModelBase.rm_fields_search)
    rm_fields_serialize.extend(ModelBase.rm_fields_serialize)

    class GenderType(models.TextChoices):
        Male = 'M', _('Male')
        Female = 'F', _('Female')
        Other = 'O', _('Other') # This will require a more detailed translation solution...

    first_name = models.CharField(max_length=40, blank=False)
    middle_name = models.CharField(max_length=40, null=False, blank=True, verbose_name="Middle Name(s)")
    last_name = models.CharField(max_length=40, blank=False, db_index=True)

    date_of_birth = models.DateField(null=False, db_index=True)
    gender = models.CharField(max_length=1, blank=False, choices=GenderType.choices)

    phone_number = models.CharField(max_length=40, blank=False, help_text="The primary contact number for a user.")
    phone_number_alt = models.CharField(max_length=40, null=False, blank=True,
                                        help_text="A secondary contact number for a user.",
                                        verbose_name="Alternate Phone Number")
    email = models.EmailField(blank=False, help_text="The email address for a user.")

    # Abstract into an address object?
    street_address = models.CharField(max_length=200, blank=False)
    city = models.CharField(max_length=100, blank=False)
    province = models.CharField(max_length=50, blank=False)
    country = models.CharField(max_length=25, blank=False)
    postal_code = models.CharField(max_length=10, blank=False)

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
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"