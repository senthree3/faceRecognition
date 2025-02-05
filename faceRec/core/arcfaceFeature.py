# -*- coding: utf-8 -*-
"""
@author: zhou
@time: 2023/11/30 10:46
"""
import os
import os.path as osp
import argparse
import cv2
import numpy as np
import onnxruntime
from typing import List
from faceRec.libs.arcface_onnx import ArcFaceONNX
from faceRec.conf.settings import ARCFACE_R50_MODEL_PATH
from faceRec.conf.settings import SAME_PERSON_THRESHOLD, LIKELY_SAME_PERSON_THRESHOLD
from faceRecognition.enums import FaceRecStatusParameter

onnxruntime.set_default_logger_severity(3)

rec = ArcFaceONNX(ARCFACE_R50_MODEL_PATH)
rec.prepare(0)


# def fun(image1):
#     feat1 = rec.get(image1, kps1)
#     feat2 = feat1
#     sim = rec.compute_sim(feat1, feat2)
#     if sim < 0.2:
#         conclu = 'They are NOT the same person'
#     elif sim >= 0.2 and sim < 0.28:
#         conclu = 'They are LIKELY TO be the same person'
#     else:
#         conclu = 'They ARE the same person'
#     return sim, conclu


def get_face_feature(image):
    feat = rec.get_feat(imgs=image)
    return feat


class GetFaceFeatureSimilarity(object):
    def __init__(self, feat1, feat2: List):
        self.feat1 = feat1
        self.feat2 = feat2

    def get_similarity(self):
        return [rec.compute_sim(self.feat1, feat2) for feat2 in self.feat2]

    def get_same_person_determine(self):
        sim = self.get_similarity()
        conclu = []
        for s in sim:
            if s < LIKELY_SAME_PERSON_THRESHOLD:
                info = FaceRecStatusParameter.not_same_face.info()
                code = FaceRecStatusParameter.not_same_face.code()
                # conclu.append("notSamePerson")  # 'They are NOT the same person'
            elif (s >= LIKELY_SAME_PERSON_THRESHOLD) and s < SAME_PERSON_THRESHOLD:
                info = FaceRecStatusParameter.likely_face.info()
                code = FaceRecStatusParameter.likely_face.code()
                # conclu.append("likelySamePerson")  # = 'They are LIKELY TO be the same person'
            else:
                info = FaceRecStatusParameter.same_face.info()
                code = FaceRecStatusParameter.same_face.code()
                # conclu.append("samePerson")  # = 'They ARE the same person'
            conclu.append([code, info])
        return sim, conclu


class GetFaceImagesSimilarity(GetFaceFeatureSimilarity):
    def __init__(self, img1, img2: List):
        self.img1 = img1
        self.img2 = img2
        self.feat1 = get_face_feature(img1)
        self.feat2 = [get_face_feature(x) for x in img2]
        super(GetFaceImagesSimilarity, self).__init__(self.feat1, self.feat2)
