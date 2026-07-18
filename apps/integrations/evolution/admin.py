from django.contrib import admin

from .models import InstanceStatus


@admin.register(InstanceStatus)
class InstanceStatusAdmin(admin.ModelAdmin):
    list_display = ("instance_name", "state", "updated_at")
