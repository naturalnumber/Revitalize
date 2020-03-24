from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from Revitalize.views import *

router = routers.DefaultRouter()


# /lab_values/history/user
# GET -> all lab value for user (history)
# POST -> {min_date, max_date} filtered history
# [{name: 'Weight", value: 120, submission_date: 32412341234}, {name: 'Weight', value: 125', submission_date:  3424324}]
# lab_values/user -> list of indicators

# /lab_values/id/history/user
# GET -> all lab values for that id
# POST -> min_date max_date to filter

_new_patterns = []

router.register('profile', ProfileRetrievalViewSet, basename='profile')

router.register('lab-value', LabValueRetrievalViewSet, basename='lab-value')

router.register('survey-value', SurveyValueRetrievalViewSet, basename='survey-value')

router.register('indicator', IndicatorRetrievalViewSet, basename='indicator')

router.register('indicator/survey', SurveyIndicatorRetrievalViewSet, basename='indicator-survey')

router.register('indicator/lab-value', LabIndicatorRetrievalViewSet, basename='indicator-lab-value')

router.register('surveys/user', UserSurveyHistoryViewSet, basename='survey')

# TODO: are these showing the proper urls when doing '/api/'

# router.register('text', TextViewSet)
# router.register('strings', StringViewSet)
# router.register('string_groups', StringGroupViewSet)
router.register('forms', FormViewSet)
router.register('surveys', SurveyViewSetFrontEnd, basename='survey')
router.register('medical_labs', MedicalLabViewSetFrontEnd, basename='medical_lab')
router.register('available_surveys', AvailableSurveyViewSet, basename='available_survey')
router.register('survey_history', UserSurveyHistoryViewSet, basename='survey_submission')
router.register('profile_retrieval', ProfileRetrievalViewSet, basename='profile_retrieval')
#router.register('profile', ProfileRetrievalViewSet.as_view({'get' : 'retrieve'}), basename='profile')
router.register('text_elements', TextElementViewSet)
router.register('question_groups', QuestionGroupViewSet)
router.register('questions', QuestionViewSet)
router.register('question_text', TextQuestionViewSet)
router.register('question_int', IntQuestionViewSet)
router.register('question_float', FloatQuestionViewSet)
router.register('question_int_range', IntRangeQuestionViewSet)
router.register('question_float_range', FloatRangeQuestionViewSet)
router.register('question_boolean_choice', BooleanChoiceQuestionViewSet)
router.register('question_exclusive_choice', ExclusiveChoiceQuestionViewSet)
router.register('question_multi_choice', MultiChoiceQuestionViewSet)
router.register('submissions', SubmissionViewSet)
router.register('responses_text', TextResponseViewSet)
router.register('responses_int', IntResponseViewSet)
router.register('responses_float', FloatResponseViewSet)
router.register('indicators', IndicatorViewSet)
router.register('data_points_int', IntDataPointViewSet)
router.register('data_points_float', FloatDataPointViewSet)
router.register('addresses', AddressViewSet)

router.register('lab_values', LabValueViewSet, basename='lab_values')

router.register('user_indicators', UserIndicatorViewSet, basename='user_indicator')

router.register('user_indicator_data', UserIndicatorDataViewSet, basename='user_indicator_data')

router.register('user_survey_indicators', UserSurveyIndicatorViewSet, basename='user_survey_indicator')
router.register('user_lab_indicators', UserLabIndicatorViewSet, basename='user_lab_indicator')

# For debugging
# router.register('surveys_d', SurveyViewSetAll)
# router.register('surveys_0', SurveyViewSet)
# router.register('medical_labs_0', MedicalLabViewSet)
# router.register('profilse_0', ProfileViewSet)


urlpatterns = [
        path('', include(router.urls)),
]

urlpatterns.extend(format_suffix_patterns(_new_patterns))
