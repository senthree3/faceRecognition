import uuid

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.html import format_html

from serviceMgt.models import CompetencyRegistry
from faceMgt.utils.faceImageSavePath import FaceImageSavePath


# Create your models here.

def get_face_reg_file_path(instance, filename):
    dp = FaceImageSavePath(filename)
    return dp.face_reg_path(instance)


class FaceRegistrationInformation(models.Model):
    """
    人脸注册信息
    """
    account = models.ForeignKey(to=CompetencyRegistry, on_delete=models.DO_NOTHING, verbose_name="账号")
    face_id = models.CharField(max_length=18, verbose_name="人脸ID")
    user_name = models.CharField(max_length=32, verbose_name="姓名")
    phone = models.CharField(max_length=11, verbose_name="电话", null=True, blank=True)
    face_reg_img = models.ImageField(upload_to=get_face_reg_file_path, verbose_name="人脸图片")
    face_feature_array = models.TextField(verbose_name="人脸特征")
    face_feature_id = models.BigAutoField(verbose_name="人脸特征向量ID", primary_key=True)
    status_choose = {
        (0, "启用"),
        (1, "停用")
    }
    status = models.BooleanField(choices=status_choose, verbose_name="状态", default=0)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    request_id = models.CharField(max_length=36, default=str(uuid.uuid4()), verbose_name="请求ID")

    class Meta:
        unique_together = ('account', 'face_id')
        verbose_name = "人脸注册信息表"
        verbose_name_plural = "人脸注册信息"

    def __str__(self):
        return self.face_id

    def save(self, *args, **kwargs):
        self.face_id = self.face_id.upper()
        super(FaceRegistrationInformation, self).save(*args, **kwargs)

    def image_img(self):
        if not self.face_reg_img:
            return '无'
        return format_html(
            """<div><img src='{}' style='width:50px;height:65px;' ></div>""",
            self.face_reg_img.url)

    image_img.short_description = '图片'
