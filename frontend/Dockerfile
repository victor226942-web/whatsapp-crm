FROM node:20-alpine AS build
WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

# VITE_API_URL e VITE_WS_URL são embutidos no bundle NESTE momento (build),
# não em runtime — no Railway, defina essas variáveis no serviço de
# frontend ANTES de fazer o deploy, apontando pro domínio público do backend.
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
RUN npm install -g serve
COPY --from=build /app/dist ./dist

EXPOSE 4173
CMD ["sh", "-c", "serve -s dist -l ${PORT:-4173}"]
