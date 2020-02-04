from django.urls import include, path
from rest_framework import routers

from Revitalize.views import ProfileViewSet, StringGroupViewSet, StringViewSet, TextViewSet

router = routers.DefaultRouter()

router.register('text', TextViewSet)
router.register('strings', StringViewSet)
router.register('string_groups', StringGroupViewSet)
router.register('profiles', ProfileViewSet)

urlpatterns = [
        path('', include(router.urls)),
]
