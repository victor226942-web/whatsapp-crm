from apps.contacts.models import Contact
from .models import Message


def get_recent_history(contact: Contact, limit: int = 10) -> list[dict]:
    messages = contact.messages.order_by("-created_at")[:limit]
    # devolve em ordem cronológica, formato pronto pro provider de IA
    return [
        {"role": m.role, "content": m.content}
        for m in reversed(messages)
    ]


def save_message(contact: Contact, role: str, content: str, external_id: str = "") -> Message:
    return Message.objects.create(
        contact=contact, role=role, content=content, external_id=external_id
    )
