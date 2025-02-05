# Create your views here.
import copy
import json
import os.path

import cv2
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from faceDet.core.scrfdDetection import ScrfdDetection
from faceMgt.utils.faceImageSavePath import FaceImageSavePath
from faceRec.core.arcfaceFeature import get_face_feature
from faceRec.conf.settings import GLOBAL_FACE_FEATURE_VECTOR_DB_POOL as gffv
from faceRecognition.utils.imageDataFormat import image_array_to_base64, save_array_to_file, image_base64_to_array
from faceRecognition.utils.imageDataFormat import image_file_to_image_base64
from faceRecognition.utils.customException import InterfaceException, NormalErrorException
from faceRecognition.enums import InterfaceRequestStatusParameter, FaceRecStatusParameter
from faceRecognition.utils.loggers import logger
from faceRecognition.settings import MEDIA_DIR, FEATURE_DB_REAL_TIME_UPDATE
from faceMgt.models import FaceRegistrationInformation
from serviceMgt.models import CompetencyRegistry
from faceRecognition.middleWares import apply_capability_middleware_decorator


# 人脸注册、删除、修改、查询

@apply_capability_middleware_decorator
class FaceRegisterInterface(View):
    def post(self, request: WSGIRequest):
        json_data = json.loads(request.body.decode("utf-8"))
        request_id = json_data.get("request_id", None)
        access_key = json_data.get('access_key')
        data = json_data["data"]
        # 注册核心参数
        face_id = data.get("face_id")
        image = data.get("image")
        user_name = data.get("user_name")
        phone = data.get("phone", None)

        account = CompetencyRegistry.objects.get(access_key=access_key)
        fri = FaceRegistrationInformation.objects.filter(account__access_key=access_key, face_id=face_id)
        if fri.exists():
            ex_msg = FaceRecStatusParameter.face_id_exist.info()
            ex_code = FaceRecStatusParameter.face_id_exist.code()
            logger.info(f"{access_key} request id:{request_id} face register face id ({face_id}) exist.")
            raise NormalErrorException(ex_msg, ex_code)
        #
        image = image_base64_to_array(image)
        # 检测人脸
        sd = ScrfdDetection(image, max_num=1)
        aimg = sd.crop_face()[0]
        # 获取特征
        feature = get_face_feature(aimg)[0].tolist()
        feature_array_str = json.dumps(feature)
        # 存储人脸
        dp = FaceImageSavePath()
        face_reg_img = dp.face_reg_path(account=account.account, face_id=face_id)
        save_array_to_file(aimg[:, :, ::-1], os.path.join(MEDIA_DIR, face_reg_img))
        # 数据入库
        created_instance = FaceRegistrationInformation.objects.create(
            account=account,
            face_id=face_id,
            user_name=user_name,
            phone=phone,
            face_reg_img=face_reg_img,
            face_feature_array=feature_array_str,
            request_id=request_id
        )
        logger.info(f"{request_id} registration {face_id} success.")

        if FEATURE_DB_REAL_TIME_UPDATE:
            ff_id = created_instance.face_feature_id
            gffv.add_face(tenant_id=account.account, face_id=ff_id, feature_vector=feature)
            logger.info(f"{request_id} reg ff_id<{ff_id}> add to feature db success.")
        return True

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(FaceRegisterInterface, self).dispatch(*args, **kwargs)


@apply_capability_middleware_decorator
class FaceRegDeleteInterface(View):
    def post(self, request: WSGIRequest):
        json_data = json.loads(request.body.decode("utf-8"))
        request_id = json_data.get("request_id", None)
        access_key = json_data.get('access_key')
        data = json_data["data"]
        # 参数
        face_ids = data.get('face_id', [])  # list 列表
        # 使用 filter 获取所有需要删除的对象
        fri = FaceRegistrationInformation.objects.filter(account__access_key=access_key, face_id__in=face_ids)

        # 检查是否存在不存在的 face_id
        existing_face_ids = fri.values_list('face_id', flat=True)
        non_existing_face_ids = set(face_ids) - set(existing_face_ids)
        if non_existing_face_ids:
            ex_msg = f"{request_id}: Faces with IDs {non_existing_face_ids} do not exist."
            ex_code = FaceRecStatusParameter.face_id_not_exist.code()
            logger.info(ex_msg)
            raise NormalErrorException(ex_msg, ex_code)

        # 执行批量删除

        if FEATURE_DB_REAL_TIME_UPDATE:
            ff_id = list(fri.values_list('face_feature_id', flat=True))
            tenant_id = list(set(fri.values_list('account__account', flat=True)))[0]
            gffv.delete_face(tenant_id=tenant_id, face_id=ff_id)
            logger.info(f"{request_id} delete reg ff_id<{ff_id}> update to feature db success.")

        fri.delete()

        return True

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(FaceRegDeleteInterface, self).dispatch(*args, **kwargs)


@apply_capability_middleware_decorator
class FaceRegUpdateInterface(View):
    def post(self, request: WSGIRequest):
        json_data = json.loads(request.body.decode("utf-8"))
        request_id = json_data.get("request_id", None)
        access_key = json_data.get('access_key')
        data = json_data["data"]
        # 参数
        face_id = data.get('face_id')
        image = data.get("image", None)
        user_name = data.get("user_name", None)
        phone = data.get("phone", None)

        fri = FaceRegistrationInformation.objects.get(account__access_key=access_key, face_id=face_id)
        feature = json.loads(fri.face_feature_array)
        if user_name is not None:
            fri.user_name = user_name
            logger.info(f"{fri.account.account}:the face id <{face_id}> update name, new name is {user_name}.")
        if phone is not None:
            fri.phone = phone
            logger.info(f"{fri.account.account}:the face id <{face_id}> update phone, new phone is {phone}.")
        if image is not None:
            image = image_base64_to_array(image)
            # 检测人脸
            sd = ScrfdDetection(image, max_num=1)
            aimg = sd.crop_face()[0]
            # 获取特征
            feature = get_face_feature(aimg)[0].tolist()
            feature_array_str = json.dumps(feature)
            # 存储人脸
            dp = FaceImageSavePath()
            face_reg_img = dp.face_reg_path(account=fri.account.account, face_id=face_id)
            logger.info(f"{fri.account.account}:the face id <{face_id}> update image ,"
                        f"{fri.face_reg_img} -> {face_reg_img}.")
            save_array_to_file(aimg[:, :, ::-1], os.path.join(MEDIA_DIR, face_reg_img))
            fri.face_reg_img = face_reg_img
            fri.face_feature_array = feature_array_str
        # 保存更新
        fri.save()

        if FEATURE_DB_REAL_TIME_UPDATE and image is not None:
            ff_id = fri.face_feature_id
            tenant_id = fri.account.account
            gffv.update_face(tenant_id=tenant_id, face_id=ff_id, new_feature_vector=feature)
            logger.info(f"{request_id} update reg ff_id<{ff_id}> update to feature db success.")

        return True

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(FaceRegUpdateInterface, self).dispatch(*args, **kwargs)


@apply_capability_middleware_decorator
class FaceRegQueryInterface(View):
    def post(self, request: WSGIRequest):
        json_data = json.loads(request.body.decode("utf-8"))
        request_id = json_data.get("request_id", None)
        access_key = json_data.get('access_key')
        data = json_data["data"]
        # 核心参数
        page = data.get("page", 1)
        size = data.get("size", 20)

        # 计算偏移量
        offset = (page - 1) * size
        fri = FaceRegistrationInformation.objects.filter(account__access_key=access_key).order_by('face_feature_id')[
              offset:offset + size]

        result_list = []
        for face_info in fri:
            result_list.append({
                "face_id": face_info.face_id,
                "user_name": face_info.user_name,
                "phone": face_info.phone,
                "image": image_file_to_image_base64(
                    face_info.face_reg_img.path) if face_info.face_reg_img.path else None,
                "feature": json.loads(face_info.face_feature_array)
            })
        return result_list

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(FaceRegQueryInterface, self).dispatch(*args, **kwargs)


@apply_capability_middleware_decorator
class FaceRegIDQueryInterface(View):
    def post(self, request: WSGIRequest):
        json_data = json.loads(request.body.decode("utf-8"))
        request_id = json_data.get("request_id", None)
        access_key = json_data.get('access_key')
        data = json_data["data"]
        # 核心参数
        face_ids = data.get('face_id', [])  # list 列表

        #
        fri = FaceRegistrationInformation.objects.filter(account__access_key=access_key, face_id__in=face_ids)

        # 构建包含结果的列表
        result_list = []
        for face_info in fri:
            result_list.append({
                "face_id": face_info.face_id,
                "user_name": face_info.user_name,
                "phone": face_info.phone,
                "image": image_file_to_image_base64(
                    face_info.face_reg_img.path) if face_info.face_reg_img.path else None,
                "feature": json.loads(face_info.face_feature_array)
            })

        return result_list

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(FaceRegIDQueryInterface, self).dispatch(*args, **kwargs)
