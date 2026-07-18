# WhatsApp CRM — Backend

Backend em Django para automatizar atendimento no WhatsApp via **Evolution API**,
com respostas geradas por IA e uma base de CRM (contatos + histórico de conversa).

## Por que essa arquitetura

A Evolution API tem dois problemas conhecidos:

1. **Conexão instável** — a instância pode cair, reconectar, ou reenviar o mesmo
   webhook duas vezes.
2. **Contatos bagunçados** — o JID (`5522999999999@s.whatsapp.net`) vem cru, sem
   padronização, e não existe fonte única de verdade sobre quem é quem.

A solução para os dois problemas é a mesma: **nunca confiar direto no webhook**.
O webhook só enfileira o evento. Um worker separado (Celery) processa a fila com:

- **Idempotência** (Redis `SETNX` no `messageId`) → nunca responde a mesma
  mensagem duas vezes, mesmo se a Evolution reenviar o webhook.
- **Upsert de contato** → toda mensagem passa por uma normalização de número e
  atualização de um registro único de contato (isso é o "CRM").
- **Status de conexão desacoplado** → o status da instância (`open`,
  `connecting`, `close`) é salvo no banco a cada evento `connection.update`,
  então o resto do sistema nunca precisa perguntar "a instância tá online?"
  direto pra Evolution — ele consulta o banco.

## Fluxo

```
WhatsApp → Evolution API → POST /webhook/evolution/
                                    │
                          (view só valida e responde 200 rápido)
                                    │
                          apps.integrations.evolution.tasks.process_message.delay()
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │ Celery worker                  │
                    │ 1. Lock Redis (idempotência)   │
                    │ 2. Upsert Contact               │
                    │ 3. Busca histórico (Conversation)│
                    │ 4. Chama AIEngine               │
                    │ 5. Envia resposta (Evolution)   │
                    │ 6. Salva Message (user + bot)   │
                    └───────────────────────────────┘
```

## Apps

- `apps/contacts` — modelo `Contact`, normalização de número, upsert.
- `apps/conversations` — modelo `Conversation` e `Message`, histórico por contato.
- `apps/integrations/evolution` — webhook, cliente HTTP da Evolution, tasks Celery.
- `apps/ai_engine` — camada que fala com o modelo de IA (troca de provider sem
  tocar no resto do sistema).

## Rodando localmente

```bash
cp .env.example .env
docker compose up -d          # sobe Postgres, Redis, Evolution API, backend e worker
python manage.py migrate
```

Em desenvolvimento local (fora do Docker), suba com Daphne (ASGI, pra ter
WebSocket funcionando) em vez do `runserver` padrão:

```bash
daphne -b 0.0.0.0 -p 8000 whatsapp_crm.asgi:application
celery -A whatsapp_crm worker -l info   # worker separado, outro terminal
```

## Frontend

O clone do WhatsApp Web (React + Vite + Tailwind) fica em `frontend/` —
veja o README lá pra rodar. Ele consome a API REST (`/api/...`) e o
WebSocket (`/ws/chat/`) que este backend expõe.

A API inteira exige login (token via `rest_framework.authtoken`). Pra
criar o primeiro usuário atendente:

```bash
python manage.py createsuperuser
```

Use esse usuário e senha na tela de login do frontend.

## Deploy no Railway

O projeto tem **5 serviços** dentro de um mesmo projeto Railway. Postgres e
Redis são os plugins nativos do Railway (2 cliques, já geram `DATABASE_URL`
e `REDIS_URL` sozinhos). Os outros 3 apontam pra este repositório/imagem:

| Serviço        | Fonte                                   | Start Command (override) |
|----------------|------------------------------------------|---------------------------|
| `postgres`     | Plugin Railway                            | —                         |
| `redis`        | Plugin Railway                            | —                         |
| `evolution-api`| Docker Image `atendai/evolution-api:latest` | —                       |
| `backend`      | Este repo, `Dockerfile` na raiz            | (usa o `CMD` do Dockerfile — Daphne) |
| `worker`       | Este repo, **mesmo** `Dockerfile` da raiz  | `celery -A whatsapp_crm worker -l info` |
| `frontend`     | Este repo, `frontend/Dockerfile`           | (usa o `CMD` do Dockerfile — `serve`) |

O `backend` e o `worker` reusam a mesma imagem Docker — no Railway, crie os
dois serviços apontando pro mesmo repo/Dockerfile e só troque o **Start
Command** do `worker` nas configurações do serviço.

### Variáveis de ambiente por serviço

**`backend`** e **`worker`** (as mesmas nos dois):
```
SECRET_KEY=<gere uma chave forte>
DEBUG=False
ALLOWED_HOSTS=<domínio público do backend, ex: meu-backend.up.railway.app>
CSRF_TRUSTED_ORIGINS=https://<domínio público do backend>
CORS_ALLOWED_ORIGINS=https://<domínio público do frontend>
DATABASE_URL=${{Postgres.DATABASE_URL}}   # referência ao plugin, Railway resolve sozinho
REDIS_URL=${{Redis.REDIS_URL}}
CELERY_BROKER_URL=${{Redis.REDIS_URL}}
EVOLUTION_API_URL=https://<domínio público do serviço evolution-api>
EVOLUTION_API_KEY=<mesma chave do AUTHENTICATION_GLOBAL_KEY abaixo>
EVOLUTION_WEBHOOK_TOKEN=<um token seu, qualquer string forte>
OPENAI_API_KEY=<sua chave>
AI_MODEL=gpt-4o-mini
```

**`evolution-api`**:
```
AUTHENTICATION_GLOBAL_KEY=<mesma chave do EVOLUTION_API_KEY acima>
SERVER_URL=https://<domínio público do próprio serviço evolution-api>
WEBHOOK_GLOBAL_ENABLED=true
WEBHOOK_GLOBAL_URL=https://<domínio público do backend>/webhook/evolution/
```

**`frontend`** — **atenção**: essas duas são embutidas no bundle em tempo de
*build*, então precisam estar configuradas *antes* do primeiro deploy do
serviço (não é só variável de runtime):
```
VITE_API_URL=https://<domínio público do backend>/api
VITE_WS_URL=wss://<domínio público do backend>/ws/chat/
```

### Checklist de primeiro deploy

1. Suba `postgres` e `redis` (plugins).
2. Suba `evolution-api` com as variáveis acima, gere o QR code e pareie o WhatsApp.
3. Suba `backend`, rode `python manage.py createsuperuser` via `railway run` pra criar o primeiro atendente.
4. Suba `worker` (mesma imagem, Start Command trocado).
5. Suba `frontend` com `VITE_API_URL`/`VITE_WS_URL` já definidos.

## Próximos passos sugeridos (CRM de verdade)

Esse esqueleto cobre a automação de resposta. Para virar CRM de fato, os
próximos módulos naturais são:

- **Pipeline/Kanban** por contato (status: novo → em atendimento → fechado)
- **Handoff humano** — campo `is_ai_paused` no `Contact` pra um atendente
  assumir a conversa e a IA parar de responder automaticamente
- **Multi-instância** — hoje o modelo já suporta várias instâncias Evolution
  por `instance_name`, útil se você tiver mais de um número/WhatsApp
- **Dashboard** — métricas de volume de mensagens, tempo de resposta, taxa de
  handoff
