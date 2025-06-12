# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create tmp directory for database
RUN mkdir -p tmp

# Expose port
EXPOSE 7777

# Run the application
CMD ["python", "-m", "uvicorn", "playground:app", "--host", "0.0.0.0", "--port", "7777"]
