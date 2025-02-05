# -*- coding: utf-8 -*-
"""
@author: zhou
@time: 2021/12/8 11:20
"""
import base64
import json
from Crypto.Cipher import AES


class aesCrypt(object):
    def __init__(self, key: str, key_size=16, model=AES.MODE_CBC, iv=None, aes_encode="utf-8"):
        self.model = model
        self.aes_model = aes_encode
        self.key_size = key_size
        self.key = self.add_size_multiple(key[:self.key_size])
        self.iv = bytes(iv.encode()) if iv is not None else self.key[:min(len(key), 16)]

        BS = self.key_size
        self.pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        self.unpad = lambda s: s[0:-ord(s[-1:])]

    def add_size_multiple(self, par):
        if type(par) == str:
            par = par.encode(self.aes_model)
        while len(par) % self.key_size != 0:
            par += b'\x00'
        return par

    def encrypt(self, text, out_bs64=True):
        """加密"""
        # text = self.add_size_multiple(text)
        if self.model == AES.MODE_CBC:
            aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        else:
            aes = AES.new(self.key, AES.MODE_ECB)
        encrypt_text = aes.encrypt(bytes(self.pad(text), encoding="utf-8"))
        if out_bs64:
            encrypt_text = base64.encodebytes(encrypt_text).decode()
        return encrypt_text

    def decrypt(self, text, in_bs64=True):
        """解密"""
        if in_bs64:
            text = base64.decodebytes(text.encode("utf-8"))
        if self.model == AES.MODE_CBC:
            aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        else:
            aes = AES.new(self.key, AES.MODE_ECB)
        decrypt_text = aes.decrypt(text)
        return self.unpad(decrypt_text).decode()


if __name__ == "__main__":
    # _tf = ["KEY.RJ", "KEY1.RJ", "KEY2.RJ", "KEY3.RJ"]  # "LICENSE.RJ" KEY.RJ
    # for t in _tf:
    #     with open(t, "rb") as f:
    #         _krj_text = f.read()
    #         # print(_krj_text)
    #         _krj_text = base64.decodebytes(_krj_text)  # E7BC96E7A081E69C89E8AFAF 916171790FDA0155469E9CB613E8ED39
    # _lf = "KEY.RJ" #"LICENSE.RJ"
    # # _lf = "/home/cv/zhouhs/temp/test.txt"
    # with open(_lf, "rb") as f1:
    #     _lf_data = f1.read()
    # _t = base64.decodebytes(_lf_data) #json.loads(_lf_data)  # ["a"]
    # # print(_t)
    # _key = "916171790FDA0155469E9CB613E8ED39" #"fMXKto3xLQOpEL58tYraXpwbEViH7iHH"
    # print(aesCrypt(key=_key).decrypt(_t, False))
    # pass
    pass
