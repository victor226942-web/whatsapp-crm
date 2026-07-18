from django.db import models

from apps.contacts.models import Contact


class Message(models.Model):
    ROLE_CHOICES = [
        ("user", "Usuário"),
        ("assistant", "Assistente (IA)"),
        ("agent", "Atendente humano"),
    ]

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()

    # messageId que veio da Evolution — guardado também aqui (não só no lock
    # do Redis) pra permitir auditoria e reprocessamento manual se precisar.
    external_id = models.CharField(max_length=100, blank=True, default="", db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"[{self.role}] {self.content[:40]}"
