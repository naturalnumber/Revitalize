from django.contrib.auth.models import User
from rest_framework import viewsets

from Revitalize.models import Profile, String, StringGroup, Text
from Revitalize.serializers import ProfileSerializer, StringGroupSerializer, StringSerializer, TextSerializer, \
    UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class StringViewSet(viewsets.ModelViewSet):
    _model = String
    queryset = _model.objects.all()
    serializer_class = StringSerializer


class TextViewSet(viewsets.ModelViewSet):
    _model = Text
    queryset = _model.objects.all()
    serializer_class = TextSerializer


class StringGroupViewSet(viewsets.ModelViewSet):
    _model = StringGroup
    queryset = _model.objects.all()
    serializer_class = StringGroupSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    _model = Profile
    queryset = _model.objects.all()
    serializer_class = ProfileSerializer
