import json

import numpy as np
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from faceDet.core.scrfdDetection import ScrfdDetection
from faceDet.utils.drawImage import DrawBBox
from faceMgt.models import FaceRegistrationInformation
from faceRec.conf.settings import GLOBAL_FACE_FEATURE_VECTOR_DB_POOL as gffv, LIKELY_SAME_PERSON_THRESHOLD, \
    SAME_PERSON_THRESHOLD
from faceRec.core.arcfaceFeature import get_face_feature, GetFaceImagesSimilarity, GetFaceFeatureSimilarity
from faceRecognition.enums import FaceRecStatusParameter
from faceRecognition.middleWares import apply_capability_middleware_decorator
from faceRecognition.utils import image_base64_to_array, image_array_to_base64, image_file_to_image_base64
from faceRecognition.utils.loggers import logger
from serviceMgt.models import CompetencyRegistry


@apply_capability_middleware_decorator
class FaceFeatureExtractionInterface(View):
    def post(self, request: WSGIRequest):
        json_data = json.loads(request.body.decode("utf-8"))
        request_id = json_data.get("request_id", None)
        access_key = json_data.get("access_key")
        data = json_data["data"]
        # 注册核心参数
        image = data.get("image")
        #
        image = image_base64_to_array(image)
        # 检测人脸
        sd = ScrfdDetection(image, max_num=1)
        aimg = sd.crop_face()[0]
        # 获取特征
        feature = get_face_feature(aimg)[0].tolist()
        face_image = image_array_to_base64(aimg)

        return {"feature": feature,
                "face_image": face_image}

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(FaceFeatureExtractionInterface, self).dispatch(*args, **kwargs)


@apply_capability_middleware_decorator
class O2OImageRecognitionInterface(View):
    def post(self, request: WSGIRequest):
        json_data = json.loads(request.body.decode("utf-8"))
        request_id = json_data.get("request_id", None)
        access_key = json_data.get("access_key")
        data = json_data["data"]

        image1 = data.get("image1")
        image2 = data.get("image2")
        image1 = image_base64_to_array(image1)
        image2 = image_base64_to_array(image2)
        # 检测人脸
        sd = ScrfdDetection(image1, max_num=1)
        aimg1 = sd.crop_face()[0]
        aimg2 = ScrfdDetection(image2, max_num=1).crop_face()
        # 获取特征
        sim, conclu = GetFaceImagesSimilarity(aimg1, aimg2).get_same_person_determine()
        logger.info(f"request id:{request_id} one to on image similarity is {conclu}:{sim}")
        tp, des = conclu[0]
        result = {
            "possibility": round(np.array(sim[0]).item(), 3),
            "type": tp,
            "describe": des
        }
        return result

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(O2OImageRecognitionInterface, self).dispatch(*args, **kwargs)


@apply_capability_middleware_decorator
class O2OCheckRecognitionInterface(View):
    def post(self, request: WSGIRequest):
        json_data = json.loads(request.body.decode("utf-8"))
        request_id = json_data.get("request_id", None)
        access_key = json_data.get("access_key")
        data = json_data["data"]

        image = data.get("image")
        image = image_base64_to_array(image)
        face_id = data.get("face_id")
        # 检测人脸
        sd = ScrfdDetection(image, max_num=1)
        aimg1 = sd.crop_face()[0]
        feature1 = get_face_feature(aimg1)
        feature2 = FaceRegistrationInformation.objects.get(account__access_key=access_key,
                                                           face_id=face_id).face_feature_array
        feature2 = json.loads(feature2)
        # 获取特征
        sim, conclu = GetFaceFeatureSimilarity(feature1, [np.array(feature2)]).get_same_person_determine()
        logger.info(f"request id:{request_id} one to on image similarity is {conclu}:{sim}")
        tp, des = conclu[0]
        result = {
            "possibility": round(np.array(sim[0]).item(), 3),
            "type": tp,
            "describe": des
        }
        return result

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(O2OCheckRecognitionInterface, self).dispatch(*args, **kwargs)


@apply_capability_middleware_decorator
class O2NRecognitionInterface(View):
    def post(self, request: WSGIRequest):
        json_data = json.loads(request.body.decode("utf-8"))
        request_id = json_data.get("request_id", None)
        access_key = json_data.get("access_key")
        data = json_data["data"]

        image = data.get("image")
        image = image_base64_to_array(image)
        similar_face = data.get("similar_face", False)
        top_k = 1
        if similar_face:
            top_k = data.get("top_k", 1)
            top_k = min(max(top_k, 1), 5)
        detected_image = data.get("det_image", False)
        drawn_image = data.get("draw_image", False)

        # 检测人脸
        sd = ScrfdDetection(image, max_num=1)
        bboxes, possibility, kpss1 = sd.det()
        aimg1 = sd.crop_face()[0]
        feature1 = get_face_feature(aimg1)[0]
        account = CompetencyRegistry.objects.get(access_key=access_key).account

        dd, ii = gffv.search_face(tenant_id=account, feature_vector=feature1, top_k=top_k)
        # dd 距离并非相似度，需要dd / (np.linalg.norm(feature1) * np.linalg.norm(np.array([np.array(feature2)])))进行转换
        logger.info(f"feature vector search {account} index is:{ii}")
        top_k_fri = FaceRegistrationInformation.objects.filter(account__access_key=access_key, face_feature_id__in=ii,
                                                               status=0)
        if similar_face:
            result_list = []
            for face_info in top_k_fri:
                sim, conclu = GetFaceFeatureSimilarity(feature1, [
                    np.array(json.loads(face_info.face_feature_array))]).get_same_person_determine()
                tp, des = conclu[0]
                f_o = {
                    "possibility": round(np.array(sim[0]).item(), 3),
                    "type": tp,
                    "describe": des,
                    "face_id": face_info.face_id,
                    "user_name": face_info.user_name,
                    "phone": face_info.phone,
                    # "image": image_file_to_image_base64(
                    #     face_info.face_reg_img.path) if face_info.face_reg_img.path else None,
                }
                rank = ii.index(face_info.face_feature_id) + 1
                if top_k != 1:
                    f_o["rank"] = rank
                result_list.append(f_o)
            result = {
                "similar_list": result_list
            }
        else:
            result = {
                "type": FaceRecStatusParameter.unknown_face.code(),
                "describe": FaceRecStatusParameter.unknown_face.info()
            }
            inference_face_obj = top_k_fri[0]
            sim, conclu = GetFaceFeatureSimilarity(feature1, [
                np.array(json.loads(inference_face_obj.face_feature_array))]).get_same_person_determine()
            sim = sim[0]
            face_id = inference_face_obj.face_id
            user_name = inference_face_obj.user_name
            phone = inference_face_obj.phone
            if sim > LIKELY_SAME_PERSON_THRESHOLD:
                result.update({
                    "face_id": face_id,
                    "user_name": user_name,
                    "phone": phone,
                    "possibility": round(np.array(sim).item(), 3)
                })
                tp, des = conclu[0]
                result["type"] = tp
                result["describe"] = des
        if detected_image:
            result["det_image"] = image_array_to_base64(aimg1)
        if drawn_image:
            draw_img = DrawBBox(image, is_original_draw=False).draw_bbox_list(bboxes)
            draw_img = image_array_to_base64(draw_img)
            result["draw_image"] = draw_img
        return result

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(O2NRecognitionInterface, self).dispatch(*args, **kwargs)
