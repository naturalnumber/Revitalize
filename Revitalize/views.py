from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Revitalize.serializers import *
from django.utils import timezone
import pytz

# Helper methods

print_debug = False
print_debug2 = False


def _m(m: str):
    return {'message': m}


def _r(m: str, s: status):
    return Response(_m(m), s)


def _ok(m: str):
    return Response(_m(m), status.HTTP_200_OK)


def _bad(m: str):
    return Response(_m(m), status.HTTP_400_BAD_REQUEST)


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

            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(_m(f"Could not parse submission ({e})"), status=status.HTTP_400_BAD_REQUEST)


class SurveyViewSetAll(viewsets.ModelViewSet):
    _model = Survey
    serializer_class = SurveySerializer
    queryset = _model.objects.all()


class SurveyViewSet(viewsets.ModelViewSet):
    _model = Survey
    serializer_class = SurveySerializerDisplay
    queryset = _model.objects.all()


class SurveyViewSetFrontEnd(viewsets.ModelViewSet):
    _model = Form
    serializer_class = FormSerializerDisplay
    queryset = _model.objects.filter(type=Form.FormType.SURVEY.value).all()
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['POST'])
    def submit(self, request, pk=None):
        if print_debug or print_debug2: print(f"Submission received for form #{pk}")
        if print_debug: print(request)
        if print_debug: print(dir(request))
        if print_debug: print(request.data)
        #SurveyViewSetFrontEnd.last_request = request
        try:
            if 'data' not in dir(request):
                return _bad("Must provide submission data.")
            if pk is None:
                return _bad("No key provided.")

            # Validate

            # Check for replacement

            if print_debug: print("check 1")

            user = request.user  # TODO

            if print_debug: print(user)

            form = Form.objects.get(id=pk)
            if print_debug: print(form)

            submission_data = request.data
            if print_debug or print_debug2: print(f"submission_data = {submission_data} \n... {dict(submission_data)}")
            if print_debug: print(type(submission_data))

            if 'time' in dir(request):
                time = request.data['time']
            elif 'time' in submission_data:
                time = submission_data['time']
            else:
                time = timezone.now()
            if print_debug: print(time)

            if isinstance(submission_data, dict):
                raw_data = json.dumps(submission_data)
                if print_debug or print_debug2: print(f"dict -> raw_data = {raw_data}")
            elif isinstance(submission_data, str):
                raw_data = submission_data
                if print_debug or print_debug2: print(f"str -> raw_data = {raw_data}")
            else:
                raw_data = submission_data
                if print_debug or print_debug2: print(f"? -> raw_data = {raw_data}")



            submission = Submission.objects.create(user=user, form=form, time=time, raw_data=raw_data)
            if print_debug: print(submission)

            try:
                if print_debug or print_debug2: print('check 2')
                submission.process(submission.validate())
                if print_debug or print_debug2: print('check 3')
            except ValidationError as e:
                if print_debug or print_debug2: print(f"Validation: {e}")
                return Response(_m(f"Could not validate submission ({e})"), status=status.HTTP_400_BAD_REQUEST)

            serializer = SubmissionSerializer(submission, many=False)

            response = {'message': 'Submission received', 'result': serializer.data}

            if print_debug: print(f"status.HTTP_201_CREATED = {status.HTTP_201_CREATED}")
            to_send = Response(response, status=status.HTTP_201_CREATED)
            if print_debug or print_debug2: print(to_send)
            return to_send
        except Exception as e:
            if print_debug or print_debug2: print(e)
            return Response(_m(f"Could not parse submission ({e})"), status=status.HTTP_400_BAD_REQUEST)


class MedicalLabViewSet(viewsets.ModelViewSet):
    _model = MedicalLab
    serializer_class = MedicalLabSerializer
    queryset = _model.objects.all()


class MedicalLabViewSetFrontEnd(viewsets.ModelViewSet):
    _model = Form
    serializer_class = FormSerializerDisplay
    queryset = _model.objects.filter(type=Form.FormType.MEDICAL_LAB.value).all()


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

            return Response(response, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(_m(f"Could not parse submission ({e})"), status=status.HTTP_400_BAD_REQUEST)


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


class UserSurveyHistoryViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = UserSurveyHistorySerializer


class ProfileRetrievalViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileRetrievalSerializer


class UserIndicatorViewSet(viewsets.ModelViewSet):
    queryset = Indicator.objects.all()
    serializer_class = UserIndicatorSerializer
