from django.contrib import admin

from Revitalize.models import AnonymizedIndicator, Client, Cohort, CohortDataPoint, DataPoint, Form, Goal, Indicator

admin.site.register(Client)
admin.site.register(Cohort)
admin.site.register(Form)
admin.site.register(Indicator)
admin.site.register(DataPoint)
admin.site.register(Goal)
admin.site.register(CohortDataPoint)
admin.site.register(AnonymizedIndicator)
