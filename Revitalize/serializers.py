from rest_framework import serializers

from Revitalize.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    # cohorts = CohortSerializer(many=True)
    # submissions = SubmissionSerializer(many=True)
    # data_points = DataPointSerializer(many=True)
    # goals = GoalSerializer(many=True)

    class Meta:
        model = Profile
        fields = model.rm_fields_serialize
        # fields.extend(['cohorts', 'submissions', 'data_points', 'goals'])