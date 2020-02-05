from django.contrib import admin

from Revitalize.models import BooleanChoiceQuestion, BooleanChoiceResponse, ExclusiveChoiceQuestion, \
    ExclusiveChoiceResponse, FloatQuestion, FloatRangeQuestion, FloatRangeResponse, FloatResponse, Form, IntQuestion, \
    IntRangeQuestion, IntRangeResponse, IntResponse, MultiChoiceQuestion, MultiChoiceResponse, Profile, Question, \
    QuestionGroup, String, StringGroup, Submission, Survey, Text, TextElement, TextQuestion, TextResponse

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
admin.site.register(FloatRangeQuestion)
admin.site.register(BooleanChoiceQuestion)
admin.site.register(ExclusiveChoiceQuestion)
admin.site.register(MultiChoiceQuestion)
admin.site.register(Submission)
admin.site.register(TextResponse)
admin.site.register(IntResponse)
admin.site.register(FloatResponse)
admin.site.register(IntRangeResponse)
admin.site.register(FloatRangeResponse)
admin.site.register(BooleanChoiceResponse)
admin.site.register(ExclusiveChoiceResponse)
admin.site.register(MultiChoiceResponse)
