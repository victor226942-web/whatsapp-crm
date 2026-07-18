from django.conf import settings
from openai import OpenAI

_client = OpenAI(api_key=settings.OPENAI_API_KEY)

SYSTEM_PROMPT = (
    "Você é um assistente de atendimento via WhatsApp. Seja direto, "
    "educado e objetivo. Nunca invente informação que você não tem."
)


def generate_reply(user_message: str, history: list[dict]) -> str:
    """
    `history` já vem no formato [{"role": "user"/"assistant", "content": "..."}]
    (ver apps.conversations.services.get_recent_history).
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    response = _client.chat.completions.create(
        model=settings.AI_MODEL,
        messages=messages,
        temperature=0.6,
    )
    return response.choices[0].message.content
