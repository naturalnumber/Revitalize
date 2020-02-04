from django.contrib.auth.models import User
from rest_framework import serializers

from Revitalize.models import String, ModelHelper, Text, StringGroup, Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}


class StringSerializer(serializers.ModelSerializer):

    class Meta:
        model = String
        fields = ModelHelper.serialize(model.__name__)


class TextSerializer(serializers.ModelSerializer):

    class Meta:
        model = Text
        fields = ModelHelper.serialize(model.__name__)


class StringGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = StringGroup
        fields = ModelHelper.serialize(model.__name__)


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ModelHelper.serialize(model.__name__)