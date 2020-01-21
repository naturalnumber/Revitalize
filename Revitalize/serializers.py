from rest_framework import serializers

from Revitalize.models import AnonymizedIndicator, Client, Cohort, CohortDataPoint, DataPoint, Form, Goal, Indicator, \
    Submission


class ClientSerializer(serializers.ModelSerializer):
    # cohorts = CohortSerializer(many=True)
    # submissions = SubmissionSerializer(many=True)
    # data_points = DataPointSerializer(many=True)
    # goals = GoalSerializer(many=True)

    class Meta:
        model = Client
        fields = model.rm_fields_serialize
        # fields.extend(['cohorts', 'submissions', 'data_points', 'goals'])


class CohortSerializer(serializers.ModelSerializer):
    clients = ClientSerializer(many=True)

    class Meta:
        model = Cohort
        fields = model.rm_fields_serialize
        fields.append('clients')


class FormSerializer(serializers.ModelSerializer):
    # submissions = SubmissionSerializer(many=True)

    class Meta:
        model = Form
        fields = model.rm_fields_serialize
        # fields.extend(['submissions'])


class SubmissionSerializer(serializers.ModelSerializer):
    client = ClientSerializer(many=False)
    form = FormSerializer(many=False)

    class Meta:
        model = Submission
        fields = model.rm_fields_serialize
        fields.extend(['client', 'form'])


class IndicatorSerializer(serializers.ModelSerializer):
    # data_points = DataPointSerializer(many=True)
    # goals = GoalSerializer(many=True)
    # a_indicators = AnonymizedIndicatorSerializer(many=True)

    class Meta:
        model = Indicator
        fields = model.rm_fields_serialize
        # fields.extend(['data_points', 'goals', 'a_indicators'])


class DataPointSerializer(serializers.ModelSerializer):
    client = ClientSerializer(many=False)
    indicator = IndicatorSerializer(many=False)

    class Meta:
        model = DataPoint
        fields = model.rm_fields_serialize
        fields.extend(['client', 'indicator'])


class GoalSerializer(serializers.ModelSerializer):
    client = ClientSerializer(many=False)
    indicator = IndicatorSerializer(many=False)

    class Meta:
        model = Goal
        fields = model.rm_fields_serialize
        fields.extend(['client', 'indicator'])


class AnonymizedIndicatorSerializer(serializers.ModelSerializer):
    indicator = IndicatorSerializer(many=False)
    # c_data_points = CohortDataPointSerializer(many=True)

    class Meta:
        model = AnonymizedIndicator
        fields = model.rm_fields_serialize
        fields.append('indicator')
        #cfields.extend(['c_data_points'])


class CohortDataPointSerializer(serializers.ModelSerializer):
    cohort = CohortSerializer(many=False)
    a_indicator = AnonymizedIndicatorSerializer(many=False)

    class Meta:
        model = CohortDataPoint
        fields = model.rm_fields_serialize
        fields.extend(['cohort', 'a_indicator'])
