from rest_framework import viewsets

from Revitalize.models import Profile, String, StringGroup, Text
from Revitalize.serializers import ProfileSerializer, StringGroupSerializer, StringSerializer, TextSerializer


class StringViewSet(viewsets.ModelViewSet):
    _model = String
    serializer_class = StringSerializer
    queryset = _model.objects.all()


class TextViewSet(viewsets.ModelViewSet):
    _model = Text
    serializer_class = TextSerializer
    queryset = _model.objects.all()


class StringGroupViewSet(viewsets.ModelViewSet):
    _model = StringGroup
    serializer_class = StringGroupSerializer
    queryset = _model.objects.all()


class ProfileViewSet(viewsets.ModelViewSet):
    _model = Profile
    serializer_class = ProfileSerializer
    queryset = _model.objects.all()
