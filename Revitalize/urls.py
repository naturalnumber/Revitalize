from django.urls import include, path
from rest_framework import routers

from Revitalize.views import *

router = routers.DefaultRouter()

# TODO: are these showing the proper urls when doing '/api/'

# router.register('text', TextViewSet)
# router.register('strings', StringViewSet)
# router.register('string_groups', StringGroupViewSet)
router.register('forms', FormViewSet)
router.register('surveys', SurveyViewSetFrontEnd, basename='survey')
router.register('medical_labs', MedicalLabViewSetFrontEnd, basename='medical_lab')
router.register('available_surveys', AvailableSurveyViewSet, basename='available_survey')
router.register('user_survey_history', UserSurveyHistoryViewSet)
router.register('profile_retrieval', ProfileRetrievalViewSet, basename='profile_retrieval')
#router.register('profile', ProfileRetrievalViewSet.as_view({'get' : 'retrieve'}), basename='profile')
router.register('user_indicator', UserIndicatorViewSet)
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

# For debugging
# router.register('surveys_d', SurveyViewSetAll)
# router.register('surveys_0', SurveyViewSet)
# router.register('medical_labs_0', MedicalLabViewSet)
# router.register('profilse_0', ProfileViewSet)


urlpatterns = [
        path('', include(router.urls)),
]
