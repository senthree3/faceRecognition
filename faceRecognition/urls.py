"""
URL configuration for faceRecognition project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import serve
from django.conf import settings
from faceRecognition.settings import OPEN_ABILITY_API_IDENTIFICATION
#
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
# from rest_framework import permissions
#
# schema_view = get_schema_view(
#     openapi.Info(
#         title="Face API",
#         default_version='v1',
#         description="Face API description",
#         terms_of_service="",
#         # contact=openapi.Contact(email=""),
#         # license=openapi.License(name="Your License"),
#     ),
#     public=True,
#     permission_classes=[permissions.AllowAny, ],
# )

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{OPEN_ABILITY_API_IDENTIFICATION}/v1/', include('faceMgt.urls')),
    path(f'{OPEN_ABILITY_API_IDENTIFICATION}/v1/', include('faceRec.urls')),
    path(f'{OPEN_ABILITY_API_IDENTIFICATION}/v1/', include('faceDet.urls')),
    re_path(r'^mediaData/(?P<path>.+)$', serve, {'document_root': settings.MEDIA_ROOT}),
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
