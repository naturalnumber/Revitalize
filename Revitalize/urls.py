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

router.register('profiles', ProfileRetrievalViewSet, basename='profile')

router.register('lab-values', LabValueRetrievalViewSet, basename='lab-value')

router.register('survey-values', SurveyValueRetrievalViewSet, basename='survey-value')

router.register('indicators', IndicatorRetrievalViewSet, basename='indicator')

router.register('indicators/survey', SurveyIndicatorRetrievalViewSet, basename='indicator-survey')

router.register('indicators/lab-value', LabIndicatorRetrievalViewSet, basename='indicator-lab-value')

router.register('surveys/user', UserSurveyHistoryViewSet, basename='survey')

router.register('surveys', SurveyViewSetFrontEnd, basename='survey')
router.register('available_surveys', AvailableSurveyViewSet, basename='available_survey')
router.register('survey_history', UserSurveyHistoryViewSet, basename='survey_submission')
router.register('profile_retrieval', ProfileRetrievalViewSet, basename='profile_retrieval')

router.register('lab_values', LabValueViewSet, basename='lab_values')

router.register('user_indicators', UserIndicatorViewSet, basename='user_indicator')

router.register('user_indicator_data', UserIndicatorDataViewSet, basename='user_indicator_data')

router.register('user_survey_indicators', UserSurveyIndicatorViewSet, basename='user_survey_indicator')
router.register('user_lab_indicators', UserLabIndicatorViewSet, basename='user_lab_indicator')



urlpatterns = [
        path('', include(router.urls)),
]

urlpatterns.extend(format_suffix_patterns(_new_patterns))
