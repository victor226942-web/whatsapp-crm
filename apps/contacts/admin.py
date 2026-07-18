from django.contrib import admin

from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("push_name", "phone", "instance_name", "status", "is_ai_paused", "last_interaction")
    list_filter = ("status", "is_ai_paused", "instance_name")
    search_fields = ("phone", "push_name")
