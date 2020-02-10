from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from Revitalize.serializers import *


# Helper methods


def _m(m: str):
    return {'message': m}


def _r(m: str, s: status):
    return ResponseType(_m(m), s)


def _ok(m: str):
    return ResponseType(_m(m), status.HTTP_200_OK)


def _bad(m: str):
    return ResponseType(_m(m), status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TextViewSet(viewsets.ModelViewSet):
    _model = Text
    queryset = _model.objects.all()
    serializer_class = TextSerializer


class StringViewSet(viewsets.ModelViewSet):
    _model = String
    queryset = _model.objects.all()
    serializer_class = StringSerializer


class StringGroupViewSet(viewsets.ModelViewSet):
    _model = StringGroup
    queryset = _model.objects.all()
    serializer_class = StringGroupSerializer


class AddressViewSet(viewsets.ModelViewSet):
    _model = Address
    queryset = _model.objects.all()
    serializer_class = AddressSerializer


class CanadianAddressViewSet(viewsets.ModelViewSet):
    _model = CanadianAddress
    queryset = _model.objects.all()
    serializer_class = CanadianAddressSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    _model = Profile
    queryset = _model.objects.all()
    serializer_class = ProfileSerializer


class FormViewSet(viewsets.ModelViewSet):
    _model = Form
    serializer_class = FormSerializer
    queryset = _model.objects.all()

    # TODO Should this be removed?
    @action(detail=True, methods=['POST'])
    def submit(self, request, pk=None):
        try:
            if 'time' not in request.data:
                return _bad("Must provide a time.")
            if 'submission_data' not in request.data:
                return _bad("Must provide submission data.")

            # Validate

            # Check for replacement

            #  user = request.user TODO
            user = User.objects.get(id=1)  # request.user.profile  # TODO

            form = Form.objects.get(id=pk)
            time = request.data['time']
            raw_data = request.data['submission_data']

            submission = Submission.objects.create(user=user, form=form, time=time, raw_data=raw_data)

            serializer = SubmissionSerializer(submission, many=False)

            response = {'message': 'Submission received', 'result': serializer.data}

            # Bad input...

            return ResponseType(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return ResponseType(_m(f"Could not parse submission ({e})"), status=status.HTTP_400_BAD_REQUEST)


class SurveyViewSet(viewsets.ModelViewSet):
    _model = Survey
    serializer_class = SurveySerializer
    queryset = _model.objects.all()

    @action(detail=True, methods=['POST'])
    def submit(self, request, pk=None):
        try:
            if 'time' not in request.data:
                return _bad("Must provide a time.")
            if 'submission_data' not in request.data:
                return _bad("Must provide submission data.")

            # Validate

            # Check for replacement

            #  user = request.user TODO
            user = User.objects.get(id=1)  # request.user.profile  # TODO

            survey = Survey.objects.get(id=pk)
            form = survey.form
            time = request.data['time']
            raw_data = request.data['submission_data']

            submission = Submission.objects.create(user=user, form=form, time=time, raw_data=raw_data)

            serializer = SubmissionSerializer(submission, many=False)

            response = {'message': 'Submission received', 'result': serializer.data}

            # Bad input...

            return ResponseType(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return ResponseType(_m(f"Could not parse submission ({e})"), status=status.HTTP_400_BAD_REQUEST)


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


class FloatRangeQuestionViewSet(viewsets.ModelViewSet):
    _model = FloatRangeQuestion
    serializer_class = FloatRangeQuestionSerializer
    queryset = _model.objects.all()


class BooleanChoiceQuestionViewSet(viewsets.ModelViewSet):
    _model = BooleanChoiceQuestion
    serializer_class = ExclusiveChoiceQuestionSerializer
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

    @action(detail=True, methods=['POST'])
    def resubmit(self, request, pk=None):  # TODO
        try:
            # Validate

            submission = Submission.objects.get(pk=pk)

            #  user = request.user TODO
            user = User.objects.get(id=1)  # request.user.profile  # TODO

            changed = False

            if 'time' in request.data:
                time = request.data['time']
                submission.time = time

            if 'submission_data' in request.data:
                raw_data = request.data['submission_data']
                submission.raw_data = raw_data

            if not changed:
                return _r("No change requested", status.HTTP_204_NO_CONTENT)

            serializer = SubmissionSerializer(submission, many=False)

            response = {'message': 'Update received', 'result': serializer.data}

            # Bad input...

            return ResponseType(response, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return ResponseType(_m(f"Could not parse submission ({e})"), status=status.HTTP_400_BAD_REQUEST)


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


class IndicatorViewSet(viewsets.ModelViewSet):
    _model = Indicator
    serializer_class = IndicatorSerializer
    queryset = _model.objects.all()


class IntDataPointViewSet(viewsets.ModelViewSet):
    _model = IntDataPoint
    serializer_class = IntDataPointSerializer
    queryset = _model.objects.all()


class FloatDataPointViewSet(viewsets.ModelViewSet):
    _model = FloatDataPoint
    serializer_class = FloatDataPointSerializer
    queryset = _model.objects.all()


class AvailableSurveyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = AvailableSurveySerializer






















