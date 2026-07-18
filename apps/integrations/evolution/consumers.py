import json
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .realtime import GROUP_NAME


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Um único canal global (grupo "chat_updates") pra manter simples: todo
    cliente conectado recebe todo evento de mensagem/status. Se no futuro
    você tiver múltiplos atendentes e quiser granularidade por instância,
    dá pra trocar por um grupo por instance_name sem mudar o resto.

    A autenticação aqui é via token (mesmo token do login REST) passado
    como query string (?token=...), porque o AuthMiddlewareStack padrão do
    Channels só entende sessão de cookie, e o front usa TokenAuthentication.
    """

    async def connect(self):
        token = parse_qs(self.scope["query_string"].decode()).get("token", [None])[0]
        user = await self._get_user(token)
        if user is None:
            await self.close(code=4001)
            return

        await self.channel_layer.group_add(GROUP_NAME, self.channel_name)
        await self.accept()

    @database_sync_to_async
    def _get_user(self, token):
        if not token:
            return None
        from rest_framework.authtoken.models import Token
        try:
            return Token.objects.select_related("user").get(key=token).user
        except Token.DoesNotExist:
            return None

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(GROUP_NAME, self.channel_name)

    async def broadcast_event(self, event):
        await self.send(text_data=json.dumps({
            "type": event["event"],
            "payload": event["payload"],
        }))
