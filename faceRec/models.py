import uuid

from django.db import models

# Create your models here.
from serviceMgt.models import CompetencyRegistry


class FeatureExtractionRecordInformation(models.Model):
    account = models.ForeignKey(to=CompetencyRegistry, on_delete=models.DO_NOTHING, verbose_name="账号")
    input_image = models.ImageField(verbose_name="输入图片")
    feature_image = models.ImageField(null=True, blank=True, verbose_name="特征图片")
    feature_vector = models.TextField(verbose_name="特征向量", null=True, blank=True)
    feature_extract_status_choose = {
        (0, "失败"),
        (1, "成功"),
        (2, "没有存在人脸信息"),
    }
    detection_type = models.BooleanField(choices=feature_extract_status_choose, default=0, verbose_name="状态")
    status_describe = models.TextField(null=True, blank=True, verbose_name="状态描述")
    request_time = models.DateTimeField(verbose_name='请求时间')
    respond_time = models.DateTimeField(verbose_name='应答时间', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    request_id = models.CharField(max_length=36, default=str(uuid.uuid4()), verbose_name="请求ID")

    class Meta:
        verbose_name = "人脸特征提取调用记录表"
        verbose_name_plural = "5.人脸特征提取调用记录表"

    def __str__(self):
        return self.account.account


class O2OImageRecognitionRecordInformation(models.Model):
    account = models.ForeignKey(to=CompetencyRegistry, on_delete=models.DO_NOTHING, verbose_name="账号")
    input_image_1 = models.ImageField(verbose_name="图片1")
    input_image_2 = models.ImageField(verbose_name="图片2")
    similarity = models.FloatField(verbose_name="相似度", null=True, blank=True)
    o2o_rec_type_choose = {
        (0, "失败"),
        (1, "是同一个人"),
        (2, "可能是同一个人"),
        (3, "不是同一个人"),
    }
    o2o_image_rec_type = models.SmallIntegerField(choices=o2o_rec_type_choose, default=0, verbose_name="状态")
    status_describe = models.TextField(null=True, blank=True, verbose_name="状态描述")
    request_time = models.DateTimeField(verbose_name='请求时间')
    respond_time = models.DateTimeField(verbose_name='应答时间', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    request_id = models.CharField(max_length=36, default=str(uuid.uuid4()), verbose_name="请求ID")

    class Meta:
        verbose_name = "1:1(图像)人脸识别调用记录表"
        verbose_name_plural = "6.1:1(图像)人脸识别调用记录表"

    def __str__(self):
        return self.account.account


class O2OCheckRecognitionRecordInformation(models.Model):
    account = models.ForeignKey(to=CompetencyRegistry, on_delete=models.DO_NOTHING, verbose_name="账号")
    face_id = models.CharField(max_length=18, verbose_name="人脸ID")
    user_name = models.CharField(max_length=32, verbose_name="姓名")
    image = models.ImageField(verbose_name="图片")
    similarity = models.FloatField(verbose_name="相似度", null=True, blank=True)
    o2o_rec_type_choose = {
        (0, "失败"),
        (1, "是同一个人"),
        (2, "可能是同一个人"),
        (3, "不是同一个人"),
    }
    o2o_check_rec_type = models.SmallIntegerField(choices=o2o_rec_type_choose, default=0, verbose_name="状态")
    status_describe = models.TextField(null=True, blank=True, verbose_name="状态描述")
    request_time = models.DateTimeField(verbose_name='请求时间')
    respond_time = models.DateTimeField(verbose_name='应答时间', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    request_id = models.CharField(max_length=36, default=str(uuid.uuid4()), verbose_name="请求ID")

    class Meta:
        verbose_name = "人脸检测调用记录表"
        verbose_name_plural = "7.人脸检测调用记录表"

    def __str__(self):
        return self.account.account


class O2NRecognitionRecordInformation(models.Model):
    account = models.ForeignKey(to=CompetencyRegistry, on_delete=models.DO_NOTHING, verbose_name="账号")
    image = models.ImageField(verbose_name="输入图片")
    similarity = models.FloatField(verbose_name="相似度", null=True, blank=True)
    infer_face_id = models.CharField(max_length=18, verbose_name="推理人脸ID")
    infer_user_name = models.CharField(max_length=32, verbose_name="推理用户姓名")
    o2n_rec_type_choose = {
        (0, "失败"),
        (1, "成功"),
        (2, "可能是"),
        (3, "无匹配信息")
    }
    o2n_rec_type = models.SmallIntegerField(choices=o2n_rec_type_choose, default=0, verbose_name="状态")
    status_describe = models.TextField(null=True, blank=True, verbose_name="状态描述")
    request_time = models.DateTimeField(verbose_name='请求时间')
    respond_time = models.DateTimeField(verbose_name='应答时间', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    request_id = models.CharField(max_length=36, default=str(uuid.uuid4()), verbose_name="请求ID")

    class Meta:
        verbose_name = "人脸检测调用记录表"
        verbose_name_plural = "8.人脸检测调用记录表"

    def __str__(self):
        return self.account.account
