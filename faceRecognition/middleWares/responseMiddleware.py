# -*- coding: utf-8 -*-
"""
@author: zhou
@time: 2023/11/29 10:17
"""
import json

from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from faceRecognition.utils.customException import InterfaceException, NormalErrorException
from faceRecognition.enums import InterfaceRequestStatusParameter
from faceRecognition.utils.loggers import logger


class ResponseMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response

    def __call__(self, request):
        # 获取请求体中的 request_id
        request_data = json.loads(request.body.decode('utf-8'))
        request_id = request_data.get("request_id", None)
        self.request_id = request_id
        try:
            response = self.get_response(request)
            return self.process_response(response, request_id)
        except Exception as e:
            # 处理异常并返回异常信息
            logger.info(f"response call error info:{e.__str__()}")
            return self.handle_exception(e, request_id)

    def process_response(self, response, request_id):
        # 封装响应为标准格式，并包含 request_id（如果存在）
        result = {"data": response,
                  "code": InterfaceRequestStatusParameter.success.code(),
                  "message": InterfaceRequestStatusParameter.success.info()}
        if request_id:
            result["request_id"] = request_id
        logger.info(f"success response data:{result}")
        return JsonResponse(result)

    def process_template_response(self, request, response):
        # 对 TemplateResponse 进行额外处理（如果有需要的话）
        return response

    def handle_exception(self, exception, request_id=None):
        # 根据异常类型返回不同的编码和消息，并包含 request_id（如果存在）
        result = {"code": InterfaceRequestStatusParameter.fail.code(),
                  "message": InterfaceRequestStatusParameter.fail.info()}
        if request_id:
            result["request_id"] = request_id

        if isinstance(exception, InterfaceException):
            result["code"] = exception.code
            result["message"] = exception.__str__()
            logger.info(f"interface exception response data:{result}")
        elif isinstance(exception, NormalErrorException):
            result["code"] = exception.code
            result["message"] = exception.__str__()
            logger.info(f"response data:{result}")
        else:
            logger.info(f"except response data:{result}")
        return JsonResponse(result)

    def process_exception(self, exception):
        # 处理其他未被捕获的异常
        return self.handle_exception(exception, self.request_id)
