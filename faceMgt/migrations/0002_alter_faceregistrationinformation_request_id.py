# Generated by Django 4.2.7 on 2024-01-03 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faceMgt', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faceregistrationinformation',
            name='request_id',
            field=models.CharField(default='c5586b5e-4931-4d89-82b6-f88ba40043f9', max_length=36, verbose_name='请求ID'),
        ),
    ]
