from django.apps import apps
from django.contrib.admin import AdminSite
from django.contrib import admin

from Revitalize.models import *

# Administrator Admin Site


class AdminsSite(AdminSite):
    site_header = 'Admin Administration'

    def has_permission(self, request):

        if request.user.is_anonymous:
            return request.user.is_active and request.user.is_staff
        else:
            return (not request.user.is_lab_tech) and request.user.is_active and request.user.is_staff


admin_site = AdminsSite(name='admin_site')

models = apps.get_models()

for model in models:
    try:
        admin_site.register(model)
    except admin.sites.AlreadyRegistered:
        pass


# Lab Tech Admin Site

class LabTechSite(AdminSite):
    site_header = 'Lab Tech Administration'


lab_tech_site = LabTechSite(name='labtech_site')

lab_tech_site.disable_action('delete_selected')


@admin.register(Submission, site=lab_tech_site)
class ProfileAdmin(admin.ModelAdmin):
    exclude = ('flags', 'validated', 'parsed', 'processed')

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Profile, site=lab_tech_site)
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'first_name', 'middle_name', 'last_name', 'date_of_birth', 'gender', 'phone_number',
                       'phone_number_alt', 'email', 'address', 'ec_first_name', 'ec_middle_name', 'ec_last_name',
                       'ec_phone_number', 'physician', 'points', 'personal_message', 'profile_picture')
    exclude = ('flags', 'password_flag', 'preferences')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Form, site=lab_tech_site)
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'description', 'display', 'specification', 'analysis', 'tag', 'type')
    exclude = ('flags', 'notes')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Survey, site=lab_tech_site)
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('form', )
    exclude = ('flags', 'prefix')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(MedicalLab, site=lab_tech_site)
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('form', )
    exclude = ('flags', 'prefix')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Indicator, site=lab_tech_site)
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'description', 'display', 'specification', 'analysis', 'origin', 'type', 'good', 'max',
                       'target', 'min', 'dynamic', 'categorizable', 'conversion')
    exclude = ('flags', )

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(IntDataPoint, site=lab_tech_site)
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'description', 'time', 'validated', 'processed', 'user', 'indicator', 'value', 'source')
    exclude = ('flags', )

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(FloatDataPoint, site=lab_tech_site)
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'description', 'time', 'validated', 'processed', 'user', 'indicator', 'value', 'source')
    exclude = ('flags',)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
