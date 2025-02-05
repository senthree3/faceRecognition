# -*- coding: utf-8 -*-
"""
@author: zhou
@time: 2023/11/29 14:26
"""
from . import views
from django.urls import path

urlpatterns = [
    path("faceReg", views.FaceRegisterInterface.as_view(), name="人脸注册服务"),
    path("faceRegDelete", views.FaceRegDeleteInterface.as_view(), name="人脸删除"),
    path("faceRegUpdate", views.FaceRegUpdateInterface.as_view(), name="人脸更新"),
    path("faceRegQuery", views.FaceRegQueryInterface.as_view(), name="人脸注册查询"),
    path("faceRegIDQuery", views.FaceRegIDQueryInterface.as_view(), name="人脸注册详细信息")
]
