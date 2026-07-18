import json

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import InstanceStatus
from .realtime import broadcast_status_change
from .tasks import process_message


@csrf_exempt
@require_POST
def evolution_webhook(request):
    # Validação do token (a Evolution manda de volta o que você configurar
    # como header/query na criação da instância). Falha fechado: sem o
    # token configurado, o endpoint fica aberto pra qualquer um simular
    # mensagens do WhatsApp, então recusamos em vez de deixar passar.
    if not settings.EVOLUTION_WEBHOOK_TOKEN:
        return JsonResponse({"error": "EVOLUTION_WEBHOOK_TOKEN não configurado"}, status=500)
    token = request.headers.get("X-Webhook-Token", "")
    if token != settings.EVOLUTION_WEBHOOK_TOKEN:
        return JsonResponse({"error": "invalid token"}, status=401)

    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "invalid json"}, status=400)

    event = payload.get("event")
    instance = payload.get("instance")

    # Status de conexão: atualiza direto, é rápido e não precisa de fila
    if event == "connection.update":
        state = payload.get("data", {}).get("state", "unknown")
        InstanceStatus.objects.update_or_create(
            instance_name=instance, defaults={"state": state}
        )
        broadcast_status_change(instance, state)
        return JsonResponse({"ok": True})

    # Mensagem recebida: enfileira e responde rápido, o resto acontece
    # assíncrono no worker
    if event == "messages.upsert":
        message = (payload.get("data", {}).get("messages") or [None])[0]
        if not message or message.get("key", {}).get("fromMe"):
            return JsonResponse({"ok": True})  # ignora mensagens enviadas por nós mesmos

        text = (
            message.get("message", {}).get("conversation")
            or message.get("message", {}).get("extendedTextMessage", {}).get("text", "")
        )
        if not text:
            return JsonResponse({"ok": True})  # ignora mídia/áudio por enquanto

        process_message.delay(
            instance_name=instance,
            message_id=message["key"]["id"],
            remote_jid=message["key"]["remoteJid"],
            push_name=message.get("pushName", ""),
            text=text,
        )

    return JsonResponse({"ok": True})
