# -*- coding: utf-8 -*-
"""
@author: zhou
@time: 2023/11/9 14:23
"""
import os
import uuid
from hashlib import md5
from faceMgt.conf.settings import FACE_IMAGES_SAVE_DIRECTORY_PATH
from faceRecognition.utils.randomGeneration import generate_random_mixed_case_string


def user_info_md5(user_info):
    return md5(user_info.encode()).hexdigest()


class FaceImageSavePath(object):
    def __init__(self, file_name: str = None):
        self.ext = "jpg" if file_name is None else file_name.split(".")[-1]
        self.uuid = uuid.uuid4().hex[:10]
        self.base_dir = FACE_IMAGES_SAVE_DIRECTORY_PATH

    def base_path(self, instance=None, account: str = None, face_id: str = None):
        if instance is not None:
            account = instance.account.account
            face_id = instance.face_id
        elif face_id is not None and account is not None:
            account = account
            face_id = face_id
        else:
            account = generate_random_mixed_case_string(10)
            face_id = self.uuid
        face_id_md5 = user_info_md5(face_id)
        return account, face_id_md5

    def face_reg_path(self, instance=None, account: str = None, face_id: str = None):
        account, face_id_md5 = self.base_path(instance, account, face_id)
        return os.path.join(self.base_dir, account, "reg", face_id_md5, f"{self.uuid}.{self.ext}")

    def face_rec_path(self, instance=None, account: str = None, face_id: str = None):
        account, face_id_md5 = self.base_path(instance, account, face_id)
        return os.path.join(self.base_dir, account, "rec", face_id_md5, f"{self.uuid}.{self.ext}")

    def random_face_path(self):
        dir_l = [generate_random_mixed_case_string(10) for _ in range(2)]
        return os.path.join(self.base_dir, dir_l[0], dir_l[1], f"{self.uuid}.{self.ext}")
