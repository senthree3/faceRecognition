# -*- coding: utf-8 -*-
"""
@author: zhou
@time: 2024/1/4 11:09
"""

import hashlib


class CustomGenerateSign(object):
    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key

    def generate_sign(self, request_id, time_stamp, data):
        # 生成校验标识 sign
        sign_data = f"{self.access_key}&{self.secret_key}&{request_id}&{time_stamp}&{data}"
        return hashlib.md5(sign_data.encode('utf-8')).hexdigest()
