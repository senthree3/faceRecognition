# -*- coding: utf-8 -*-
"""
@author: zhou
@time: 2023/11/28 14:12
"""
import os
from faceRecognition.settings import BASE_DIR
from faceRec.core.globalFeatureVectorPool import GlobalFeatureVectorPool

ARCFACE_R50_MODEL_PATH = os.path.join(BASE_DIR, "aiModels/ms1mv2_r50_expand/model.onnx")

SAME_PERSON_THRESHOLD = 0.28
LIKELY_SAME_PERSON_THRESHOLD = 0.2

GLOBAL_FACE_FEATURE_VECTOR_DB_POOL = GlobalFeatureVectorPool()
GLOBAL_FACE_FEATURE_VECTOR_DB_POOL.load_all_tenants_feature_vectors()
