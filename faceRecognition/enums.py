# -*- coding: utf-8 -*-
"""
@author: zhou
@time: 2023/11/28 14:30
"""

from enum import Enum


class InterfaceRequestStatusParameter(Enum):
    fail = ("fail", 500)
    success = ("success", 200)
    miss_req_param = ("Missing required parameters", 400)
    invalid_access_key = ("Invalid access key", 401)
    invalid_sign = ("Invalid sign", 402)
    encrypted_data_format_error = ("Encrypted data format error", 6001)
    ability_not_subscription = ("Ability not subscription", 7521)
    ability_not_exist = ("Ability not exist", 7522)
    ability_expired = ("Ability subscription has expired", 7523)
    ability_exhausted = ("Exhausted maximum request limit", 7524)
    invalid_req_data_format = ("Invalid request data format", 7525)

    def code(self):
        return self.value[1]

    def info(self):
        return self.value[0]


class FaceRecStatusParameter(Enum):
    zero_face = ("Face not found in image", 8301)
    face_id_exist = ("Face id registered", 8401)
    face_id_not_exist = ("Faces with IDs do not exist", 8402)
    face_feature_vector_db_not_exist = ("Face feature vector database do not exist", 8403)
    unknown_face = ("unknown_face", 0)
    likely_face = ("likely_face", 1)
    same_face = ("same_face", 2)
    not_same_face = ("not_same_face", 3)

    def code(self):
        return self.value[1]

    def info(self):
        return self.value[0]
