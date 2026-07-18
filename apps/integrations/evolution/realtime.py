"""
Helpers para publicar eventos no grupo WebSocket "chat_updates".
Usado pela task Celery (nova mensagem) e pela view do webhook
(mudança de status de conexão), pra manter o front-end em tempo real
sem ele precisar dar polling.
"""
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

GROUP_NAME = "chat_updates"


def _send(event_type: str, payload: dict) -> None:
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return  # channel layer não configurado (ex: em testes) — no-op
    async_to_sync(channel_layer.group_send)(
        GROUP_NAME, {"type": "broadcast_event", "event": event_type, "payload": payload}
    )


def broadcast_new_message(contact_id: int, message: dict) -> None:
    _send("new_message", {"contact_id": contact_id, "message": message})


def broadcast_status_change(instance_name: str, state: str) -> None:
    _send("status_change", {"instance_name": instance_name, "state": state})
