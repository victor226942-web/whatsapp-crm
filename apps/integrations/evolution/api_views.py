from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.contacts.models import Contact
from apps.conversations.services import save_message
from .client import evolution_client
from .models import InstanceStatus
from .realtime import broadcast_new_message


class InstanceStatusView(APIView):
    """GET /api/evolution/status/?instance=<nome> — pro badge verde/amarelo/vermelho."""

    def get(self, request):
        instance = request.query_params.get("instance", "default")
        status_obj = InstanceStatus.objects.filter(instance_name=instance).first()
        return Response({"instance": instance, "state": status_obj.state if status_obj else "close"})


class InstanceQRCodeView(APIView):
    """GET /api/evolution/qrcode/?instance=<nome> — pro modal de pareamento."""

    def get(self, request):
        instance = request.query_params.get("instance", "default")
        qrcode = evolution_client.get_qrcode(instance)
        return Response({"instance": instance, "qrcode": qrcode})


class SendMessageView(APIView):
    """
    POST /api/send-message/  { "contact_id": 1, "text": "..." }

    Usado quando o ATENDENTE HUMANO digita direto na interface (não a IA).
    Isso é o que dá o "modo manual" — geralmente disparado depois que o
    operador pausa a IA (is_ai_paused=True) numa conversa específica.
    """

    def post(self, request):
        contact_id = request.data.get("contact_id")
        text = request.data.get("text", "").strip()
        if not contact_id or not text:
            return Response({"error": "contact_id e text são obrigatórios"}, status=400)

        contact = get_object_or_404(Contact, pk=contact_id)
        remote_jid = f"{contact.phone}@s.whatsapp.net"

        evolution_client.send_text(instance=contact.instance_name, to=remote_jid, text=text)
        message = save_message(contact, role="agent", content=text)

        broadcast_new_message(contact.id, {
            "id": message.id, "role": "agent", "content": text,
            "created_at": message.created_at.isoformat(),
        })
        return Response({"ok": True})
