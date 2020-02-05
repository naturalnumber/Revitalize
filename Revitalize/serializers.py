from django.contrib.auth.models import User
from rest_framework import serializers

from Revitalize.models import BooleanChoiceQuestion, BooleanChoiceResponse, ExclusiveChoiceQuestion, \
    ExclusiveChoiceResponse, FloatQuestion, FloatRangeQuestion, FloatRangeResponse, FloatResponse, Form, IntQuestion, \
    IntRangeQuestion, IntRangeResponse, IntResponse, ModelHelper, MultiChoiceQuestion, MultiChoiceResponse, Profile, \
    Question, QuestionGroup, String, StringGroup, Submission, Survey, Text, TextElement, TextQuestion, TextResponse


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ModelHelper.serialize(model.__name__)
        #  fields = ('id', 'value')


class StringSerializer(serializers.ModelSerializer):
    class Meta:
        model = String
        fields = ModelHelper.serialize(model.__name__)


class StringGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StringGroup
        fields = ModelHelper.serialize(model.__name__)


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Profile
        fields = ModelHelper.serialize(model.__name__)


class FormSerializer(serializers.ModelSerializer):
    name = StringSerializer(many=False)
    description = TextSerializer(many=False)

    class Meta:
        model = Form
        fields = ModelHelper.serialize(model.__name__)


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ModelHelper.serialize(model.__name__)


class TextElementSerializer(serializers.ModelSerializer):
    form = FormSerializer(many=False)
    text = TextSerializer(many=False)

    class Meta:
        model = TextElement
        fields = ModelHelper.serialize(model.__name__)


class QuestionGroupSerializer(serializers.ModelSerializer):
    form = FormSerializer(many=False)
    text = TextSerializer(many=False)
    annotations = StringGroupSerializer(many=False)

    class Meta:
        model = QuestionGroup
        fields = ModelHelper.serialize(model.__name__)


class QuestionSerializer(serializers.ModelSerializer):
    group = QuestionGroupSerializer(many=False)
    text = TextSerializer(many=False)
    annotations = StringGroupSerializer(many=False)

    class Meta:
        model = Question
        fields = ModelHelper.serialize(model.__name__)


class TextQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=False)

    class Meta:
        model = TextQuestion
        fields = ModelHelper.serialize(model.__name__)


class IntQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=False)

    class Meta:
        model = IntQuestion
        fields = ModelHelper.serialize(model.__name__)


class FloatQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=False)

    class Meta:
        model = FloatQuestion
        fields = ModelHelper.serialize(model.__name__)


class IntRangeQuestionSerializer(serializers.ModelSerializer):
    labels = StringGroupSerializer(many=False)
    question = QuestionSerializer(many=False)

    class Meta:
        model = IntRangeQuestion
        fields = ModelHelper.serialize(model.__name__)


class BooleanChoiceQuestionSerializer(serializers.ModelSerializer):
    labels = StringGroupSerializer(many=False)
    question = QuestionSerializer(many=False)

    class Meta:
        model = BooleanChoiceQuestion
        fields = ModelHelper.serialize(model.__name__)


class ExclusiveChoiceQuestionSerializer(serializers.ModelSerializer):
    labels = StringGroupSerializer(many=False)
    question = QuestionSerializer(many=False)

    class Meta:
        model = ExclusiveChoiceQuestion
        fields = ModelHelper.serialize(model.__name__)


class MultiChoiceQuestionSerializer(serializers.ModelSerializer):
    labels = StringGroupSerializer(many=False)
    question = QuestionSerializer(many=False)

    class Meta:
        model = MultiChoiceQuestion
        fields = ModelHelper.serialize(model.__name__)


class FloatRangeQuestionSerializer(serializers.ModelSerializer):
    labels = StringGroupSerializer(many=False)
    question = QuestionSerializer(many=False)

    class Meta:
        model = FloatRangeQuestion
        fields = ModelHelper.serialize(model.__name__)


class SubmissionSerializer(serializers.ModelSerializer):
    # profile = ProfileSerializer(many=False)
    user = UserSerializer(many=False)
    form = FormSerializer(many=False)

    class Meta:
        model = Submission
        fields = ModelHelper.serialize(model.__name__)


class TextResponseSerializer(serializers.ModelSerializer):
    submission = SubmissionSerializer(many=False)
    question = TextQuestionSerializer(many=False)

    class Meta:
        model = TextResponse
        fields = ModelHelper.serialize(model.__name__)


class IntResponseSerializer(serializers.ModelSerializer):
    submission = SubmissionSerializer(many=False)
    question = IntQuestionSerializer(many=False)

    class Meta:
        model = IntResponse
        fields = ModelHelper.serialize(model.__name__)


class FloatResponseSerializer(serializers.ModelSerializer):
    submission = SubmissionSerializer(many=False)
    question = FloatQuestionSerializer(many=False)

    class Meta:
        model = FloatResponse
        fields = ModelHelper.serialize(model.__name__)


class IntRangeResponseSerializer(serializers.ModelSerializer):
    submission = SubmissionSerializer(many=False)
    question = IntRangeQuestionSerializer(many=False)

    class Meta:
        model = IntRangeResponse
        fields = ModelHelper.serialize(model.__name__)


class BooleanChoiceResponseSerializer(serializers.ModelSerializer):
    submission = SubmissionSerializer(many=False)
    question = BooleanChoiceQuestionSerializer(many=False)

    class Meta:
        model = BooleanChoiceResponse
        fields = ModelHelper.serialize(model.__name__)


class ExclusiveChoiceResponseSerializer(serializers.ModelSerializer):
    submission = SubmissionSerializer(many=False)
    question = ExclusiveChoiceQuestionSerializer(many=False)

    class Meta:
        model = ExclusiveChoiceResponse
        fields = ModelHelper.serialize(model.__name__)


class MultiChoiceResponseSerializer(serializers.ModelSerializer):
    submission = SubmissionSerializer(many=False)
    question = MultiChoiceQuestionSerializer(many=False)

    class Meta:
        model = MultiChoiceResponse
        fields = ModelHelper.serialize(model.__name__)


class FloatRangeResponseSerializer(serializers.ModelSerializer):
    submission = SubmissionSerializer(many=False)
    question = TextQuestionSerializer(many=False)

    class Meta:
        model = FloatRangeResponse
        fields = ModelHelper.serialize(model.__name__)
