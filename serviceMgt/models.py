import uuid
from datetime import datetime
from django.db import models
from faceRecognition.utils.randomGeneration import generate_random_mixed_case_string


# Create your models here.

class CompetencyRegistry(models.Model):
    account = models.CharField(max_length=32, verbose_name="账号", primary_key=True)
    phone = models.CharField(max_length=11, verbose_name="电话", null=True, blank=True)
    access_key = models.CharField(max_length=32, verbose_name="AK", unique=True,
                                  default=generate_random_mixed_case_string(32))
    secret_key = models.CharField(max_length=32, verbose_name="SK", unique=True,
                                  default=generate_random_mixed_case_string(32))
    account_description = models.CharField(max_length=128, verbose_name="描述", null=True, blank=True)
    status_choose = {
        (0, "启用"),
        (1, "停用")
    }
    status = models.BooleanField(choices=status_choose, verbose_name="状态", default=0)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = "能力注册"
        verbose_name_plural = "1.能力注册"

    def __str__(self):
        return self.account


class CapabilitySubscriptionModel(models.Model):
    account = models.ForeignKey(to=CompetencyRegistry, on_delete=models.CASCADE, verbose_name="账号")
    ability_choices = (
        (0, '人脸检测'),
        (1, '人脸特征提取'),
        (2, '人脸1:1(图像)'),
        (3, '人脸1:1(校验)'),
        (4, '人脸1:N'),
        (5, '静默活体检测'),
        (6, '人脸关键点检测'),
        (7, '人脸注册（库管理）'),
        (8, '人脸相似检索')
    )
    ability = models.SmallIntegerField(choices=ability_choices, verbose_name="能力选择")
    validity_period = models.DateTimeField(verbose_name='有效期',default=datetime(2099, 12, 31, 23, 59, 59))
    subscription_req_amount = models.IntegerField(default=-1, verbose_name="订阅调用量（-1为无限制）")
    max_req_amount = models.IntegerField(default=-1, verbose_name="剩余调用量（-1为无限制）")
    total_req_count = models.IntegerField(default=0, verbose_name="累计调用量")
    status_choices = (
        (0, '生效'),
        (1, '失效'),
    )
    status = models.BooleanField(choices=status_choices, verbose_name='能力状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        unique_together = ('account', 'ability')
        verbose_name = "能力订阅详情"
        verbose_name_plural = "2.能力订阅详情"

    def __str__(self):
        return self.account.account
