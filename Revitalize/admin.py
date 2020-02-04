from django.contrib import admin

from Revitalize.models import Form, Question, IntRangeQuestion, IntRangeResponse, Profile, QuestionGroup, String, \
    StringGroup, \
    Submission, Survey, Text, TextQuestion, TextResponse, TextElement, IntQuestion, FloatQuestion, \
    ExclusiveChoiceQuestion, MultiChoiceQuestion, IntResponse, FloatResponse, ExclusiveChoiceResponse, \
    MultiChoiceResponse

admin.site.register(Text)
admin.site.register(String)
admin.site.register(StringGroup)
admin.site.register(Profile)
admin.site.register(Form)
admin.site.register(Survey)
admin.site.register(TextElement)
admin.site.register(QuestionGroup)
admin.site.register(Question)
admin.site.register(TextQuestion)
admin.site.register(IntQuestion)
admin.site.register(FloatQuestion)
admin.site.register(IntRangeQuestion)
admin.site.register(ExclusiveChoiceQuestion)
admin.site.register(MultiChoiceQuestion)
admin.site.register(Submission)
admin.site.register(TextResponse)
admin.site.register(IntResponse)
admin.site.register(FloatResponse)
admin.site.register(IntRangeResponse)
admin.site.register(ExclusiveChoiceResponse)
admin.site.register(MultiChoiceResponse)
