# -*- coding: utf-8 -*-
"""
@author: zhou
@time: 2023/11/29 14:26
"""
from . import views
from django.urls import path

urlpatterns = [
    path("faceFeatureExtraction", views.FaceFeatureExtractionInterface.as_view(), name="人脸特征提取"),
    path("face11Images", views.O2OImageRecognitionInterface.as_view(), name="人脸1t1(图像)"),
    path("face11Check", views.O2OCheckRecognitionInterface.as_view(), name="人脸1t1(校验)"),
    path("face1N", views.O2NRecognitionInterface.as_view(), name="人脸1tN"),
    path("faceSimilarRetrieval", views.O2NRecognitionInterface.as_view(), name="人脸相似检索")
]
