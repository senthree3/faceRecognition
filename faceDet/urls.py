# -*- coding: utf-8 -*-
"""
@author: zhou
@time: 2023/11/29 14:26
"""
from . import views
from django.urls import path

urlpatterns = [
    path("faceDet", views.FaceDetectionInterface.as_view(), name="人脸检测服务"),
]