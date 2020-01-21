from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from Revitalize.views import ClientViewSet, CohortViewSet, FormViewSet, SubmissionViewSet, IndicatorViewSet, \
    DataPointViewSet, GoalViewSet, AnonymizedIndicatorViewSet, CohortDataPointViewSet

router = routers.DefaultRouter()
router.register('clients', ClientViewSet)
router.register('cohorts', CohortViewSet)
router.register('forms', FormViewSet)
router.register('submissions', SubmissionViewSet)
router.register('indicators', IndicatorViewSet)
router.register('data_points', DataPointViewSet)
router.register('goals', GoalViewSet)
router.register('a_indicators', AnonymizedIndicatorViewSet)
router.register('c_data_points', CohortDataPointViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
