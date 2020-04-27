from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core import mail
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from Revitalize.models import Profile
import logging

logger = logging.getLogger(__name__)
_context = 'forms.'
_tracing = True


class AccountCreationForm(forms.Form):

    first_name = forms.CharField(label='First', min_length=1, max_length=40)
    middle_name = forms.CharField(label='Middle', min_length=0, max_length=40, required=False)
    last_name = forms.CharField(label='Last', min_length=1, max_length=40)

    date_of_birth = forms.DateField(label='Date of Birth', widget=forms.SelectDateWidget(years=list(range(1900, 2021))))

    _profile_fields = ['first_name', 'middle_name', 'last_name', 'date_of_birth']


    username = forms.CharField(label='Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Email', required=False)
    use_email = forms.BooleanField(label="Send password to this email?", widget=forms.CheckboxInput, initial=False,
                                   required=False)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth']

    class Meta:
        User = get_user_model()
        model = User
        fields = ('username', 'password1', 'password2') # , 'email')
        include = ('username', 'password1', 'password2')
        exclude = ('email',)

    def clean_username(self):
        User = get_user_model()

        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        # User = get_user_model()

        if 'email' not in self.cleaned_data:
            return ''
        email = self.cleaned_data['email'].lower()
        if len(email) < 5:
            return ''
        # r = User.objects.filter(email=email)
        # if r.count():
        #     raise ValidationError("Email already exists")
        return email

    def save(self, commit=True):
        __method = _context + self.__class__.__name__ + '.' + 'save'
        if _tracing: logger.info(__method + f"({commit})")

        User = get_user_model()

        password = User.objects.make_random_password(6)

        user = User.objects.create_user(
                self.cleaned_data['username'],
                '',
                password
        )

        profile_args = {}

        for f in self._profile_fields:
            if f in self.cleaned_data.keys():
                profile_args[f] = self.cleaned_data.get(f)

        profile = Profile.objects.create(
                user=user,
                email=self.cleaned_data['email'],
                **profile_args
        )

        if self.cleaned_data['use_email'] and len(self.cleaned_data['email']) > 4:
            send_to = self.cleaned_data['email']
        else:
            send_to = "astewart@upei.ca"

        subject = "Revitalize Access"

        message = f"\nThe Revitalize password for {profile.name()} ({user.username}) is {password}."

        try:
            with mail.get_connection() as connection:
                mail.EmailMessage(
                        subject, message, "system@revitalize.upei.ca", [send_to],
                        connection=connection,
                ).send()
        except Exception as e:
            logger.error(__method + f": error sending email to {user} at {send_to} ({e})")
            print(f"Missed password: {password}")


        # address_base = Address.objects.create(country=Address.Country.CANADA)
        # address = CanadianAddress.objects.create(base=address_base,
        #                                          street_address=p['street_address'],
        #                                          city=p['city'],
        #                                          postal_code=p['postal_code'],
        #                                          province=CanadianAddress.Province.PRINCE_EDWARD_ISLAND)
        #
        # profile = Profile.objects.create(
        #         address=address_base,
        #         user=user,
        #         first_name=p['first_name'],
        #         middle_name=p['middle_name'],
        #         last_name=p['last_name'],
        #         date_of_birth=p['date_of_birth'],
        #         gender=p['gender'],
        #         phone_number=p['phone_number'],
        #         phone_number_alt=p['phone_number_alt'],
        #         email=p['email'],
        #         ec_first_name=p['ec_first_name'],
        #         ec_middle_name=p['ec_middle_name'],
        #         ec_last_name=p['ec_last_name'],
        #         ec_phone_number=p['ec_phone_number'],
        #         physician=p['physician'],
        #         points=p['points'],
        #         personal_message=p['personal_message'],
        #         profile_picture=p['profile_picture'],
        #         password_flag=p['password_flag'],
        #         preferences=p['preferences'],
        # )

        return user




class AccountRegistrationForm(forms.Form):

    first_name = forms.CharField(label='First', min_length=1, max_length=40)
    middle_name = forms.CharField(label='Middle', min_length=0, max_length=40, required=False)
    last_name = forms.CharField(label='Last', min_length=1, max_length=40)

    date_of_birth = forms.DateField(label='Date of Birth', widget=forms.SelectDateWidget(years=list(range(1900, 2021))))

    _profile_fields = ['first_name', 'middle_name', 'last_name', 'date_of_birth']


    username = forms.CharField(label='Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Email', required=False)
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth']

    class Meta:
        User = get_user_model()
        model = User
        fields = ('username', 'password1', 'password2') # , 'email')
        include = ('username', 'password1', 'password2')
        exclude = ('email',)

    def clean_username(self):
        User = get_user_model()

        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        # User = get_user_model()

        if 'email' not in self.cleaned_data:
            return ''
        email = self.cleaned_data['email'].lower()
        if len(email) < 1:
            return ''
        # r = User.objects.filter(email=email)
        # if r.count():
        #     raise ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password doesn't match")

        return password2

    def save(self, commit=True):
        User = get_user_model()

        user = User.objects.create_user(
                self.cleaned_data['username'],
                '',
                self.cleaned_data['password1']
        )

        profile_args = {}

        for f in self._profile_fields:
            if f in self.cleaned_data.keys():
                profile_args[f] = self.cleaned_data.get(f)

        profile = Profile.objects.create(
                user=user,
                email=self.cleaned_data['email'],
                **profile_args
        )

        return user