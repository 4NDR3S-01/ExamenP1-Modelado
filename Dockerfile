# Dockerfile multi-stage para Next.js (frontend) y FastAPI (backend) en un solo contenedor

# Etapa 1: Construcción del frontend
FROM node:20-alpine AS frontend-build
WORKDIR /app/agent-ui
COPY agent-ui/package.json ./
COPY agent-ui/pnpm-lock.yaml ./
COPY agent-ui ./
RUN npm install -g pnpm && pnpm install && pnpm build

# Etapa 2: Construcción del backend
FROM python:3.11-slim AS backend-build
WORKDIR /app
COPY playground.py ./
COPY tmp ./tmp
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Imagen final
FROM python:3.11-slim
WORKDIR /app

# Copia el backend
COPY --from=backend-build /app /app

# Copia el frontend estático
COPY --from=frontend-build /app/agent-ui/.next /app/frontend/.next
COPY --from=frontend-build /app/agent-ui/public /app/frontend/public
COPY --from=frontend-build /app/agent-ui/package.json /app/frontend/package.json

# Instala nginx y dependencias mínimas
RUN pip install --no-cache-dir uvicorn fastapi && \
    apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# Copia la configuración y el script de inicio
COPY nginx.conf /etc/nginx/nginx.conf
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 80

CMD ["/start.sh"]

