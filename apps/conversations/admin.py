from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("contact", "role", "created_at")
    list_filter = ("role",)
    search_fields = ("content",)
