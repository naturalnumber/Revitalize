from django.contrib import admin

from Revitalize.models import Profile, String, StringGroup, Text

admin.site.register(Text)
admin.site.register(String)
admin.site.register(StringGroup)
admin.site.register(Profile)
