FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Sem variáveis de ambiente reais no build (usa os defaults do settings.py) —
# não precisa de banco/redis pra gerar os arquivos estáticos do admin.
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Roda as migrations a cada boot (idempotente) antes de subir o servidor.
# No Railway, o serviço de worker reusa essa mesma imagem mas sobrescreve o
# Start Command para "celery -A whatsapp_crm worker -l info".
CMD ["sh", "-c", "python manage.py migrate --noinput && daphne -b 0.0.0.0 -p ${PORT:-8000} whatsapp_crm.asgi:application"]
