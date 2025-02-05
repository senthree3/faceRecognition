import json
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from faceDet.core.scrfdDetection import ScrfdDetection
from faceDet.utils.drawImage import DrawBBox
from faceRecognition.middleWares import apply_capability_middleware_decorator
from faceRecognition.utils.imageDataFormat import image_array_to_base64, image_base64_to_array
from faceRecognition.utils.customException import InterfaceException
from faceRecognition.enums import InterfaceRequestStatusParameter
from faceRecognition.utils.loggers import logger


# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
# from drf_yasg.views import APIView

@apply_capability_middleware_decorator
class FaceDetectionInterface(View):
    # @swagger_auto_schema(
    #     request_body=openapi.Schema(
    #         type=openapi.TYPE_OBJECT,
    #         properties={
    #             'request_id': openapi.Schema(type=openapi.TYPE_STRING),
    #             'data': openapi.Schema(type=openapi.TYPE_OBJECT),
    #         },
    #         required=['data'],
    #     ),
    #     responses={200: "OK - Success response"},
    #     operation_summary="Face Detection API",
    #     operation_description="Endpoint for face detection",
    # )
    def post(self, request: WSGIRequest):
        json_data = json.loads(request.body.decode('utf-8'))
        request_id = json_data.get('request_id', None)
        if 'data' not in json_data or not isinstance(json_data['data'], dict):
            err_msg = InterfaceRequestStatusParameter.invalid_req_data_format.info()
            err_code = InterfaceRequestStatusParameter.invalid_req_data_format.code()
            logger.info(f"error:{err_msg} err_code:{err_code}")
            raise InterfaceException(err_msg, err_code)
        data = json_data["data"]
        image = data.get('image', None)
        det_type = data.get('det_type', 1)
        detected_image = data.get('det_image', False)
        drawn_image = data.get('draw_image', False)

        image = image_base64_to_array(image)
        sd = ScrfdDetection(image, det_type)
        bboxes, possibility, kpss1 = sd.det()
        result = {
            "bbox": bboxes,
            "possibility": possibility,
        }
        if detected_image:
            det_image = sd.crop_face()
            det_image = [image_array_to_base64(d) for d in det_image]
            result["det_image"] = det_image
        if drawn_image:
            draw_img = DrawBBox(image, is_original_draw=False).draw_bbox_list(bboxes)
            draw_img = image_array_to_base64(draw_img)
            result["draw_image"] = draw_img

        return result  # JsonResponse(result)

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(FaceDetectionInterface, self).dispatch(*args, **kwargs)
