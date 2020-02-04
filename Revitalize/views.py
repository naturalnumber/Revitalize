from django.contrib.auth.models import User
from rest_framework import viewsets

from Revitalize.models import Profile, String, StringGroup, Text, Form, Survey, QuestionGroup, Question, TextQuestion, \
    IntRangeQuestion, Submission, IntRangeResponse, TextResponse, TextElement, IntQuestion, FloatQuestion, \
    ExclusiveChoiceQuestion, MultiChoiceQuestion, IntResponse, FloatResponse, ExclusiveChoiceResponse, \
    MultiChoiceResponse
from Revitalize.serializers import ProfileSerializer, StringGroupSerializer, StringSerializer, TextSerializer, \
    UserSerializer, FormSerializer, SurveySerializer, QuestionSerializer, InputSerializer, TextQuestionSerializer, \
    IntRangeQuestionSerializer, SubmissionSerializer, IntRangeResponseSerializer, TextResponseSerializer, \
    QuestionGroupSerializer, TextElementSerializer, IntQuestionSerializer, FloatQuestionSerializer, \
    ExclusiveChoiceQuestionSerializer, MultiChoiceQuestionSerializer, IntResponseSerializer, FloatResponseSerializer, \
    ExclusiveChoiceResponseSerializer, MultiChoiceResponseSerializer


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


class FormViewSet(viewsets.ModelViewSet):
    _model = Form
    serializer_class = FormSerializer
    queryset = _model.objects.all()


class SurveyViewSet(viewsets.ModelViewSet):
    _model = Survey
    serializer_class = SurveySerializer
    queryset = _model.objects.all()


class TextElementViewSet(viewsets.ModelViewSet):
    _model = TextElement
    serializer_class = TextElementSerializer
    queryset = _model.objects.all()


class QuestionGroupViewSet(viewsets.ModelViewSet):
    _model = QuestionGroup
    serializer_class = QuestionGroupSerializer
    queryset = _model.objects.all()


class QuestionViewSet(viewsets.ModelViewSet):
    _model = Question
    serializer_class = QuestionSerializer
    queryset = _model.objects.all()


class TextQuestionViewSet(viewsets.ModelViewSet):
    _model = TextQuestion
    serializer_class = TextQuestionSerializer
    queryset = _model.objects.all()


class IntQuestionViewSet(viewsets.ModelViewSet):
    _model = IntQuestion
    serializer_class = IntQuestionSerializer
    queryset = _model.objects.all()


class FloatQuestionViewSet(viewsets.ModelViewSet):
    _model = FloatQuestion
    serializer_class = FloatQuestionSerializer
    queryset = _model.objects.all()


class IntRangeQuestionViewSet(viewsets.ModelViewSet):
    _model = IntRangeQuestion
    serializer_class = IntRangeQuestionSerializer
    queryset = _model.objects.all()


class ExclusiveChoiceQuestionViewSet(viewsets.ModelViewSet):
    _model = ExclusiveChoiceQuestion
    serializer_class = ExclusiveChoiceQuestionSerializer
    queryset = _model.objects.all()


class MultiChoiceQuestionViewSet(viewsets.ModelViewSet):
    _model = MultiChoiceQuestion
    serializer_class = MultiChoiceQuestionSerializer
    queryset = _model.objects.all()


class SubmissionViewSet(viewsets.ModelViewSet):
    _model = Submission
    serializer_class = SubmissionSerializer
    queryset = _model.objects.all()


class TextResponseViewSet(viewsets.ModelViewSet):
    _model = TextResponse
    serializer_class = TextResponseSerializer
    queryset = _model.objects.all()


class IntResponseViewSet(viewsets.ModelViewSet):
    _model = IntResponse
    serializer_class = IntResponseSerializer
    queryset = _model.objects.all()


class FloatResponseViewSet(viewsets.ModelViewSet):
    _model = FloatResponse
    serializer_class = FloatResponseSerializer
    queryset = _model.objects.all()


class IntRangeResponseViewSet(viewsets.ModelViewSet):
    _model = IntRangeResponse
    serializer_class = IntRangeResponseSerializer
    queryset = _model.objects.all()


class ExclusiveChoiceResponseViewSet(viewsets.ModelViewSet):
    _model = ExclusiveChoiceResponse
    serializer_class = ExclusiveChoiceResponseSerializer
    queryset = _model.objects.all()


class MultiChoiceResponseViewSet(viewsets.ModelViewSet):
    _model = MultiChoiceResponse
    serializer_class = MultiChoiceResponseSerializer
    queryset = _model.objects.all()
