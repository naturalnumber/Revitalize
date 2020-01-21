from rest_framework import serializers

from Revitalize.models import AnonymizedIndicator, Client, Cohort, CohortDataPoint, DataPoint, Form, Goal, Indicator, \
    Submission


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = model.rm_fields_serialize


class CohortSerializer(serializers.ModelSerializer):
    clients = ClientSerializer(many=True)
    class Meta:
        model = Cohort
        fields = model.rm_fields_serialize


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = model.rm_fields_serialize


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = model.rm_fields_serialize


class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = model.rm_fields_serialize


class DataPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPoint
        fields = model.rm_fields_serialize


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = model.rm_fields_serialize


class AnonymizedIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymizedIndicator
        fields = model.rm_fields_serialize


class CohortDataPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = CohortDataPoint
        fields = model.rm_fields_serialize
