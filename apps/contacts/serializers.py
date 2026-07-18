from rest_framework import serializers

from apps.conversations.models import Message
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    last_message_at = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = [
            "id", "phone", "instance_name", "push_name", "status",
            "is_ai_paused", "last_interaction", "last_message", "last_message_at",
        ]

    def get_last_message(self, obj):
        msg = obj.messages.order_by("-created_at").first()
        return msg.content if msg else ""

    def get_last_message_at(self, obj):
        msg = obj.messages.order_by("-created_at").first()
        return msg.created_at if msg else obj.last_interaction
