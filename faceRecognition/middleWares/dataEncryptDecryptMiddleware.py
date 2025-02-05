# -*- coding: utf-8 -*-
"""
@author: zhou
@time: 2023/11/30 09:19
"""
import json
from faceRecognition.utils.loggers import logger
from django.utils.deprecation import MiddlewareMixin
from faceRecognition.utils.encryptDecryptAlgorithm.AesCrypt import aesCrypt
from faceRecognition.utils.customException import InterfaceException
from faceRecognition.enums import InterfaceRequestStatusParameter


class DataEncryptDecryptMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super(DataEncryptDecryptMiddleware, self).__init__(get_response)
        self.get_response = get_response

    def __call__(self, request):
        # 在请求到达视图之前进行解密
        secret_key = request.secret_key
        edc = aesCrypt(key=secret_key, key_size=32)
        if request.method == 'POST':
            request_data = json.loads(request.body.decode('utf-8'))
            data = request_data.get('data', None)
            if data:
                decrypted_data = edc.decrypt(data)
                request_data["data"] = json.loads(decrypted_data)
                modified_data = json.dumps(request_data).encode("utf-8")
                request._body = modified_data

        response = self.get_response(request)

        # 在响应返回之前进行加密
        if isinstance(response, dict):
            response = json.dumps(response)
        if isinstance(response, list):
            response = json.dumps(response)
        elif isinstance(response, str):
            pass
        elif isinstance(response, bool):
            response = str(response)
        else:
            err_code = InterfaceRequestStatusParameter.encrypted_data_format_error.code()
            err_msg = InterfaceRequestStatusParameter.encrypted_data_format_error.info()
            logger.error(f"error msg:{err_msg} error code:{err_code}")
            raise InterfaceException(err_msg, err_code)
        response = edc.encrypt(response)

        return response
