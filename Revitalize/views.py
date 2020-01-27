from django.shortcuts import render
from rest_framework import viewsets

from Revitalize.models import Profile
from Revitalize.serializers import ProfileSerializer


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
