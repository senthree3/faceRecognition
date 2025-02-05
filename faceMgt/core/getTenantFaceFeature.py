# -*- coding: utf-8 -*-
"""
@author: zhou
@time: 2024/1/9 14:48
"""
import json
from typing import List

from faceMgt.models import FaceRegistrationInformation
from faceRecognition.utils.loggers import logger


class GetTenantFaceFeature(object):
    def __init__(self):
        self.tff = {}

    def grouped_result(self, result):
        grouped_result = {}
        for item in result:
            account_id = item['account']
            face_feature_id = item['face_feature_id']
            face_feature_array = json.loads(item['face_feature_array'])

            if account_id not in grouped_result:
                grouped_result[account_id] = [(face_feature_id, face_feature_array)]
            else:
                grouped_result[account_id].append((face_feature_id, face_feature_array))
        self.tff = grouped_result
        return grouped_result

    def get_all_tenant_face_feature(self):
        result = FaceRegistrationInformation.objects.values('account', 'face_feature_id',
                                                            'face_feature_array').filter(status=0)
        grouped_result = self.grouped_result(result)
        logger.info(f"success get {len(grouped_result.keys())} tenant all face feature")
        return grouped_result

    def get_tenant_list_face_feature(self, tenant_id: List):
        result = FaceRegistrationInformation.objects.values('account', 'face_feature_id',
                                                            'face_feature_array').filter(status=0,
                                                                                         account__account_id__in=tenant_id)
        grouped_result = self.grouped_result(result)
        logger.info(f"success get {tenant_id} tenant list face feature")
        return grouped_result

    def get_one_tenant_face_feature(self, tenant_id):
        result = FaceRegistrationInformation.objects.values('account', 'face_feature_id',
                                                            'face_feature_array').filter(status=0,
                                                                                         account__account_id=tenant_id)
        grouped_result = self.grouped_result(result)
        logger.info(f"success get {tenant_id} tenant face feature")
        return grouped_result
