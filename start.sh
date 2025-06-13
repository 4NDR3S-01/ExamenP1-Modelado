#!/bin/bash

# Startup script for Cloud Run
set -e

echo "🚀 Starting Agent Playground..."
echo "Port: ${PORT:-7777}"
echo "Python version: $(python --version)"

# Check if tmp directory exists and create if not
if [ ! -d "tmp" ]; then
    echo "📁 Creating tmp directory..."
    mkdir -p tmp
    chmod 755 tmp
fi

# Initialize database if needed
echo "🗄️ Initializing database..."
python -c "
import sqlite3
import os
db_path = 'tmp/agents.db'
if not os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    conn.close()
    print('Database initialized')
else:
    print('Database already exists')
"

# Start the application
echo "🌟 Starting Uvicorn server on port ${PORT:-7777}..."
exec python -m uvicorn playground:app \
    --host 0.0.0.0 \
    --port ${PORT:-7777} \
    --log-level info \
    --access-log \
    --timeout-keep-alive 5 \
    --timeout-graceful-shutdown 30
