# WhatsApp CRM — Frontend

Clone funcional do WhatsApp Web (React + Vite + Tailwind), pra atender e
supervisionar as conversas que o backend automatiza. Roda em cima da API
do projeto Django em `../` (veja o README lá pra subir o backend primeiro).

## O que tem

- **Sidebar** com busca e lista de conversas ordenada pela mais recente,
  igual o WhatsApp faz quando chega mensagem nova.
- **Badge de status da instância** (verde/amarelo/vermelho) e **modal de
  QR Code** pra parear o número — some sozinho assim que a conexão abre.
- **Balão "IA"** em cada mensagem respondida automaticamente, pra você
  saber o que foi piloto automático.
- **Botão de handoff**: "assumir conversa" pausa a IA pro contato atual
  (o backend para de responder automaticamente) e deixa você digitar
  direto — sem editar nada no banco.
- **Tempo real via WebSocket** — mensagem nova aparece sem dar refresh,
  reconecta sozinho se a conexão cair.

## Rodando

```bash
cp .env.example .env
npm install
npm run dev
```

Por padrão espera o backend em `http://localhost:8000` (API) e
`ws://localhost:8000/ws/chat/` (WebSocket) — ajuste no `.env` se for
diferente.

## Próximos passos naturais

- Autenticação (hoje qualquer um que acesse a URL vê todas as conversas)
- Indicador de "digitando…" e confirmação de leitura (dois vistos)
- Envio de mídia (a Evolution suporta, o backend ainda só trata texto)
