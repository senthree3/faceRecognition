from django.contrib import admin
from .models import FaceDetectionRecordInformation


# Register your models here.

@admin.register(FaceDetectionRecordInformation)
class FaceDetectionRecordInformationAdmin(admin.ModelAdmin):
    list_display = ["account", "input_image_img", "output_image_img", "detection_type", "request_id"]
    list_filter = ["detection_type"]
    search_fields = ["account", "request_id"]
    list_per_page = 10
