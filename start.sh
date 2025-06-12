#!/bin/sh
# Inicia el backend en /api
uvicorn playground:app --host 0.0.0.0 --port 8000 &
# Inicia nginx para servir el frontend
nginx -g 'daemon off;'
