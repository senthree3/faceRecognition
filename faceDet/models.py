import uuid

from django.db import models
from django.utils.html import format_html
from django.contrib import admin
from serviceMgt.models import CompetencyRegistry


# Create your models here.

class FaceDetectionRecordInformation(models.Model):
    account = models.ForeignKey(to=CompetencyRegistry, on_delete=models.DO_NOTHING, verbose_name="账号")
    input_image = models.ImageField(verbose_name="输入图片")
    output_image = models.ImageField(null=True, blank=True, verbose_name="输出图片")
    detection_result = models.TextField(verbose_name="检测结果", null=True, blank=True)
    det_type_choose = {
        (0, "所有人脸"),
        (1, "最大人脸"),
        (2, "置信度最优人脸")
    }
    detection_type = models.SmallIntegerField(choices=det_type_choose, default=0, verbose_name="人脸检测类型")
    status_describe = models.TextField(null=True, blank=True, verbose_name="状态描述")
    request_time = models.DateTimeField(verbose_name='请求时间')
    respond_time = models.DateTimeField(verbose_name='应答时间', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    request_id = models.CharField(max_length=36, default=str(uuid.uuid4()), verbose_name="请求ID")

    class Meta:
        verbose_name = "人脸检测调用记录表"
        verbose_name_plural = "4.人脸检测调用记录表"

    def __str__(self):
        return self.account.account

    def input_image_img(self):
        if not self.input_image:
            return '无'
        return format_html(
            """<div><img src='{}' style='width:50px;height:65px;' ></div>""",
            self.input_image.url)

    input_image_img.short_description = '检测原图'

    def output_image_img(self):
        if not self.output_image:
            return '无'
        return format_html(
            """<div><img src='{}' style='width:50px;height:65px;' ></div>""",
            self.output_image.url)

    output_image_img.short_description = '检测结果'

