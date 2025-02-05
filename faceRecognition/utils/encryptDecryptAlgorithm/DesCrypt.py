# -*- coding: utf-8 -*-
"""
@author: zhou
@time: 2022/7/27 16:30
"""
import base64

import pyDes
from pyDes import ECB, PAD_PKCS5
# import binascii  # 二进制和 ASCII 码互转


class desCrypt(object):
    def __init__(self, key):
        self.key = key  # 八位密钥

    # 加密
    def des_en(self, text):
        iv = secret_key = self.key
        k = pyDes.des(secret_key, ECB, iv, pad=None, padmode=PAD_PKCS5)
        data = k.encrypt(text, padmode=PAD_PKCS5)
        # data.进制返回文本字符串.解码字符串
        # binascii.b2a_hex(data).decode()
        return base64.encodebytes(data).decode()

    # 解密
    def des_de(self, text):
        iv = secret_key = self.key
        k = pyDes.des(secret_key, ECB, iv, pad=None, padmode=PAD_PKCS5)
        # binascii.a2b_hex(text)
        data = k.decrypt(base64.decodebytes(text.encode("utf-8")), padmode=PAD_PKCS5)
        return data.decode()


if __name__ == "__main__":
    _key = "E.Al0p1O"
    dc = desCrypt(_key)
    text = "afd3412"
    _en_text = dc.des_en(text)
    print(_en_text)
    print(dc.des_de(_en_text))
