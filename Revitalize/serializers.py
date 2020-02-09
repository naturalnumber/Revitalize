from rest_framework import serializers

from Revitalize.models import *


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


class AddressSerializer(serializers.ModelSerializer):
    street_address = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    province = serializers.SerializerMethodField()
    postal_code = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = ModelHelper.serialize(model.__name__)
        fields.extend(["street_address", "city", "province", "postal_code"])

    def get_street_address(self, a: Address):
        return a.address.street_address

    def get_city(self, a: Address):
        return a.address.city

    def get_province(self, a: Address):
        return a.address.province

    def get_postal_code(self, a: Address):
        return a.address.postal_code


class CanadianAddressSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField()

    class Meta:
        model = CanadianAddress
        fields = ModelHelper.serialize(model.__name__)
        fields.extend(["country"])

    def get_country(self, ca: CanadianAddress):
        return ca.base.country


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Profile
        fields = ModelHelper.serialize(model.__name__)
        fields.extend(['id'])


# Question Types


class TextQuestionSerializer(serializers.ModelSerializer):
    # question = QuestionSerializer(many=False)

    class Meta:
        model = TextQuestion
        fields = ModelHelper.serialize(model.__name__)


class IntQuestionSerializer(serializers.ModelSerializer):
    # question = QuestionSerializer(many=False)

    class Meta:
        model = IntQuestion
        fields = ModelHelper.serialize(model.__name__)


class FloatQuestionSerializer(serializers.ModelSerializer):
    # question = QuestionSerializer(many=False)

    class Meta:
        model = FloatQuestion
        fields = ModelHelper.serialize(model.__name__)


class IntRangeQuestionSerializer(serializers.ModelSerializer):
    labels = StringGroupSerializer(many=False)

    # question = QuestionSerializer(many=False)

    class Meta:
        model = IntRangeQuestion
        fields = ModelHelper.serialize(model.__name__)


class BooleanChoiceQuestionSerializer(serializers.ModelSerializer):
    labels = StringGroupSerializer(many=False)

    # question = QuestionSerializer(many=False)

    class Meta:
        model = BooleanChoiceQuestion
        fields = ModelHelper.serialize(model.__name__)


class ExclusiveChoiceQuestionSerializer(serializers.ModelSerializer):
    labels = StringGroupSerializer(many=False)

    # question = QuestionSerializer(many=False)

    class Meta:
        model = ExclusiveChoiceQuestion
        fields = ModelHelper.serialize(model.__name__)


class MultiChoiceQuestionSerializer(serializers.ModelSerializer):
    labels = StringGroupSerializer(many=False)

    # question = QuestionSerializer(many=False)

    class Meta:
        model = MultiChoiceQuestion
        fields = ModelHelper.serialize(model.__name__)


class FloatRangeQuestionSerializer(serializers.ModelSerializer):
    labels = StringGroupSerializer(many=False)

    # question = QuestionSerializer(many=False)

    class Meta:
        model = FloatRangeQuestion
        fields = ModelHelper.serialize(model.__name__)


# Questions


class QuestionSerializer(serializers.ModelSerializer):
    # Nameable
    name = StringSerializer(many=False)
    description = TextSerializer(many=False)

    # group = QuestionGroupSerializer(many=False)
    text = TextSerializer(many=False)
    annotations = StringGroupSerializer(many=False)

    class Meta:
        model = Question
        fields = ModelHelper.serialize(model.__name__)


# Elements


class TextElementSerializer(serializers.ModelSerializer):
    # Nameable
    name = StringSerializer(many=False)
    description = TextSerializer(many=False)

    # form = FormSerializer(many=False)
    text = TextSerializer(many=False)

    class Meta:
        model = TextElement
        fields = ModelHelper.serialize(model.__name__)


class QuestionGroupSerializer(serializers.ModelSerializer):
    # Nameable
    name = StringSerializer(many=False)
    description = TextSerializer(many=False)

    # form = FormSerializer(many=False)
    text = TextSerializer(many=False)
    annotations = StringGroupSerializer(many=False)
    questions = QuestionSerializer(many=True)
    question_data = serializers.SerializerMethodField()

    class Meta:
        model = QuestionGroup
        fields = ModelHelper.serialize(model.__name__)
        fields.extend(['questions'])
        fields.extend(['question_data'])

    def get_question_data(self, qg: QuestionGroup):
        data = qg.data()

        serializer = None

        if data is not None:
            if qg.type is qg.DataType.TEXT.value:
                serializer = TextQuestionSerializer(data, many=False)
            elif qg.type is qg.DataType.INT.value:
                serializer = IntQuestionSerializer(data, many=False)
            elif qg.type is qg.DataType.FLOAT.value:
                serializer = FloatQuestionSerializer(data, many=False)
            elif qg.type is qg.DataType.INT_RANGE.value:
                serializer = IntRangeQuestionSerializer(data, many=False)
            elif qg.type is qg.DataType.BOOLEAN.value:
                serializer = BooleanChoiceQuestionSerializer(data, many=False)
            elif qg.type is qg.DataType.EXCLUSIVE.value:
                serializer = ExclusiveChoiceQuestionSerializer(data, many=False)
            elif qg.type is qg.DataType.CHOICES.value:
                serializer = MultiChoiceQuestionSerializer(data, many=False)
            elif qg.type is qg.DataType.FLOAT_RANGE.value:
                serializer = FloatRangeQuestionSerializer(data, many=False)

        return serializer.data if serializer is not None else None


# Forms


class FormSerializer(serializers.ModelSerializer):
    # Nameable
    name = StringSerializer(many=False)
    description = TextSerializer(many=False)

    class Meta:
        model = Form
        fields = ModelHelper.serialize(model.__name__)
        fields.extend(['id'])


class FormSerializerShort(serializers.ModelSerializer):
    name = StringSerializer(many=False)
    description = TextSerializer(many=False)

    class Meta:
        model = Form
        fields = ['name', 'description', 'type']


class FormSerializerDisplay(serializers.ModelSerializer):
    name = StringSerializer(many=False)
    description = TextSerializer(many=False)
    question_groups = QuestionGroupSerializer(many=True)

    class Meta:
        model = Form
        fields = ['name', 'description', 'type', 'display', 'question_groups']


class SurveySerializer(serializers.ModelSerializer):
    form = FormSerializerDisplay(many=False)

    class Meta:
        model = Survey
        fields = ModelHelper.serialize(model.__name__)


class AvailableSurveySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Survey
        fields = ['id', 'name', 'description', 'form_id']

    def get_name(self, s: Survey):
        name_serializer = StringSerializer(s.form.name, many=False)
        return name_serializer.data

    def get_description(self, s: Survey):
        description_serializer = TextSerializer(s.form.description, many=False)
        return description_serializer.data

    def get_form_id(self, s: Survey):
        return s.form.id


# Submissions


class SubmissionSerializer(serializers.ModelSerializer):
    # profile = ProfileSerializer(many=False)
    user = UserSerializer(many=False)
    form = FormSerializer(many=False)

    class Meta:
        model = Submission
        fields = ModelHelper.serialize(model.__name__)
        fields.extend(['id'])


class TextResponseSerializer(serializers.ModelSerializer):
    submission = SubmissionSerializer(many=False)

    class Meta:
        model = TextResponse
        fields = ModelHelper.serialize(model.__name__)


class IntResponseSerializer(serializers.ModelSerializer):
    submission = SubmissionSerializer(many=False)

    class Meta:
        model = IntResponse
        fields = ModelHelper.serialize(model.__name__)


class FloatResponseSerializer(serializers.ModelSerializer):
    submission = SubmissionSerializer(many=False)

    class Meta:
        model = FloatResponse
        fields = ModelHelper.serialize(model.__name__)
