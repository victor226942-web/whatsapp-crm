import redis
from celery import shared_task
from django.conf import settings

from apps.contacts.services import upsert_contact
from apps.conversations.services import get_recent_history, save_message
from apps.ai_engine.services import generate_reply
from .client import evolution_client
from .realtime import broadcast_new_message

_redis = redis.from_url(settings.REDIS_URL)

LOCK_TTL_SECONDS = 300  # 5 min — janela em que um messageId repetido é ignorado


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=10,
)
def process_message(self, instance_name, message_id, remote_jid, push_name, text):
    # 1. Idempotência: se a Evolution reenviar o mesmo webhook, isso aqui
    #    bloqueia o processamento duplicado. SET ... NX só grava se a chave
    #    não existir — atômico, sem race condition entre workers.
    lock_key = f"evo:msg:{instance_name}:{message_id}"
    acquired = _redis.set(lock_key, "1", nx=True, ex=LOCK_TTL_SECONDS)
    if not acquired:
        return  # já processada, ignora silenciosamente

    try:
        # 2. Upsert do contato (normaliza número, atualiza nome/timestamp)
        contact = upsert_contact(
            remote_jid=remote_jid, instance_name=instance_name, push_name=push_name
        )

        if contact.is_ai_paused:
            # atendente humano assumiu a conversa — só registra a mensagem
            user_msg = save_message(contact, role="user", content=text, external_id=message_id)
            broadcast_new_message(contact.id, {
                "id": user_msg.id, "role": "user", "content": text,
                "created_at": user_msg.created_at.isoformat(),
            })
            return

        # 3. Histórico recente para dar contexto à IA
        history = get_recent_history(contact, limit=10)

        # 4. Gera resposta
        reply = generate_reply(text, history)

        # 5. Envia via Evolution
        evolution_client.send_text(instance=instance_name, to=remote_jid, text=reply)

        # 6. Salva as duas mensagens no histórico e avisa o front em tempo real
        user_msg = save_message(contact, role="user", content=text, external_id=message_id)
        ai_msg = save_message(contact, role="assistant", content=reply)

        for msg in (user_msg, ai_msg):
            broadcast_new_message(contact.id, {
                "id": msg.id, "role": msg.role, "content": msg.content,
                "created_at": msg.created_at.isoformat(),
            })

    except Exception as exc:
        # Libera o lock em caso de erro real (não idempotência), para
        # permitir retry sem ficar travado pelos próximos 5 minutos
        _redis.delete(lock_key)
        raise self.retry(exc=exc)
