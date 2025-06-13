# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    g++ \
    gcc \
    pkg-config \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create tmp directory for database, set permissions, and create user
RUN mkdir -p tmp && \
    chmod 755 tmp && \
    useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app

USER app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=7777
ENV PYTHONPATH=/app

# Expose port
EXPOSE 7777

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7777/health || exit 1

# Run the application
CMD ["python", "-m", "uvicorn", "playground:app", "--host", "0.0.0.0", "--port", "7777", "--log-level", "info"]
