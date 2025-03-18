# -*- coding: utf-8 -*-
"""
@author: zhou
@time: 2023/12/18 10:26
"""
from faceMgt.conf.settings import GLOBAL_FACE_FEATURE_INDEX_DICT
from faceRec.core.faceVectorIndex import FaceVectorIndex


def add_account_face_index_to_pool(account, value: FaceVectorIndex):
    # global GLOBAL_FACE_FEATURE_INDEX_DICT
    GLOBAL_FACE_FEATURE_INDEX_DICT[account] = value


def get_account_face_index_from_pool(account):
    return GLOBAL_FACE_FEATURE_INDEX_DICT.get(account)


