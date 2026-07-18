from rest_framework.generics import ListAPIView

from apps.contacts.models import Contact
from .models import Message
from .serializers import MessageSerializer


class MessageListView(ListAPIView):
    """GET /api/contacts/<contact_id>/messages/ — histórico completo do chat."""
    serializer_class = MessageSerializer

    def get_queryset(self):
        contact_id = self.kwargs["contact_id"]
        return Message.objects.filter(contact_id=contact_id).order_by("created_at")
