# -*- coding: utf-8 -*-
"""
@author: zhou
@time: 2023/11/29 14:37
"""
import json

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from faceRecognition.settings import OPEN_ABILITY_API_IDENTIFICATION
from faceRecognition.utils.customException import InterfaceException
from faceRecognition.enums import InterfaceRequestStatusParameter
from faceRecognition.utils.loggers import logger
from serviceMgt.models import CompetencyRegistry, CapabilitySubscriptionModel
from serviceMgt.conf.openAbilitySettings import OPEN_ABILITY_ADDRESS_KV_DB_ID


class AccessKeyCheckMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response

    def __call__(self, request):
        # 判定需要进行 access_key 验证的路由子串
        protected_route_substring = OPEN_ABILITY_API_IDENTIFICATION

        # 获取请求路径和请求方法
        request_path = request.path
        request_method = request.method
        request.is_open_ability = False
        if protected_route_substring in request_path and request_method == 'POST':
            # 为request 添加自定义类型标识
            request.is_open_ability = True

            # 如果请求路径包含受保护的路由子串且是 POST 请求
            request_data = json.loads(request.body.decode('utf-8'))
            access_key = request_data.get("access_key", None)

            # 这里假设你有一个函数 validate_access_key 来验证 access_key 是否正确
            if not self.validate_access_key(access_key):
                logger.info(f"Invalid access key:{access_key}")
                raise InterfaceException(InterfaceRequestStatusParameter.invalid_access_key.info(),
                                         InterfaceRequestStatusParameter.invalid_access_key.code())

            # 提取请求路径中的标识符
            path_segments = request_path.split("/")
            v1_index = path_segments.index("v1")

            # 获取 /v1/ 后面的标识符
            if v1_index + 1 < len(path_segments):
                v1_identifier = path_segments[v1_index + 1]
            else:
                logger.info(f"{access_key} request {request_path} is error path")
                raise Exception(f"{request_path} is a request path")

            if not self.check_ability_subscription(access_key, v1_identifier):
                logger.info(f"{access_key} ability not subscription {v1_identifier}")
                raise InterfaceException(InterfaceRequestStatusParameter.ability_not_subscription.info(),
                                         InterfaceRequestStatusParameter.ability_not_subscription.code())

        # 继续处理请求
        response = self.get_response(request)
        return response

    def validate_access_key(self, access_key):
        try:
            registry_entry = CompetencyRegistry.objects.get(access_key=access_key, status=0)
            return True
        except CompetencyRegistry.DoesNotExist:
            return False

    def check_ability_subscription(self, access_key, ability_identifier):
        ability_id = self.convert_ability_address_to_ability_id(ability_identifier)
        try:
            ability_info = CapabilitySubscriptionModel.objects.get(account__access_key=access_key,
                                                                   ability=ability_id,
                                                                   status=0)
            current_time = timezone.now()
            if current_time > ability_info.validity_period:
                logger.info(f"{access_key}:{InterfaceRequestStatusParameter.ability_expired.info()}")
                raise InterfaceException(InterfaceRequestStatusParameter.ability_expired.info(),
                                         InterfaceRequestStatusParameter.ability_expired.code())

            if ability_info.max_req_amount != -1 and ability_info.max_req_amount <= 0:
                logger.info(f"{access_key}:{InterfaceRequestStatusParameter.ability_exhausted.info()}")
                raise InterfaceException(InterfaceRequestStatusParameter.ability_exhausted.info(),
                                         InterfaceRequestStatusParameter.ability_exhausted.code())
            return True
        except Exception as e:
            logger.info(f"check ability error is {e.__str__()}")
            return False

    def convert_ability_address_to_ability_id(self, ability_address_identifier):
        try:
            ability_id = OPEN_ABILITY_ADDRESS_KV_DB_ID[ability_address_identifier]
            return ability_id
        except Exception as e:
            logger.info(f"ability url address not exits:{ability_address_identifier} | {e.__str__()}")
            raise InterfaceException(InterfaceRequestStatusParameter.ability_not_exist.info(),
                                     InterfaceRequestStatusParameter.ability_not_exist.code())
