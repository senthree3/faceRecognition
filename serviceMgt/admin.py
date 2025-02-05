from django.contrib import admin
from .models import CompetencyRegistry, CapabilitySubscriptionModel


# Register your models here.

@admin.register(CompetencyRegistry)
class CompetencyRegistryAdmin(admin.ModelAdmin):
    list_display = ["account", "access_key", "secret_key", "status"]
    list_filter = ["status"]
    search_fields = ["account", "access_key"]
    list_per_page = 10


@admin.register(CapabilitySubscriptionModel)
class CapabilitySubscriptionModelAdmin(admin.ModelAdmin):
    list_display = ["account", "ability", "max_req_amount", "total_req_count", "status"]
    list_filter = ["ability", "status"]
    search_fields = ["account"]
    list_per_page = 10


# 修改后台样式
admin.site.site_header = '人脸服务管理'
admin.site.site_title = '人脸服务'
admin.site.index_title = '后台主页'


