import httpx
from django.conf import settings


class EvolutionClient:
    def __init__(self):
        self.base_url = settings.EVOLUTION_API_URL
        self.headers = {"apikey": settings.EVOLUTION_API_KEY}

    def send_text(self, instance: str, to: str, text: str) -> None:
        url = f"{self.base_url}/message/sendText/{instance}"
        with httpx.Client(timeout=15) as client:
            resp = client.post(url, json={"number": to, "text": text}, headers=self.headers)
            resp.raise_for_status()

    def get_connection_state(self, instance: str) -> str:
        url = f"{self.base_url}/instance/connectionState/{instance}"
        with httpx.Client(timeout=10) as client:
            resp = client.get(url, headers=self.headers)
            resp.raise_for_status()
            return resp.json().get("instance", {}).get("state", "unknown")

    def get_qrcode(self, instance: str) -> str | None:
        """Retorna o QR code (base64) para parear o WhatsApp, se disponível."""
        url = f"{self.base_url}/instance/connect/{instance}"
        with httpx.Client(timeout=10) as client:
            resp = client.get(url, headers=self.headers)
            resp.raise_for_status()
            return resp.json().get("base64")


evolution_client = EvolutionClient()
