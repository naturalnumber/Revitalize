from rest_framework import viewsets

from Revitalize.models import AnonymizedIndicator, Client, Cohort, CohortDataPoint, DataPoint, Form, Goal, Indicator, \
    Submission
from Revitalize.serializers import AnonymizedIndicatorSerializer, ClientSerializer, CohortDataPointSerializer, \
    CohortSerializer, DataPointSerializer, FormSerializer, GoalSerializer, IndicatorSerializer, SubmissionSerializer


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class CohortViewSet(viewsets.ModelViewSet):
    serializer_class = CohortSerializer
    queryset = Cohort.objects.all()


class FormViewSet(viewsets.ModelViewSet):
    serializer_class = FormSerializer
    queryset = Form.objects.all()


class SubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all()


class IndicatorViewSet(viewsets.ModelViewSet):
    serializer_class = IndicatorSerializer
    queryset = Indicator.objects.all()


class DataPointViewSet(viewsets.ModelViewSet):
    serializer_class = DataPointSerializer
    queryset = DataPoint.objects.all()


class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    queryset = Goal.objects.all()


class AnonymizedIndicatorViewSet(viewsets.ModelViewSet):
    serializer_class = AnonymizedIndicatorSerializer
    queryset = AnonymizedIndicator.objects.all()


class CohortDataPointViewSet(viewsets.ModelViewSet):
    serializer_class = CohortDataPointSerializer
    queryset = CohortDataPoint.objects.all()
