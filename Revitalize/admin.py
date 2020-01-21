from django.contrib import admin

from Revitalize.models import AnonymizedIndicator, Client, Cohort, CohortDataPoint, DataPoint, Form, Submission, Goal, Indicator

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    #list_display = ['username', 'first_name', 'middle_name', 'last_name', 'birth_date', 'gender', 'phone_number', 'email']
    #list_filter = ['username', 'first_name', 'last_name', 'birth_date', 'gender']
    #search_fields = ['username', 'first_name', 'last_name', 'birth_date', 'gender', 'phone_number', 'email']

    model = Client

    list_display = model.rm_fields_display
    list_filter = model.rm_fields_filter
    search_fields = model.rm_fields_search


admin.site.register(Cohort)
admin.site.register(Form)
admin.site.register(Submission)
admin.site.register(Indicator)
admin.site.register(DataPoint)
admin.site.register(Goal)
admin.site.register(AnonymizedIndicator)
admin.site.register(CohortDataPoint)
