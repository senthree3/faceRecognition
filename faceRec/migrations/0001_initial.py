# Generated by Django 4.2.7 on 2024-01-03 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('serviceMgt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='O2OImageRecognitionRecordInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_image_1', models.ImageField(upload_to='', verbose_name='图片1')),
                ('input_image_2', models.ImageField(upload_to='', verbose_name='图片2')),
                ('similarity', models.FloatField(blank=True, null=True, verbose_name='相似度')),
                ('o2o_image_rec_type', models.SmallIntegerField(choices=[(0, '失败'), (3, '不是同一个人'), (1, '是同一个人'), (2, '可能是同一个人')], default=0, verbose_name='状态')),
                ('status_describe', models.TextField(blank=True, null=True, verbose_name='状态描述')),
                ('request_time', models.DateTimeField(verbose_name='请求时间')),
                ('respond_time', models.DateTimeField(blank=True, null=True, verbose_name='应答时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('request_id', models.CharField(default='2a12a3c0-86dc-498c-9aa9-01d620be2a14', max_length=36, verbose_name='请求ID')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='serviceMgt.competencyregistry', verbose_name='账号')),
            ],
            options={
                'verbose_name': '1:1(图像)人脸识别调用记录表',
                'verbose_name_plural': '6.1:1(图像)人脸识别调用记录表',
            },
        ),
        migrations.CreateModel(
            name='O2OCheckRecognitionRecordInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('face_id', models.CharField(max_length=18, verbose_name='人脸ID')),
                ('user_name', models.CharField(max_length=32, verbose_name='姓名')),
                ('image', models.ImageField(upload_to='', verbose_name='图片')),
                ('similarity', models.FloatField(blank=True, null=True, verbose_name='相似度')),
                ('o2o_check_rec_type', models.SmallIntegerField(choices=[(0, '失败'), (3, '不是同一个人'), (1, '是同一个人'), (2, '可能是同一个人')], default=0, verbose_name='状态')),
                ('status_describe', models.TextField(blank=True, null=True, verbose_name='状态描述')),
                ('request_time', models.DateTimeField(verbose_name='请求时间')),
                ('respond_time', models.DateTimeField(blank=True, null=True, verbose_name='应答时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('request_id', models.CharField(default='9f594689-6307-4d4e-9cca-e077f87c91b0', max_length=36, verbose_name='请求ID')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='serviceMgt.competencyregistry', verbose_name='账号')),
            ],
            options={
                'verbose_name': '人脸检测调用记录表',
                'verbose_name_plural': '7.人脸检测调用记录表',
            },
        ),
        migrations.CreateModel(
            name='O2NRecognitionRecordInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='输入图片')),
                ('similarity', models.FloatField(blank=True, null=True, verbose_name='相似度')),
                ('infer_face_id', models.CharField(max_length=18, verbose_name='推理人脸ID')),
                ('infer_user_name', models.CharField(max_length=32, verbose_name='推理用户姓名')),
                ('o2n_rec_type', models.SmallIntegerField(choices=[(0, '失败'), (3, '无匹配信息'), (2, '可能是'), (1, '成功')], default=0, verbose_name='状态')),
                ('status_describe', models.TextField(blank=True, null=True, verbose_name='状态描述')),
                ('request_time', models.DateTimeField(verbose_name='请求时间')),
                ('respond_time', models.DateTimeField(blank=True, null=True, verbose_name='应答时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('request_id', models.CharField(default='6dcf6f2e-063b-4219-b948-7adbf3953b28', max_length=36, verbose_name='请求ID')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='serviceMgt.competencyregistry', verbose_name='账号')),
            ],
            options={
                'verbose_name': '人脸检测调用记录表',
                'verbose_name_plural': '8.人脸检测调用记录表',
            },
        ),
        migrations.CreateModel(
            name='FeatureExtractionRecordInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_image', models.ImageField(upload_to='', verbose_name='输入图片')),
                ('feature_image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='特征图片')),
                ('feature_vector', models.TextField(blank=True, null=True, verbose_name='特征向量')),
                ('detection_type', models.BooleanField(choices=[(0, '失败'), (2, '没有存在人脸信息'), (1, '成功')], default=0, verbose_name='状态')),
                ('status_describe', models.TextField(blank=True, null=True, verbose_name='状态描述')),
                ('request_time', models.DateTimeField(verbose_name='请求时间')),
                ('respond_time', models.DateTimeField(blank=True, null=True, verbose_name='应答时间')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('request_id', models.CharField(default='d49ab5e4-fecb-400c-b5f6-d1f73b08c4ab', max_length=36, verbose_name='请求ID')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='serviceMgt.competencyregistry', verbose_name='账号')),
            ],
            options={
                'verbose_name': '人脸特征提取调用记录表',
                'verbose_name_plural': '5.人脸特征提取调用记录表',
            },
        ),
    ]
