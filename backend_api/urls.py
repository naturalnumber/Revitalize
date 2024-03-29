"""backend_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from Revitalize import views
from Revitalize.admin import admin_site, lab_tech_site, detailed_admin_site
from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

# profile picture
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
        path('admin/', admin_site.urls),
        path('labtech/', lab_tech_site.urls),
        path('detailed/', detailed_admin_site.urls),
        path('api/', include('Revitalize.urls')),
        # TODO could these be put in the Revitalize urls.py?
        # Authentication : https://github.com/davesque/django-rest-framework-simplejwt
        path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        url(r'account/register/$', views.register_account, name='register_account'),
        url(r'account/create/$', views.create_account, name='create_account')
]

# profile picture
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
