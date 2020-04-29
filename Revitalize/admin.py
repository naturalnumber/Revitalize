from django.apps import apps
from django.contrib import admin, auth
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group

from Revitalize.models import *


class DetailedAdminsSite(AdminSite):
    site_header = 'Detailed Admin Administration'

    def has_permission(self, request):
        user: User = request.user

        return user.is_authenticated and user.is_active and user.is_staff and user.is_superuser


detailed_admin_site = DetailedAdminsSite(name='detailed_admin_site')

models = apps.get_models()

for model in models:
    try:
        detailed_admin_site.register(model)
    except admin.sites.AlreadyRegistered:
        pass


# Admin Inlines


class ProfileInline(admin.StackedInline):
    model = Profile

    exclude = ('flags', 'password_flag', 'preferences')


class SurveyInline(admin.TabularInline):
    model = Survey

    fields = ('prefix',)


class TextElementInline(admin.TabularInline):
    model = TextElement

    readonly_fields = ('id',)
    fields = ('number', 'prefix', 'text', 'help_text', 'screen_reader_text')

    extra = 0
    show_change_link = True


class CanadianAddressInline(admin.TabularInline):
    model = CanadianAddress

    fields = ('street_address', 'city', 'province', 'postal_code')

    extra = 0
    # show_change_link = True


class QuestionGroupInline(admin.TabularInline):
    model = QuestionGroup

    readonly_fields = ('id',)
    fields = ('number', 'prefix', 'type', 'text', 'help_text', 'screen_reader_text', 'internal_name')

    extra = 0
    show_change_link = True

    # def admin_link(self, instance):
    #     url = reverse('admin:%s_%s_change' % (instance._meta.app_label,
    #                                           instance._meta.model_name),
    #                   args=(instance.id,))
    #     print(url)
    #     return format_html(u'<a href="{}">Edit</a>', url)
    #     # … or if you want to include other fields:
    #     # return format_html(u'<a href="{}">Edit: {}</a>', url, instance.title)


_q_type_inlines = []


class TextQuestionInline(admin.TabularInline):
    model = TextQuestion

    readonly_fields = ('id',)
    fields = ('min_length', 'max_length')

    extra = 0
    show_change_link = True

    verbose_name = 'Type Data'

    verbose_name_plural = 'Type Data'


_q_type_inlines.append(TextQuestionInline)


class IntQuestionInline(admin.TabularInline):
    model = IntQuestion

    readonly_fields = ('id',)
    fields = ('min', 'max')

    extra = 0
    show_change_link = True

    verbose_name = 'Type Data'

    verbose_name_plural = 'Type Data'


_q_type_inlines.append(IntQuestionInline)


class FloatQuestionInline(admin.TabularInline):
    model = FloatQuestion

    readonly_fields = ('id',)
    fields = ('min', 'max')

    extra = 0
    show_change_link = True

    verbose_name = 'Type Data'

    verbose_name_plural = 'Type Data'


_q_type_inlines.append(FloatQuestionInline)


class IntRangeQuestionInline(admin.TabularInline):
    model = IntRangeQuestion

    readonly_fields = ('id',)
    fields = ('num_possibilities', 'min', 'max', 'step', 'initial', 'labels')

    extra = 0
    show_change_link = True

    verbose_name = 'Type Data'

    verbose_name_plural = 'Type Data'


_q_type_inlines.append(IntRangeQuestionInline)


class BooleanChoiceQuestionInline(admin.TabularInline):
    model = BooleanChoiceQuestion

    readonly_fields = ('id',)
    fields = ('labels',)

    extra = 0
    show_change_link = True

    verbose_name = 'Type Data'

    verbose_name_plural = 'Type Data'


_q_type_inlines.append(BooleanChoiceQuestionInline)


class ExclusiveChoiceQuestionInline(admin.TabularInline):
    model = ExclusiveChoiceQuestion

    readonly_fields = ('id',)
    fields = ('num_possibilities', 'initial', 'labels')

    extra = 0
    show_change_link = True

    verbose_name = 'Type Data'

    verbose_name_plural = 'Type Data'


_q_type_inlines.append(ExclusiveChoiceQuestionInline)


class MultiChoiceQuestionInline(admin.TabularInline):
    model = MultiChoiceQuestion

    readonly_fields = ('id',)
    fields = ('num_possibilities', 'min_choices', 'max_choices', 'labels')

    extra = 0
    show_change_link = True

    verbose_name = 'Type Data'

    verbose_name_plural = 'Type Data'


_q_type_inlines.append(MultiChoiceQuestionInline)


class FloatRangeQuestionInline(admin.TabularInline):
    model = FloatRangeQuestion

    readonly_fields = ('id',)
    fields = ('range', 'min', 'max', 'initial', 'labels')

    extra = 0
    show_change_link = True

    verbose_name = 'Type Data'

    verbose_name_plural = 'Type Data'


_q_type_inlines.append(FloatRangeQuestionInline)


class QuestionInline(admin.TabularInline):
    model = Question

    readonly_fields = ('id',)
    fields = ('number', 'prefix', 'optional', 'text', 'help_text', 'screen_reader_text')  # , 'internal_name'

    extra = 0
    show_change_link = True


class IntDataPointInline(admin.TabularInline):
    model = IntDataPoint

    readonly_fields = ('id',)
    fields = ('user', 'indicator', 'time', 'value')

    extra = 0
    show_change_link = True

    verbose_name = 'Data Point'

    verbose_name_plural = 'Data Points'


class FloatDataPointInline(admin.TabularInline):
    model = FloatDataPoint

    readonly_fields = ('id',)
    fields = ('user', 'indicator', 'time', 'value')

    extra = 0
    show_change_link = True

    verbose_name = 'Data Point'

    verbose_name_plural = 'Data Points'


class IntDataPointInline2(admin.TabularInline):
    model = IntDataPoint

    readonly_fields = ('id',)
    fields = ('user', 'indicator', 'time', 'value')

    extra = 0
    show_change_link = True

    verbose_name = 'Integer Data Point'

    verbose_name_plural = 'Integer Data Points'


class FloatDataPointInline2(admin.TabularInline):
    model = FloatDataPoint

    readonly_fields = ('id',)
    fields = ('user', 'indicator', 'time', 'value')

    extra = 0
    show_change_link = True

    verbose_name = 'Decimal Data Point'

    verbose_name_plural = 'Decimal Data Points'


# Administrator Admin Site


class AdminsSite(AdminSite):
    site_header = 'Admin Administration'

    def has_permission(self, request):
        user: User = request.user

        return user.is_authenticated and user.is_active and user.is_staff and user.is_superuser


admin_site = AdminsSite(name='admin_site')


@admin.register(User, site=admin_site)
class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'is_staff', 'is_lab_tech', 'is_active', 'is_superuser', 'last_login', 'date_joined')

    list_display = ('first_name_', 'last_name_', 'date_of_birth', 'gender',
                    'country', 'street_address', 'city', 'province', 'postal_code',
                    'username', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined')

    list_filter = ('profile__address__address__province', 'profile__address__address__postal_code',
                   'profile__address__country',
                   'profile__creation_time', 'profile__update_time',
                   'is_staff', 'is_active', 'is_superuser')

    search_fields = ('username',
                     'profile__first_name', 'profile__last_name', 'profile__address__address__street_address',
                     'profile__address__address__city', 'profile__address__address__province',
                     'profile__address__address__postal_code')

    list_select_related = ('profile',)

    inlines = [ProfileInline, IntDataPointInline2, FloatDataPointInline2]

    def first_name_(self, obj: User):
        return obj.profile.first_name

    first_name_.admin_order_field = f'profile__{"first_name"}'

    def last_name_(self, obj: User):
        return obj.profile.last_name

    last_name_.admin_order_field = f'profile__{"last_name"}'

    def date_of_birth(self, obj: User):
        return obj.profile.date_of_birth

    date_of_birth.admin_order_field = f'profile__{"date_of_birth"}'

    def gender(self, obj: User):
        return obj.profile.gender

    gender.admin_order_field = f'profile__{"gender"}'

    def country(self, obj: User):
        return obj.profile.address.country

    country.admin_order_field = f'profile__address__{"country"}'

    def street_address(self, obj: User):
        return obj.profile.address.address.street_address

    street_address.admin_order_field = f'profile__address__address__{"street_address"}'

    def city(self, obj: User):
        return obj.profile.address.address.city

    city.admin_order_field = f'profile__address__address__{"city"}'

    def province(self, obj: User):
        return obj.profile.address.address.province

    province.admin_order_field = f'profile__address__address__{"province"}'

    def postal_code(self, obj: User):
        return obj.profile.address.address.postal_code

    postal_code.admin_order_field = f'profile__address__address__{"postal_code"}'


@admin.register(String, site=admin_site)
class StringAdmin(admin.ModelAdmin):
    list_display = ('id', 'value')
    # list_filter = ('creation_time', 'update_time')

    search_fields = ('value',)

    # date_hierarchy = 'creation_time'

    def has_module_permission(self, request):
        return False


@admin.register(Text, site=admin_site)
class TextAdmin(admin.ModelAdmin):
    list_display = ('id', 'value')
    # list_filter = ('creation_time', 'update_time')

    search_fields = ('value',)

    # date_hierarchy = 'creation_time'

    def has_module_permission(self, request):
        return False


@admin.register(StringGroup, site=admin_site)
class StringGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'value')
    # list_filter = ('creation_time', 'update_time')

    search_fields = ('value',)

    # date_hierarchy = 'creation_time'

    def has_module_permission(self, request):
        return False


@admin.register(Address, site=admin_site)
class AddressAdmin(admin.ModelAdmin):
    fields = ('country',)

    list_display = ('country', 'street_address', 'city', 'province', 'postal_code')
    list_filter = ('address__province', 'address__postal_code', 'creation_time', 'update_time')

    search_fields = ('user__first_name', 'user__last_name', 'address__street_address', 'address__city',
                     'address__province', 'address__postal_code')

    date_hierarchy = 'creation_time'

    list_select_related = ('address',)

    inlines = [CanadianAddressInline, ]

    def street_address(self, obj: Address):
        return obj.address.street_address

    street_address.admin_order_field = f'address__{"street_address"}'

    def city(self, obj: Address):
        return obj.address.city

    city.admin_order_field = f'address__{"city"}'

    def province(self, obj: Address):
        return obj.address.province

    province.admin_order_field = f'address__{"province"}'

    def postal_code(self, obj: Address):
        return obj.address.postal_code

    postal_code.admin_order_field = f'address__{"postal_code"}'

    def has_module_permission(self, request):
        return False


@admin.register(CanadianAddress, site=admin_site)
class CanadianAddressAdmin(admin.ModelAdmin):
    fields = ('street_address', 'city', 'province', 'postal_code')

    list_display = ('street_address', 'city', 'province', 'postal_code')
    list_filter = ('province', 'postal_code', 'creation_time', 'update_time')

    search_fields = ('user__base__first_name', 'user__base__last_name', 'street_address', 'city', 'province',
                     'postal_code')

    date_hierarchy = 'creation_time'

    def has_module_permission(self, request):
        return False


@admin.register(Profile, site=admin_site)
class ProfileAdmin(admin.ModelAdmin):
    # readonly_fields = ('user', 'first_name', 'middle_name', 'last_name', 'date_of_birth', 'gender', 'phone_number',
    #                    'phone_number_alt', 'email', 'address', 'ec_first_name', 'ec_middle_name', 'ec_last_name',
    #                    'ec_phone_number', 'physician', 'points', 'personal_message', 'profile_picture')

    exclude = ('flags', 'password_flag', 'preferences')

    list_display = ('first_name', 'middle_name', 'last_name', 'date_of_birth', 'gender', 'country', 'street_address',
                    'city', 'province', 'postal_code')
    list_filter = ('address__address__province', 'address__address__postal_code', 'address__country',
                   'creation_time', 'update_time')

    search_fields = ('first_name', 'last_name', 'middle_name', 'address__address__street_address',
                     'address__address__city', 'address__address__province', 'address__address__postal_code')

    def country(self, obj: Profile):
        return obj.address.country

    country.admin_order_field = f'address__{"country"}'

    def street_address(self, obj: Profile):
        return obj.address.address.street_address

    street_address.admin_order_field = f'address__address__{"street_address"}'

    def city(self, obj: Profile):
        return obj.address.address.city

    city.admin_order_field = f'address__address__{"city"}'

    def province(self, obj: Profile):
        return obj.address.address.province

    province.admin_order_field = f'address__address__{"province"}'

    def postal_code(self, obj: Profile):
        return obj.address.address.postal_code

    postal_code.admin_order_field = f'address__address__{"postal_code"}'

    def has_module_permission(self, request):
        return False


@admin.register(Submission, site=admin_site)
class SubmissionAdmin(admin.ModelAdmin):
    exclude = ('flags', 'validated', 'parsed', 'processed', 'raw_data')

    list_display = ('first_name_', 'last_name_', 'form_', 'time', 'creation_time', 'update_time')
    list_filter = (('form', admin.RelatedOnlyFieldListFilter), 'time', 'creation_time', 'update_time')

    search_fields = ('user__profile__first_name', 'user__profile__last_name', 'form__name__value')

    date_hierarchy = 'time'

    def first_name_(self, obj: Submission):
        return obj.user.profile.first_name

    first_name_.admin_order_field = f'user__profile__{"first_name"}'

    def last_name_(self, obj: Submission):
        return obj.user.profile.last_name

    last_name_.admin_order_field = f'user__profile__{"last_name"}'

    def form_(self, obj: Submission):
        return obj.form.name.value

    form_.admin_order_field = 'form__name__value'

    inlines = [IntDataPointInline2, FloatDataPointInline2]

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Form, site=admin_site)
class FormAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'creation_time', 'update_time')
    exclude = ('flags', 'notes', 'display', 'specification', 'analysis', 'annotations')

    list_display = ('name_', 'type', 'creation_time', 'update_time')
    list_filter = ('type', 'creation_time', 'update_time')

    search_fields = ('name__value', 'description__value', 'tag')

    list_select_related = ('name', 'description')

    date_hierarchy = 'creation_time'

    inlines = [TextElementInline, QuestionGroupInline]  # TODO remove survey model or create by default *** * ***

    def name_(self, obj: Form):
        return obj.name.value

    name_.admin_order_field = f'name__{"value"}'


@admin.register(QuestionGroup, site=admin_site)
class QuestionGroupAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'form', 'type', 'creation_time', 'update_time')
    fields = ('number', 'prefix', 'type', 'text', 'help_text', 'screen_reader_text', 'internal_name')
    exclude = ('flags', 'notes', 'display', 'specification', 'analysis', 'annotations')

    inlines = [QuestionInline, ] + _q_type_inlines

    def get_formsets_with_inlines(self, request, group: QuestionGroup = None):
        for inline in self.get_inline_instances(request, group):
            # hide MyInline in the add view

            if group is not None and (not isinstance(inline, tuple(_q_type_inlines))
                                      or inline.model is Question
                                      or inline.model is group.data_class()):
                yield inline.get_formset(request, group), inline

    def has_module_permission(self, request):
        return False


@admin.register(Question, site=admin_site)
class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'group', 'creation_time', 'update_time')
    fields = ('number', 'prefix', 'text', 'help_text', 'screen_reader_text', 'internal_name', 'annotations')
    exclude = ('flags', 'notes', 'display', 'specification', 'analysis')

    def has_module_permission(self, request):
        return False


# @admin.register(Survey, site=admin_site)
# class SurveyAdmin(admin.ModelAdmin):
#     exclude = ('form', 'flags', 'prefix')
#
#
# @admin.register(MedicalLab, site=admin_site)
# class MedicalLabAdmin(admin.ModelAdmin):
#     exclude = ('form', 'flags', 'prefix')


@admin.register(Indicator, site=admin_site)
class IndicatorAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'origin', 'type', 'max', 'target', 'min', 'unit', 'analysis', 'good')
    exclude = ('flags', 'display', 'specification', 'dynamic', 'categorizable', 'conversion', )

    list_display = ('name_', 'type', 'origin', 'creation_time', 'update_time')
    list_filter = ('type', 'origin', 'creation_time', 'update_time')

    search_fields = ('name__value', 'description__value')

    date_hierarchy = 'creation_time'

    def name_(self, obj: Form):
        return obj.name.value

    name_.admin_order_field = f'name__{"value"}'

    inlines = [IntDataPointInline, FloatDataPointInline]

    def get_formsets_with_inlines(self, request, indicator: Indicator = None):
        for inline in self.get_inline_instances(request, indicator):
            # hide MyInline in the add view

            if indicator is not None and (not isinstance(inline, tuple([IntDataPointInline, FloatDataPointInline]))
                                          or inline.model is indicator.data_class()):
                yield inline.get_formset(request, indicator), inline


@admin.register(IntDataPoint, site=admin_site)
class IntDataPointAdmin(admin.ModelAdmin):
    fields = ('user', 'indicator', 'time', 'value',)
    exclude = ('name', 'description', 'flags', 'source', 'validated', 'processed')

    list_display = ('first_name', 'last_name', 'indicator_', 'time', 'value')
    list_filter = ('indicator', 'time')

    search_fields = ('indicator__name__value', 'user__profile__first_name', 'user__profile__last_name')

    date_hierarchy = 'creation_time'

    def indicator_(self, obj: IntDataPoint):
        return obj.indicator.name.value

    indicator_.admin_order_field = 'indicator__name__value'

    def first_name(self, obj: IntDataPoint):
        return obj.user.profile.first_name

    first_name.admin_order_field = 'user__profile__first_name'

    def last_name(self, obj: IntDataPoint):
        return obj.user.profile.last_name

    last_name.admin_order_field = 'user__profile__last_name'

    def has_module_permission(self, request):
        return False


@admin.register(FloatDataPoint, site=admin_site)
class FloatDataPointAdmin(admin.ModelAdmin):
    fields = ('user', 'indicator', 'time', 'value',)
    exclude = ('name', 'description', 'flags', 'source', 'validated', 'processed')

    list_display = ('first_name', 'last_name', 'indicator_', 'time', 'value')
    list_filter = ('indicator', 'time')

    search_fields = ('indicator__name__value', 'user__profile__first_name', 'user__profile__last_name')

    date_hierarchy = 'creation_time'

    def indicator_(self, obj: IntDataPoint):
        return obj.indicator.name.value

    indicator_.admin_order_field = 'indicator__name__value'

    def first_name(self, obj: IntDataPoint):
        return obj.user.profile.first_name

    first_name.admin_order_field = 'user__profile__first_name'

    def last_name(self, obj: IntDataPoint):
        return obj.user.profile.last_name

    last_name.admin_order_field = 'user__profile__last_name'

    def has_module_permission(self, request):
        return False


# Admin Inlines


class ProfileInlineLT(admin.StackedInline):
    model = Profile

    exclude = ('flags', 'password_flag', 'preferences')


class SurveyInlineLT(admin.TabularInline):
    model = Survey

    fields = ('prefix',)


class TextElementInlineLT(admin.TabularInline):
    model = TextElement

    readonly_fields = ('id',)
    fields = ('number', 'prefix', 'text', 'help_text', 'screen_reader_text')

    extra = 0
    show_change_link = True


class CanadianAddressInlineLT(admin.TabularInline):
    model = CanadianAddress

    fields = ('street_address', 'city', 'province', 'postal_code')

    extra = 0
    # show_change_link = True


class QuestionGroupInlineLT(admin.TabularInline):
    model = QuestionGroup

    readonly_fields = ('id',)
    fields = ('number', 'prefix', 'type', 'text', 'help_text', 'screen_reader_text', 'internal_name')

    extra = 0
    show_change_link = True

    # def admin_link(self, instance):
    #     url = reverse('admin:%s_%s_change' % (instance._meta.app_label,
    #                                           instance._meta.model_name),
    #                   args=(instance.id,))
    #     print(url)
    #     return format_html(u'<a href="{}">Edit</a>', url)
    #     # … or if you want to include other fields:
    #     # return format_html(u'<a href="{}">Edit: {}</a>', url, instance.title)


_q_type_inlines = []


class TextQuestionInlineLT(admin.TabularInline):
    model = TextQuestion

    readonly_fields = ('id',)
    fields = ('min_length', 'max_length')

    extra = 0
    show_change_link = True

    verbose_name = 'Type Data'

    verbose_name_plural = 'Type Data'


_q_type_inlines.append(TextQuestionInline)


class IntQuestionInlineLT(admin.TabularInline):
    model = IntQuestion

    readonly_fields = ('id',)
    fields = ('min', 'max')

    extra = 0
    show_change_link = True

    verbose_name = 'Type Data'

    verbose_name_plural = 'Type Data'


_q_type_inlines.append(IntQuestionInline)


class FloatQuestionInlineLT(admin.TabularInline):
    model = FloatQuestion

    readonly_fields = ('id',)
    fields = ('min', 'max')

    extra = 0
    show_change_link = True

    verbose_name = 'Type Data'

    verbose_name_plural = 'Type Data'


_q_type_inlines.append(FloatQuestionInline)


class IntRangeQuestionInlineLT(admin.TabularInline):
    model = IntRangeQuestion

    readonly_fields = ('id',)
    fields = ('num_possibilities', 'min', 'max', 'step', 'initial', 'labels')

    extra = 0
    show_change_link = True

    verbose_name = 'Type Data'

    verbose_name_plural = 'Type Data'


_q_type_inlines.append(IntRangeQuestionInline)


class BooleanChoiceQuestionInlineLT(admin.TabularInline):
    model = BooleanChoiceQuestion

    readonly_fields = ('id',)
    fields = ('labels',)

    extra = 0
    show_change_link = True

    verbose_name = 'Type Data'

    verbose_name_plural = 'Type Data'


_q_type_inlines.append(BooleanChoiceQuestionInline)


class ExclusiveChoiceQuestionInlineLT(admin.TabularInline):
    model = ExclusiveChoiceQuestion

    readonly_fields = ('id',)
    fields = ('num_possibilities', 'initial', 'labels')

    extra = 0
    show_change_link = True

    verbose_name = 'Type Data'

    verbose_name_plural = 'Type Data'


_q_type_inlines.append(ExclusiveChoiceQuestionInline)


class MultiChoiceQuestionInlineLT(admin.TabularInline):
    model = MultiChoiceQuestion

    readonly_fields = ('id',)
    fields = ('num_possibilities', 'min_choices', 'max_choices', 'labels')

    extra = 0
    show_change_link = True

    verbose_name = 'Type Data'

    verbose_name_plural = 'Type Data'


_q_type_inlines.append(MultiChoiceQuestionInline)


class FloatRangeQuestionInlineLT(admin.TabularInline):
    model = FloatRangeQuestion

    readonly_fields = ('id',)
    fields = ('range', 'min', 'max', 'initial', 'labels')

    extra = 0
    show_change_link = True

    verbose_name = 'Type Data'

    verbose_name_plural = 'Type Data'


_q_type_inlines.append(FloatRangeQuestionInline)


class QuestionInlineLT(admin.TabularInline):
    model = Question

    readonly_fields = ('id',)
    fields = ('number', 'prefix', 'optional', 'text', 'help_text', 'screen_reader_text')  # , 'internal_name'

    extra = 0
    show_change_link = True


class IntDataPointInlineLT(admin.TabularInline):
    model = IntDataPoint

    readonly_fields = ('id',)
    fields = ('user', 'indicator', 'time', 'value')

    extra = 0
    show_change_link = True

    verbose_name = 'Data Point'

    verbose_name_plural = 'Data Points'


class FloatDataPointInlineLT(admin.TabularInline):
    model = FloatDataPoint

    readonly_fields = ('id',)
    fields = ('user', 'indicator', 'time', 'value')

    extra = 0
    show_change_link = True

    verbose_name = 'Data Point'

    verbose_name_plural = 'Data Points'


class IntDataPointInlineLT2(admin.TabularInline):
    model = IntDataPoint

    readonly_fields = ('id',)
    fields = ('user', 'indicator', 'time', 'value')

    extra = 0
    show_change_link = True

    verbose_name = 'Integer Data Point'

    verbose_name_plural = 'Integer Data Points'


class FloatDataPointInlineLT2(admin.TabularInline):
    model = FloatDataPoint

    readonly_fields = ('id',)
    fields = ('user', 'indicator', 'time', 'value')

    extra = 0
    show_change_link = True

    verbose_name = 'Decimal Data Point'

    verbose_name_plural = 'Decimal Data Points'


# Lab Tech Admin Site


class LabTechSite(AdminSite):
    site_header = 'Admin Administration'

    def has_permission(self, request):
        user: User = request.user

        return user.is_authenticated and user.is_active and user.is_staff


lab_tech_site = LabTechSite(name='lab_tech_site')


@admin.register(User, site=lab_tech_site)
class UserLabTech(admin.ModelAdmin):
    readonly_fields = ('username', 'is_staff', 'is_active', 'last_login', 'date_joined')
    exclude = ('password', 'groups', 'is_superuser', 'user_permissions', 'first_name', 'last_name', 'email')

    list_display = ('first_name_', 'last_name_', 'date_of_birth', 'gender',
                    'country', 'street_address', 'city', 'province', 'postal_code',
                    'username', 'is_staff', 'is_active', 'last_login', 'date_joined')

    list_filter = ('profile__address__address__province', 'profile__address__address__postal_code',
                   'profile__address__country',
                   'profile__creation_time', 'profile__update_time',
                   'is_staff', 'is_active')

    search_fields = ('username',
                     'profile__first_name', 'profile__last_name', 'profile__address__address__street_address',
                     'profile__address__address__city', 'profile__address__address__province',
                     'profile__address__address__postal_code')

    list_select_related = ('profile',)

    inlines = [ProfileInlineLT, IntDataPointInlineLT2, FloatDataPointInlineLT2]

    def first_name_(self, obj: User):
        return obj.profile.first_name

    first_name_.admin_order_field = f'profile__{"first_name"}'

    def last_name_(self, obj: User):
        return obj.profile.last_name

    last_name_.admin_order_field = f'profile__{"last_name"}'

    def date_of_birth(self, obj: User):
        return obj.profile.date_of_birth

    date_of_birth.admin_order_field = f'profile__{"date_of_birth"}'

    def gender(self, obj: User):
        return obj.profile.gender

    gender.admin_order_field = f'profile__{"gender"}'

    def country(self, obj: User):
        return obj.profile.address.country

    country.admin_order_field = f'profile__address__{"country"}'

    def street_address(self, obj: User):
        return obj.profile.address.address.street_address

    street_address.admin_order_field = f'profile__address__address__{"street_address"}'

    def city(self, obj: User):
        return obj.profile.address.address.city

    city.admin_order_field = f'profile__address__address__{"city"}'

    def province(self, obj: User):
        return obj.profile.address.address.province

    province.admin_order_field = f'profile__address__address__{"province"}'

    def postal_code(self, obj: User):
        return obj.profile.address.address.postal_code

    postal_code.admin_order_field = f'profile__address__address__{"postal_code"}'

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(String, site=lab_tech_site)
class StringLabTech(admin.ModelAdmin):
    list_display = ('id', 'value')
    # list_filter = ('creation_time', 'update_time')

    search_fields = ('value',)

    # date_hierarchy = 'creation_time'

    def has_module_permission(self, request):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Text, site=lab_tech_site)
class TextLabTech(admin.ModelAdmin):
    list_display = ('id', 'value')
    # list_filter = ('creation_time', 'update_time')

    search_fields = ('value',)

    # date_hierarchy = 'creation_time'

    def has_module_permission(self, request):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(StringGroup, site=lab_tech_site)
class StringGroupLabTech(admin.ModelAdmin):
    list_display = ('id', 'value')
    # list_filter = ('creation_time', 'update_time')

    search_fields = ('value',)

    # date_hierarchy = 'creation_time'

    def has_module_permission(self, request):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Address, site=lab_tech_site)
class AddressLabTech(admin.ModelAdmin):
    fields = ('country',)

    list_display = ('country', 'street_address', 'city', 'province', 'postal_code')
    list_filter = ('address__province', 'address__postal_code', 'creation_time', 'update_time')

    search_fields = ('user__first_name', 'user__last_name', 'address__street_address', 'address__city',
                     'address__province', 'address__postal_code')

    date_hierarchy = 'creation_time'

    list_select_related = ('address',)

    inlines = [CanadianAddressInlineLT, ]

    def street_address(self, obj: Address):
        return obj.address.street_address

    street_address.admin_order_field = f'address__{"street_address"}'

    def city(self, obj: Address):
        return obj.address.city

    city.admin_order_field = f'address__{"city"}'

    def province(self, obj: Address):
        return obj.address.province

    province.admin_order_field = f'address__{"province"}'

    def postal_code(self, obj: Address):
        return obj.address.postal_code

    postal_code.admin_order_field = f'address__{"postal_code"}'

    def has_module_permission(self, request):
        return False


@admin.register(CanadianAddress, site=lab_tech_site)
class CanadianAddressLabTech(admin.ModelAdmin):
    fields = ('street_address', 'city', 'province', 'postal_code')

    list_display = ('street_address', 'city', 'province', 'postal_code')
    list_filter = ('province', 'postal_code', 'creation_time', 'update_time')

    search_fields = ('user__base__first_name', 'user__base__last_name', 'street_address', 'city', 'province',
                     'postal_code')

    date_hierarchy = 'creation_time'

    def has_module_permission(self, request):
        return False


@admin.register(Profile, site=lab_tech_site)
class ProfileLabTech(admin.ModelAdmin):
    # readonly_fields = ('user', 'first_name', 'middle_name', 'last_name', 'date_of_birth', 'gender', 'phone_number',
    #                    'phone_number_alt', 'email', 'address', 'ec_first_name', 'ec_middle_name', 'ec_last_name',
    #                    'ec_phone_number', 'physician', 'points', 'personal_message', 'profile_picture')

    exclude = ('flags', 'password_flag', 'preferences')

    list_display = ('first_name', 'middle_name', 'last_name', 'date_of_birth', 'gender', 'country', 'street_address',
                    'city', 'province', 'postal_code')
    list_filter = ('address__address__province', 'address__address__postal_code', 'address__country',
                   'creation_time', 'update_time')

    search_fields = ('first_name', 'last_name', 'middle_name', 'address__address__street_address',
                     'address__address__city', 'address__address__province', 'address__address__postal_code')

    def country(self, obj: Profile):
        return obj.address.country

    country.admin_order_field = f'address__{"country"}'

    def street_address(self, obj: Profile):
        return obj.address.address.street_address

    street_address.admin_order_field = f'address__address__{"street_address"}'

    def city(self, obj: Profile):
        return obj.address.address.city

    city.admin_order_field = f'address__address__{"city"}'

    def province(self, obj: Profile):
        return obj.address.address.province

    province.admin_order_field = f'address__address__{"province"}'

    def postal_code(self, obj: Profile):
        return obj.address.address.postal_code

    postal_code.admin_order_field = f'address__address__{"postal_code"}'

    def has_module_permission(self, request):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Submission, site=lab_tech_site)
class SubmissionLabTech(admin.ModelAdmin):
    exclude = ('flags', 'validated', 'parsed', 'processed', 'raw_data')

    list_display = ('first_name_', 'last_name_', 'form_', 'time', 'creation_time', 'update_time')
    list_filter = (('form', admin.RelatedOnlyFieldListFilter), 'time', 'creation_time', 'update_time')

    search_fields = ('user__profile__first_name', 'user__profile__last_name', 'form__name__value')

    date_hierarchy = 'time'

    def first_name_(self, obj: Submission):
        return obj.user.profile.first_name

    first_name_.admin_order_field = f'user__profile__{"first_name"}'

    def last_name_(self, obj: Submission):
        return obj.user.profile.last_name

    last_name_.admin_order_field = f'user__profile__{"last_name"}'

    def form_(self, obj: Submission):
        return obj.form.name.value

    form_.admin_order_field = 'form__name__value'

    inlines = [IntDataPointInlineLT2, FloatDataPointInlineLT2]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Form, site=lab_tech_site)
class FormLabTech(admin.ModelAdmin):
    readonly_fields = ('id', 'creation_time', 'update_time')
    exclude = ('flags', 'notes', 'display', 'specification', 'analysis', 'annotations')

    list_display = ('name_', 'type', 'creation_time', 'update_time')
    list_filter = ('type', 'creation_time', 'update_time')

    search_fields = ('name__value', 'description__value', 'tag')

    list_select_related = ('name', 'description')

    date_hierarchy = 'creation_time'

    inlines = [TextElementInlineLT, QuestionGroupInlineLT]  # TODO remove survey model or create by default *** * ***

    def name_(self, obj: Form):
        return obj.name.value

    name_.admin_order_field = f'name__{"value"}'

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(QuestionGroup, site=lab_tech_site)
class QuestionGroupLabTech(admin.ModelAdmin):
    readonly_fields = ('id', 'form', 'type', 'creation_time', 'update_time')
    fields = ('number', 'prefix', 'type', 'text', 'help_text', 'screen_reader_text', 'internal_name')
    exclude = ('flags', 'notes', 'display', 'specification', 'analysis', 'annotations')

    inlines = [QuestionInlineLT, ] + _q_type_inlines

    def get_formsets_with_inlines(self, request, group: QuestionGroup = None):
        for inline in self.get_inline_instances(request, group):
            # hide MyInlineLT in the add view

            if group is not None and (not isinstance(inline, tuple(_q_type_inlines))
                                      or inline.model is Question
                                      or inline.model is group.data_class()):
                yield inline.get_formset(request, group), inline

    def has_module_permission(self, request):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Question, site=lab_tech_site)
class QuestionLabTech(admin.ModelAdmin):
    readonly_fields = ('id', 'group', 'creation_time', 'update_time')
    fields = ('number', 'prefix', 'text', 'help_text', 'screen_reader_text', 'internal_name', 'annotations')
    exclude = ('flags', 'notes', 'display', 'specification', 'analysis')

    def has_module_permission(self, request):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


# @admin.register(Survey, site=lab_tech_site)
# class SurveyLabTech(admin.ModelAdmin):
#     exclude = ('form', 'flags', 'prefix')
#
#
# @admin.register(MedicalLab, site=lab_tech_site)
# class MedicalLabLabTech(admin.ModelAdmin):
#     exclude = ('form', 'flags', 'prefix')


@admin.register(Indicator, site=lab_tech_site)
class IndicatorLabTech(admin.ModelAdmin):
    readonly_fields = ('name', 'description', 'origin', 'type', 'max', 'target', 'min', 'unit')
    exclude = ('flags', 'display', 'specification', 'analysis', 'dynamic', 'categorizable', 'conversion', 'good', 'notes',)

    list_display = ('name_', 'type', 'origin', 'creation_time', 'update_time')
    list_filter = ('type', 'origin', 'creation_time', 'update_time')

    search_fields = ('name__value', 'description__value')

    date_hierarchy = 'creation_time'

    def name_(self, obj: Form):
        return obj.name.value

    name_.admin_order_field = f'name__{"value"}'

    inlines = [IntDataPointInlineLT, FloatDataPointInlineLT]

    def get_formsets_with_inlines(self, request, indicator: Indicator = None):
        for inline in self.get_inline_instances(request, indicator):
            # hide MyInlineLT in the add view

            if indicator is not None and (not isinstance(inline, tuple([IntDataPointInlineLT, FloatDataPointInlineLT]))
                                          or inline.model is indicator.data_class()):
                yield inline.get_formset(request, indicator), inline

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(IntDataPoint, site=lab_tech_site)
class IntDataPointLabTech(admin.ModelAdmin):
    fields = ('user', 'indicator', 'time', 'value',)
    exclude = ('name', 'description', 'flags', 'source', 'validated', 'processed')

    list_display = ('first_name', 'last_name', 'indicator_', 'time', 'value')
    list_filter = ('indicator', 'time')

    search_fields = ('indicator__name__value', 'user__profile__first_name', 'user__profile__last_name')

    date_hierarchy = 'creation_time'

    def indicator_(self, obj: IntDataPoint):
        return obj.indicator.name.value

    indicator_.admin_order_field = 'indicator__name__value'

    def first_name(self, obj: IntDataPoint):
        return obj.user.profile.first_name

    first_name.admin_order_field = 'user__profile__first_name'

    def last_name(self, obj: IntDataPoint):
        return obj.user.profile.last_name

    last_name.admin_order_field = 'user__profile__last_name'

    def has_module_permission(self, request):
        return False


@admin.register(FloatDataPoint, site=lab_tech_site)
class FloatDataPointLabTech(admin.ModelAdmin):
    fields = ('user', 'indicator', 'time', 'value',)
    exclude = ('name', 'description', 'flags', 'source', 'validated', 'processed')

    list_display = ('first_name', 'last_name', 'indicator_', 'time', 'value')
    list_filter = ('indicator', 'time')

    search_fields = ('indicator__name__value', 'user__profile__first_name', 'user__profile__last_name')

    date_hierarchy = 'creation_time'

    def indicator_(self, obj: IntDataPoint):
        return obj.indicator.name.value

    indicator_.admin_order_field = 'indicator__name__value'

    def first_name(self, obj: IntDataPoint):
        return obj.user.profile.first_name

    first_name.admin_order_field = 'user__profile__first_name'

    def last_name(self, obj: IntDataPoint):
        return obj.user.profile.last_name

    last_name.admin_order_field = 'user__profile__last_name'

    def has_module_permission(self, request):
        return False