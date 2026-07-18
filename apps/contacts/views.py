from rest_framework.generics import ListAPIView, UpdateAPIView

from .models import Contact
from .serializers import ContactSerializer


class ContactListView(ListAPIView):
    """
    GET /api/contacts/  — lista de conversas para a sidebar, já ordenada
    pela mensagem mais recente (igual o WhatsApp faz).
    """
    serializer_class = ContactSerializer

    def get_queryset(self):
        return Contact.objects.all().order_by("-last_interaction")


class ContactUpdateView(UpdateAPIView):
    """
    PATCH /api/contacts/<id>/  — usado para pausar/retomar a IA
    (handoff humano) e mudar o status do atendimento (kanban básico).
    """
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()
