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

# profile/user/ -> retrieve the profile for a single user
router.register('profiles', ProfileRetrievalViewSet, basename='profile')

#  values/user/ -> retrieve all data values associated with a user in format:
#  survey-values/user/ -> retrieve all survey values associated with a user in format:
#  lab-values/user/ -> retrieve all lab values associated with a user in format:
#       [{name: 'Weight", value: 120, unit: 'lb', submission_date: 32412341234},
#        {name: 'Weight', value: 125', unit: 'lb', submission_date:  3424324}]
#  values/id/user/ -> retrieve all data values of a certain id for a user in format:
#  survey-values/id/user/ -> retrieve all survey values of a certain id for a user in format:
#  lab-values/id/user/ -> retrieve all lab values of a certain id for a user in format:
#       [{name: 'Weight", value: 120, submission_date: 32412341234},
#        {name: 'Weight', value: 125', submission_date:  3424324}]
# 	GET -> all lab values associated with an id and user (history)
# 	POST -> {min_date, max_date} filtered version
router.register('data-values', LabValueRetrievalViewSet, basename='data-value')
router.register('lab-values', LabValueRetrievalViewSet, basename='lab-value')
router.register('survey-values', SurveyValueRetrievalViewSet, basename='survey-value')

#router.register('indicators', IndicatorRetrievalViewSet, basename='indicator')

#  apiCall('/indicators/survey/user/', { method: 'GET' }) // get all survey indicators for user (to select which one to graph)
#  apiCall(`/indicators/survey/${change.selector}/user/`, { method: 'POST', body: range }) // get graph data for survey indicators
# indicator/survey/user/ -> retrieves survey indicators associated with a user
# 	GET -> any submission_date/no submission_date
# 	POST -> {min_date, max_date} filtered version
router.register('indicators/survey', SurveyIndicatorRetrievalViewSet, basename='indicator-survey')

#  apiCall(`/indicators/lab-value/${change.selector}/user/`, { method: 'POST', body: range }) // get graph data for lab value
# indicator/lab-value/user/ -> retrieves lab value indicators associated with a user
# 	GET -> a submission_date/no submission_date
# 	POST -> {min_date, max_date} filtered version
# indicator/lab-value/id/user/recent -> most recent submission
router.register('indicators/lab-value', LabIndicatorRetrievalViewSet, basename='indicator-lab-value') # LabIndicatorRetrievalViewSet

#  apiCall('/surveys/user/', { method: 'GET'}) // get submitted survey history
#  apiCall('/surveys/user/available/', { method: 'GET'}) // get surveys avaialble to complete
#  apiCall(`/surveys/${surveyId}/submit/`, { method: 'POST', body: model }, false) // submit survey
# surveys/user/ -> retrieve all submitted surveys associated with a user (same as survey history endpoint)
router.register('surveys/user', UserSurveyHistoryViewSet, basename='survey') # UserSurveyHistoryViewSet

#  apiCall(`/surveys/${surveyId}/`, { method: 'GET'}) // get survey JSON
router.register('surveys', SurveyViewSetFrontEnd, basename='survey')
# router.register('available_surveys', AvailableSurveyViewSet, basename='available_survey')
# router.register('survey_history', UserSurveyHistoryViewSet, basename='survey_submission')
# router.register('profile_retrieval', ProfileRetrievalViewSet, basename='profile_retrieval')

# router.register('lab_values', LabValueViewSet, basename='lab_values')
#
# router.register('user_indicators', UserIndicatorViewSet, basename='user_indicator')
#
# router.register('user_indicator_data', UserIndicatorDataViewSet, basename='user_indicator_data')
#
# router.register('user_survey_indicators', UserSurveyIndicatorViewSet, basename='user_survey_indicator')
# router.register('user_lab_indicators', UserLabIndicatorViewSet, basename='user_lab_indicator')



urlpatterns = [
        path('', include(router.urls)),
]

urlpatterns.extend(format_suffix_patterns(_new_patterns))
