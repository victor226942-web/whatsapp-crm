from django.db import models


class Contact(models.Model):
    """
    Fonte única de verdade sobre um contato do WhatsApp.

    O número é sempre salvo já normalizado (sem @s.whatsapp.net, sem
    caracteres extras), então toda outra parte do sistema (conversas,
    IA, dashboard) trabalha com um identificador limpo e consistente.
    """

    phone = models.CharField(max_length=20, db_index=True)
    instance_name = models.CharField(max_length=100, db_index=True)
    push_name = models.CharField(max_length=150, blank=True, default="")

    # Kanban/CRM básico: status do atendimento
    STATUS_CHOICES = [
        ("new", "Novo"),
        ("in_service", "Em atendimento"),
        ("closed", "Encerrado"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")

    # Handoff humano: quando True, a IA para de responder automaticamente
    is_ai_paused = models.BooleanField(default=False)

    last_interaction = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("phone", "instance_name")
        indexes = [models.Index(fields=["phone", "instance_name"])]

    def __str__(self):
        return f"{self.push_name or self.phone} ({self.instance_name})"
