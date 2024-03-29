from itertools import chain

from rest_framework import serializers
from rest_framework.serializers import ListSerializer

from Revitalize.models import *
from Revitalize.language_support import database_to_string as _str
from Revitalize.utils import ModelHelper


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}


# Basic string implementations


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


# Short Implementations


class FormSerializerShort(serializers.ModelSerializer):
    name = StringSerializer(many=False)
    description = TextSerializer(many=False)

    class Meta:
        model = Form
        fields = ['name', 'description', 'type']


# Basic Profile implementations


class AddressSerializer(serializers.ModelSerializer):
    street_address = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    province = serializers.SerializerMethodField()
    postal_code = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = ModelHelper.serialize(model.__name__)
        fields.extend(["id", "street_address", "city", "province", "postal_code", "country"])

    def get_street_address(self, a: Address):
        return a.address.street_address

    def get_city(self, a: Address):
        return a.address.city

    def get_province(self, a: Address):
        return a.address.province

    def get_postal_code(self, a: Address):
        return a.address.postal_code

    def get_country(self, a: Address):
        return a.country


class CanadianAddressSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField()

    class Meta:
        model = CanadianAddress
        fields = ModelHelper.serialize(model.__name__)
        fields.extend(["country"])

    def get_country(self, ca: CanadianAddress):
        return ca.base.country


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ModelHelper.serialize(model.__name__)
        fields.extend(['id'])


# Basic form implementations
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
    # Notable
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    # group = QuestionGroupSerializer(many=False)
    text = serializers.SerializerMethodField()
    annotations = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ModelHelper.serialize(model.__name__)

    def get_name(self, n: Notable):
        return _str(n.name)

    def get_description(self, n: Notable):
        return _str(n.description)

    def get_text(self, q: Question):
        return q.text.value

    def get_annotations(self, q: Question):
        return json.loads(_str(q.annotations)) if q.annotations is not None else None


# Elements


class TextElementSerializer(serializers.ModelSerializer):
    # Notable
    name = StringSerializer(many=False)
    description = TextSerializer(many=False)

    # form = FormSerializer(many=False)
    text = TextSerializer(many=False)

    class Meta:
        model = TextElement
        fields = ModelHelper.serialize(model.__name__)


class QuestionGroupSerializer(serializers.ModelSerializer):
    # Notable
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    # group = QuestionGroupSerializer(many=False)
    text = serializers.SerializerMethodField()
    annotations = serializers.SerializerMethodField()

    questions = QuestionSerializer(many=True)
    question_data = serializers.SerializerMethodField()

    class Meta:
        model = QuestionGroup
        fields = ModelHelper.serialize(model.__name__)
        fields.extend(['questions'])
        fields.extend(['question_data'])

    def get_name(self, n: Notable):
        return _str(n.name)

    def get_description(self, n: Notable):
        return _str(n.description)

    def get_text(self, q: QuestionGroup):
        return q.text.value

    def get_annotations(self, q: QuestionGroup):
        return json.loads(_str(q.annotations)) if q.annotations is not None else None

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
    # Notable
    name = StringSerializer(many=False)
    description = TextSerializer(many=False)

    class Meta:
        model = Form
        fields = ModelHelper.serialize(model.__name__)
        fields.extend(['id'])


class SurveySerializer(serializers.ModelSerializer):
    form = FormSerializer(many=False)

    class Meta:
        model = Survey
        fields = ModelHelper.serialize(model.__name__)
        fields.extend(['id'])


class MedicalLabSerializer(serializers.ModelSerializer):
    form = FormSerializer(many=False)

    class Meta:
        model = MedicalLab
        fields = ModelHelper.serialize(model.__name__)


# I moved available surveys to near the bottom for better organization


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


class IndicatorSerializer(serializers.ModelSerializer):
    # Notable
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Indicator
        fields = ['id', 'name', 'description']

    def get_name(self, n: Notable):
        return _str(n.name)

    def get_description(self, n: Notable):
        return _str(n.description)


class IntDataPointSerializer(serializers.ModelSerializer):
    # profile = ProfileSerializer(many=False)
    user = UserSerializer(many=False)
    indicator = IndicatorSerializer(many=False)

    class Meta:
        model = IntDataPoint
        fields = ModelHelper.serialize(model.__name__)
        fields.extend(['id'])


class FloatDataPointSerializer(serializers.ModelSerializer):
    # profile = ProfileSerializer(many=False)
    user = UserSerializer(many=False)
    indicator = IndicatorSerializer(many=False)

    class Meta:
        model = FloatDataPoint
        fields = ModelHelper.serialize(model.__name__)
        fields.extend(['id'])


# Frontend related


class QuestionSerializerDisplay(serializers.ModelSerializer):
    # Notable
    #name = serializers.SerializerMethodField()
    #description = serializers.SerializerMethodField()

    text = serializers.SerializerMethodField()
    help_text = serializers.SerializerMethodField()
    screen_reader_text = serializers.SerializerMethodField()

    annotations = serializers.SerializerMethodField()

    number = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'number', 'optional', 'text', 'help_text', 'screen_reader_text', 'annotations', 'display']

    def get_text(self, q: Question):
        return _str(q.text)

    def get_help_text(self, q: Question):
        return _str(q.help_text)

    def get_screen_reader_text(self, q: Question):
        return _str(q.screen_reader_text)

    def get_annotations(self, q: Question):
        return json.loads(_str(q.annotations)) if q.annotations is not None else None

    def get_number(self, q: Question):
        return q.prefix


class TextQuestionSerializerDisplay(serializers.ModelSerializer):
    # question = QuestionSerializer(many=False)

    class Meta:
        model = TextQuestion
        fields = ModelHelper.serialize(model.__name__)


class IntQuestionSerializerDisplay(serializers.ModelSerializer):
    # question = QuestionSerializer(many=False)

    class Meta:
        model = IntQuestion
        fields = ModelHelper.serialize(model.__name__)


class FloatQuestionSerializerDisplay(serializers.ModelSerializer):
    # question = QuestionSerializer(many=False)

    class Meta:
        model = FloatQuestion
        fields = ModelHelper.serialize(model.__name__)


class IntRangeQuestionSerializerDisplay(serializers.ModelSerializer):
    labels = serializers.SerializerMethodField()  # TODO

    annotations = serializers.SerializerMethodField()

    minimum = serializers.SerializerMethodField()
    maximum = serializers.SerializerMethodField()

    class Meta:
        model = IntRangeQuestion
        fields = ['minimum', 'maximum', 'step', 'initial', 'labels', 'annotations']

    def get_labels(self, q: IntRangeQuestion):
        if StringGroup.size(q.labels) < 2:
            vals = json.loads(q.default_labels())
        else:
            vals = json.loads(_str(q.labels))

        return vals

    def get_minimum(self, q: IntRangeQuestion):
        return q.min

    def get_maximum(self, q: IntRangeQuestion):
        return q.max

    def get_annotations(self, q: IntRangeQuestion):
        return json.loads(_str(q.group.annotations)) if q.group.annotations is not None else None


class BooleanChoiceQuestionSerializerDisplay(serializers.ModelSerializer):
    labels = serializers.SerializerMethodField()
    annotations = serializers.SerializerMethodField()

    # question = QuestionSerializer(many=False)

    class Meta:
        model = BooleanChoiceQuestion
        fields = ['initial', 'labels', 'annotations']

    def get_labels(self, q: BooleanChoiceQuestion):
        if StringGroup.size(q.labels) < 2:
            vals = json.loads(q.default_labels())
        else:
            vals = json.loads(_str(q.labels))

        return vals

    def get_annotations(self, q: BooleanChoiceQuestion):
        return json.loads(_str(q.group.annotations)) if q.group.annotations is not None else None


class ExclusiveChoiceQuestionSerializerDisplay(serializers.ModelSerializer):
    labels = serializers.SerializerMethodField()
    annotations = serializers.SerializerMethodField()

    # question = QuestionSerializer(many=False) TODO

    class Meta:
        model = ExclusiveChoiceQuestion
        fields = ['labels', 'annotations']

    def get_labels(self, q: ExclusiveChoiceQuestion):
        if StringGroup.size(q.labels) < 2:
            vals = json.loads(q.default_labels())
        else:
            vals = json.loads(_str(q.labels))

        return vals

    def get_annotations(self, q: ExclusiveChoiceQuestion):
        return json.loads(_str(q.group.annotations)) if q.group.annotations is not None else None


class MultiChoiceQuestionSerializerDisplay(serializers.ModelSerializer):
    labels = StringGroupSerializer(many=False)

    # question = QuestionSerializer(many=False)

    class Meta:
        model = MultiChoiceQuestion
        fields = ModelHelper.serialize(model.__name__)


class FloatRangeQuestionSerializerDisplay(serializers.ModelSerializer):
    labels = StringGroupSerializer(many=False)

    # question = QuestionSerializer(many=False)

    class Meta:
        model = FloatRangeQuestion
        fields = ModelHelper.serialize(model.__name__)


class ElementSerializerDisplay(serializers.ModelSerializer):
    @classmethod
    def get_serializer(cls, model):
        if model == TextElement:
            return TextElementSerializerDisplay
        elif model == QuestionGroup:
            return QuestionGroupSerializerDisplay

    def to_representation(self, instance):
        serializer = self.get_serializer(instance.__class__)
        return serializer(instance, context=self.context).data


class TextElementSerializerDisplay(serializers.ModelSerializer):
    element_type = serializers.SerializerMethodField()

    text = serializers.SerializerMethodField()
    help_text = serializers.SerializerMethodField()
    screen_reader_text = serializers.SerializerMethodField()

    number = serializers.SerializerMethodField()

    class Meta:
        model = TextElement
        fields = ['id', 'element_type', 'number', 'text', 'help_text', 'screen_reader_text', 'display']

    def get_text(self, e: TextElement):
        return _str(e.text)

    def get_help_text(self, e: TextElement):
        return _str(e.help_text)

    def get_screen_reader_text(self, e: TextElement):
        return _str(e.screen_reader_text)

    def get_number(self, e: FormElement):
        return e.prefix

    def get_element_type(self, e: FormElement):
        return e.element_type


class QuestionGroupSerializerDisplay(serializers.ModelSerializer):
    element_type = serializers.SerializerMethodField()

    text = serializers.SerializerMethodField()
    help_text = serializers.SerializerMethodField()
    screen_reader_text = serializers.SerializerMethodField()

    number = serializers.SerializerMethodField()

    question_group_type = serializers.SerializerMethodField()

    question_group_type_data = serializers.SerializerMethodField()

    number_of_questions = serializers.SerializerMethodField()

    questions = serializers.SerializerMethodField()

    class Meta:
        model = QuestionGroup
        fields = ['id', 'element_type', 'number', 'text', 'help_text', 'screen_reader_text', 'question_group_type',
                  'question_group_type_data', 'display', 'number_of_questions', 'questions']

    def get_text(self, e: QuestionGroup):
        return _str(e.text)

    def get_help_text(self, e: QuestionGroup):
        return _str(e.help_text)

    def get_screen_reader_text(self, e: QuestionGroup):
        return _str(e.screen_reader_text)

    def get_annotations(self, e: QuestionGroup):
        return json.loads(_str(e.annotations)) if e.annotations is not None else None

    def get_number(self, e: FormElement):
        return e.prefix

    def get_element_type(self, e: FormElement):
        return e.element_type

    def get_question_group_type(self, qg: QuestionGroup):
        return qg.data_class().question_group_type

    def get_number_of_questions(self, qg: QuestionGroup):
        return qg.questions.count()

    def get_questions(self, qg: QuestionGroup):
        questions = sorted(Question.objects.filter(group=qg.pk).all(), key= lambda q: q.number)
        ser = QuestionSerializerDisplay(questions, many=True)
        return ser.data

    def get_question_group_type_data(self, qg: QuestionGroup):  # TODO
        data = qg.data()

        serializer = None

        if data is not None:
            if qg.type is qg.DataType.TEXT.value:
                serializer = TextQuestionSerializerDisplay(data, many=False)
            elif qg.type is qg.DataType.INT.value:
                serializer = IntQuestionSerializerDisplay(data, many=False)
            elif qg.type is qg.DataType.FLOAT.value:
                serializer = FloatQuestionSerializerDisplay(data, many=False)
            elif qg.type is qg.DataType.INT_RANGE.value:
                serializer = IntRangeQuestionSerializerDisplay(data, many=False)
            elif qg.type is qg.DataType.BOOLEAN.value:
                serializer = BooleanChoiceQuestionSerializerDisplay(data, many=False)
            elif qg.type is qg.DataType.EXCLUSIVE.value:
                serializer = ExclusiveChoiceQuestionSerializerDisplay(data, many=False)
            elif qg.type is qg.DataType.CHOICES.value:
                serializer = MultiChoiceQuestionSerializerDisplay(data, many=False)
            elif qg.type is qg.DataType.FLOAT_RANGE.value:
                serializer = FloatRangeQuestionSerializerDisplay(data, many=False)

        #annotations = self.get_annotations(qg)

        return serializer.data if serializer is not None else None


class FormSerializerDisplay(serializers.ModelSerializer):
    # Notable
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    elements = serializers.SerializerMethodField()

    class Meta:
        model = Form
        fields = ['id', 'name', 'description', 'type', 'display', 'elements']

    def get_name(self, n: Notable):
        return _str(n.name)

    def get_description(self, n: Notable):
        return _str(n.description)

    def get_elements(self, f: Form):
        elements = sorted(chain(f.text_elements.order_by('number').all(),
                                f.question_groups.order_by('number').all()),
                          key=lambda e: e.number
                          )

        # print(elements)

        ser = ElementSerializerDisplay(elements, many=True)

        # print(ser.is_valid())

        return ser.data

        # elements = []
        #
        # text_elements = f.text_elements.order_by('number').all()
        #
        # for te in text_elements:
        #     print(te)
        #     elements.append((te.number, TextElementSerializerDisplay(te, many=False).data))
        #     print(f"te #{te.number} = {TextElementSerializerDisplay(te, many=False).data}")
        #
        # question_groups = f.question_groups.order_by('number').all()
        #
        # for qg in question_groups:
        #     print(qg)
        #     elements.append((qg.number, QuestionGroupSerializerDisplay(qg, many=False).data))
        #     print(f"te #{qg.number} = {QuestionGroupSerializerDisplay(qg, many=False).data}")

        #elements.sort(key=lambda e: e[0])

        #serialized_elements = [str(e[0]) for e in elements]

        #serialized = "["

        #for s in serialized_elements:
         #   serialized += s
         #   serialized += ','

        #serialized += ']'

        #return "test" # serialized


class SurveySerializerDisplay(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    display = serializers.SerializerMethodField()
    elements = serializers.SerializerMethodField()

    class Meta:
        model = Survey
        fields = ['id', 'name', 'description', 'type', 'display', 'elements']

    def get_id(self, s: Survey):
        return s.form.id

    def get_name(self, s: Survey):
        return _str(s.form.name)

    def get_description(self, s: Survey):
        return _str(s.form.description)

    def get_type(self, s: Survey):
        return s.form.type

    def get_display(self, s: Survey):
        return s.form.display

    def get_elements(self, s: Survey):
        f = s.form

        elements = []

        text_elements = f.text_elements.order_by('number').all()

        for te in text_elements:
            elements.append((te.number, TextElementSerializerDisplay(te, many=False)))

        question_groups = f.question_groups.order_by('number').all()

        for qg in question_groups:
            elements.append((qg.number, QuestionGroupSerializerDisplay(qg, many=False)))

        elements.sort(key=lambda e: e[0])

        return ListSerializer([e[1] for e in elements])


class AbstractDataPointSerializerDisplay(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    indicator_id = serializers.SerializerMethodField()
    indicator_data = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    submission_date = serializers.SerializerMethodField()

    class Meta:
        fields = ['id', 'time', 'value', 'type', 'validated', 'processed', 'indicator_id', 'name',
                  'indicator_data', 'submission_date']

    def get_name(self, p: FloatDataPoint):
        return _str(p.indicator.name)

    def get_type(self, p: FloatDataPoint):
        return p.indicator.type

    def get_indicator_id(self, p: FloatDataPoint):
        return p.indicator_id

    def get_indicator_data(self, p: FloatDataPoint):
        return p.indicator.get_basic_info()

    def get_submission_date(self, p: FloatDataPoint):
        return p.time.date().isoformat()


class IntDataPointSerializerDisplay(AbstractDataPointSerializerDisplay):
    class Meta:
        model = IntDataPoint
        fields = ['id', 'time', 'submission_date', 'value', 'type', 'name', 'indicator_id', 'indicator_data',
                  'validated', 'processed']


class FloatDataPointSerializerDisplay(AbstractDataPointSerializerDisplay):
    class Meta:
        model = FloatDataPoint
        fields = ['id', 'time', 'submission_date', 'value', 'type', 'name', 'indicator_id', 'indicator_data',
                  'validated', 'processed']


class DataPointSerializerDisplay(serializers.ModelSerializer):
    @classmethod
    def get_serializer(cls, model):
        if model == IntDataPoint:
            return IntDataPointSerializerDisplay
        elif model == FloatDataPoint:
            return FloatDataPointSerializerDisplay

    def to_representation(self, instance):
        serializer = self.get_serializer(instance.__class__)
        return serializer(instance, context=self.context).data


class IntDataPointSerializerDisplayBasic(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = IntDataPoint
        fields = ['id', 'time', 'value', 'type']

    def get_type(self, p: FloatDataPoint):
        return p.indicator.type


class FloatDataPointSerializerDisplayBasic(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = FloatDataPoint
        fields = ['id', 'time', 'value', 'type']

    def get_type(self, p: FloatDataPoint):
        return p.indicator.type


class DataPointSerializerDisplayBasic(serializers.ModelSerializer):
    @classmethod
    def get_serializer(cls, model):
        if model == IntDataPoint:
            return IntDataPointSerializerDisplayBasic
        elif model == FloatDataPoint:
            return FloatDataPointSerializerDisplayBasic

    def to_representation(self, instance):
        serializer = self.get_serializer(instance.__class__)
        return serializer(instance, context=self.context).data

# Endpoint related


class UserSubmissionHistorySerializer(serializers.ModelSerializer):
    submission_id = serializers.SerializerMethodField()
    survey_id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    alt_survey_id = serializers.SerializerMethodField()
    results = serializers.SerializerMethodField()
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", default_timezone=None)

    class Meta:
        model = Submission
        fields = ['submission_id', 'time', 'validated', 'parsed', 'processed', 'survey_id', 'name', 'description',
                  'alt_survey_id', 'results', 'submitter']

    def get_name(self, s: Submission):
        return _str(s.form.name)

    def get_description(self, s: Submission):
        return _str(s.form.description)

    def get_submission_id(self, s: Submission):
        return s.id

    def get_survey_id(self, s: Submission):
        return s.form.id

    def get_alt_survey_id(self, s: Submission):
        return s.id

    def get_results(self, s: Submission):
        data_points = chain(s.int_data_points.all(),
                             s.float_data_points.all())

        ser = DataPointSerializerDisplay(data_points, many=True)

        return ser.data


class AvailableSurveySerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    alt_id = serializers.SerializerMethodField()

    class Meta:
        model = Form
        fields = ['id', 'name', 'description', 'alt_id']

    def get_name(self, s: Form):
        return _str(s.name)

    def get_description(self, s: Form):
        return _str(s.description)

    def get_id(self, s: Form):
        return s.id

    def get_alt_id(self, s: Form):
        survey = None
        try:
            survey = s.get_survey()
        except:
            pass
        return survey.id if survey is not None else -1

# class AvailableSurveySerializer(serializers.ModelSerializer):
#     id = serializers.SerializerMethodField()
#     name = serializers.SerializerMethodField()
#     description = serializers.SerializerMethodField()
#     alt_id = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Survey
#         fields = ['id', 'name', 'description', 'alt_id']
#
#     def get_name(self, s: Survey):
#         #name_serializer = StringSerializer(s.form.name, many=False)
#         return _str(s.form.name)
#
#     def get_description(self, s: Survey):
#         #description_serializer = TextSerializer(s.form.description, many=False)
#         return _str(s.form.description)
#
#     def get_id(self, s: Survey):
#         return s.form.id
#
#     def get_alt_id(self, s: Survey):
#         return s.id


class ProfileRetrievalSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=False)
    height = serializers.SerializerMethodField()
    weight = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'first_name', 'middle_name', 'last_name', 'date_of_birth', 'gender', 'phone_number',
                  'phone_number_alt', 'email', 'address', 'ec_first_name', 'ec_middle_name', 'ec_last_name',
                  'ec_phone_number', 'physician', 'points', 'personal_message', 'profile_picture', 'password_flag',
                  'preferences', 'height', 'weight']

    def get_height(self, p: Profile) -> float:
        return p.get_height()

    def get_weight(self, p: Profile) -> float:
        return p.get_weight()


class UserIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = ModelHelper.serialize(model.__name__)


class UserIndicatorDataSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    class Meta:
        model = Indicator
        fields = ['id', 'name', 'description', 'data']


    def get_data(self, i: Indicator):
        data_points = chain(i.int_data_points.all(), i.float_data_points.all())

        ser = DataPointSerializerDisplay(data_points, many=True)

        return ser.data



# class FormSerializerDisplay2(serializers.ModelSerializer):
#     name = StringSerializer(many=False)
#     description = TextSerializer(many=False)
#     elements = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Form
#         fields = ['id', 'name', 'description', 'type', 'display', 'elements']
#
#     def get_elements(self, f: Form):
#
#         elements = []
#
#         text_elements = f.text_elements.order_by('number').all()
#
#         for te in text_elements:
#             print(te)
#             elements.append((te.number, TextElementSerializerDisplay(te, many=False).data))
#             print(f"te-#{te.number} = {TextElementSerializerDisplay(te, many=False).data}")
#
#         question_groups = f.question_groups.order_by('number').all()
#
#         for qg in question_groups:
#             print(qg)
#             elements.append((qg.number, QuestionGroupSerializerDisplay(qg, many=False).data))
#             print(f"qg-#{qg.number} = {QuestionGroupSerializerDisplay(qg, many=False).data}")
#
#         elements.sort(key=lambda e: e[0])
#
#         serialized_elements = [e[1] for e in elements]
#
#         serialized = "["
#
#         for s in serialized_elements:
#             serialized += s
#             serialized += ','
#
#         serialized += ']'
#
#         return serialized