from django.contrib.admin import AdminSite

from Revitalize.models import *


class AdminsSite(AdminSite):
    site_header = 'Admin Administration'


admin_site = AdminsSite(name='admin_site')

admin_site.register(Text)
admin_site.register(String)
admin_site.register(StringGroup)
admin_site.register(Address)
admin_site.register(CanadianAddress)
# admin_site.register(Profile)
admin_site.register(Form)
admin_site.register(Survey)
admin_site.register(MedicalLab)
admin_site.register(TextElement)
admin_site.register(QuestionGroup)
admin_site.register(Question)
admin_site.register(TextQuestion)
admin_site.register(IntQuestion)
admin_site.register(FloatQuestion)
admin_site.register(IntRangeQuestion)
admin_site.register(FloatRangeQuestion)
admin_site.register(BooleanChoiceQuestion)
admin_site.register(ExclusiveChoiceQuestion)
admin_site.register(MultiChoiceQuestion)
admin_site.register(Submission)
admin_site.register(TextResponse)
admin_site.register(IntResponse)
admin_site.register(FloatResponse)
admin_site.register(Indicator)
admin_site.register(IntDataPoint)
admin_site.register(FloatDataPoint)


class LabTechSite(AdminSite):
    site_header = 'Lab Tech Administration'


lab_tech_site = LabTechSite(name='labtech_site')


lab_tech_site.register(Profile)
