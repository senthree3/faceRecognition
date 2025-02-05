# -*- coding: utf-8 -*-
"""
@author: zhou
@time: 2023/11/29 17:22
"""
import json

from django.utils.deprecation import MiddlewareMixin

from faceRecognition.enums import InterfaceRequestStatusParameter
from faceRecognition.utils.customException import InterfaceException
from faceRecognition.utils.customGenerateSign import CustomGenerateSign
from faceRecognition.utils.loggers import logger
from serviceMgt.models import CompetencyRegistry


class SignValidationMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response

    def __call__(self, request):
        # 获取请求中的基本参数
        is_open_ability = request.is_open_ability
        request_data = json.loads(request.body.decode('utf-8'))

        request_id = request_data.get('request_id', None)
        time_stamp = request_data.get('time_stamp', None)
        access_key = request_data.get("access_key", None)
        sign = request_data.get('sign', None)

        # 获取请求中的 data 参数
        data = request_data.get('data', None)  # or request.GET.get('data')
        # 校验参数
        if not all([request_id, time_stamp, access_key, sign, data]):
            logger.info(f"{access_key}:{InterfaceRequestStatusParameter.miss_req_param.info()}")
            raise InterfaceException(InterfaceRequestStatusParameter.miss_req_param.info(),
                                     InterfaceRequestStatusParameter.miss_req_param.code())

        secret_key = CompetencyRegistry.objects.get(access_key=access_key).secret_key
        request.secret_key = secret_key
        validator = CustomGenerateSign(access_key, secret_key)
        # 生成预期的校验标识
        expected_sign = validator.generate_sign(request_id, time_stamp, data)

        # 校验生成的校验标识与请求中的是否一致
        if sign != expected_sign:
            logger.info(f"{access_key}:{InterfaceRequestStatusParameter.invalid_sign.info()}")
            raise InterfaceException(InterfaceRequestStatusParameter.invalid_sign.info(),
                                     InterfaceRequestStatusParameter.invalid_sign.code())

        # 继续处理请求
        response = self.get_response(request)
        return response
