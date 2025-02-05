import json
from io import BytesIO

from django.contrib import admin, messages
from django.http import HttpResponseBadRequest
from django.db import transaction
from faceDet.core.scrfdDetection import ScrfdDetection
from faceRec.core.arcfaceFeature import get_face_feature
from faceRecognition.settings import FEATURE_DB_REAL_TIME_UPDATE
from faceRecognition.utils import image_binary_to_array, image_array_to_image_binary
from faceRec.conf.settings import GLOBAL_FACE_FEATURE_VECTOR_DB_POOL as gffv
from .models import FaceRegistrationInformation
from faceRecognition.utils.loggers import logger


# Register your models here.


@admin.register(FaceRegistrationInformation)
class FaceRegistrationInformationAdmin(admin.ModelAdmin):
    list_display = ["face_feature_id", "account", "face_id", "user_name", "image_img", "status"]
    list_filter = ["status"]
    search_fields = ["account", "face_feature_id", "user_name"]
    list_per_page = 10
    readonly_fields = ['face_feature_array']

    def save_model(self, request, obj: FaceRegistrationInformation, form, change):
        try:
            if 'face_reg_img' in request.FILES:
                img = request.FILES['face_reg_img']

                image = image_binary_to_array(img.read())
                sd = ScrfdDetection(image, max_num=1)
                aimg = sd.crop_face()[0]
                # 获取特征
                feature = get_face_feature(aimg)[0].tolist()
                feature_array_str = json.dumps(feature)

                obj.face_feature_array = feature_array_str
                obj.face_reg_img.save(obj.face_reg_img.name, BytesIO(image_array_to_image_binary(aimg)))
                super(FaceRegistrationInformationAdmin, self).save_model(request, obj, form, change)
                if FEATURE_DB_REAL_TIME_UPDATE:
                    ff_id = obj.face_feature_id
                    tenant_id = obj.account.account
                    if change:
                        gffv.update_face(tenant_id=tenant_id, face_id=ff_id, new_feature_vector=feature)
                        logger.info(f"admin views reg ff_id<{ff_id}> updated in feature db success.")
                    else:
                        gffv.add_face(tenant_id=tenant_id, face_id=ff_id, feature_vector=feature)
                        logger.info(f"admin views reg ff_id<{ff_id}> add to feature db success.")
            else:
                super(FaceRegistrationInformationAdmin, self).save_model(request, obj, form, change)

        except Exception as e:
            error_message = f"Error: {type(e).__name__} - {str(e)}"
            logger.error(f"admin views reg error:{error_message}")
            self.message_user(request, error_message, level=messages.ERROR)
            # return HttpResponseBadRequest(error_message)

    def delete_model(self, request, obj: FaceRegistrationInformation):
        try:
            with transaction.atomic():
                # 调用父类的 delete_model 方法删除对象
                if FEATURE_DB_REAL_TIME_UPDATE:
                    ff_id = [obj.face_feature_id]
                    tenant_id = obj.account.account
                    gffv.delete_face(tenant_id=tenant_id, face_id=ff_id)
                    logger.info(f"admin views delete reg ff_id<{ff_id}> delete to feature db success.")
                super(FaceRegistrationInformationAdmin, self).delete_model(request, obj)
        except Exception as e:
            error_message = f"Error: {type(e).__name__} - {str(e)}"
            logger.error(f"admin views reg delete error:{error_message}")
            self.message_user(request, error_message, level=messages.ERROR)

    def delete_queryset(self, request, queryset):
        try:
            with transaction.atomic():
                if FEATURE_DB_REAL_TIME_UPDATE:
                    ff_id = list(queryset.values_list('face_feature_id', flat=True))
                    tenant_id = list(set(queryset.values_list('account__account', flat=True)))[0]
                    gffv.delete_face(tenant_id=tenant_id, face_id=ff_id)
                    logger.info(f"admin views delete queryset reg ff_id<{ff_id}> delete to feature db success.")
                super(FaceRegistrationInformationAdmin, self).delete_queryset(request, queryset)
        except Exception as e:
            error_message = f"Error: {type(e).__name__} - {str(e)}"
            logger.error(f"admin views reg delete queryset error:{error_message}")
            self.message_user(request, error_message, level=messages.ERROR)
