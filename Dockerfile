# Multi-stage build: Frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy frontend
COPY frontend/package*.json ./
RUN npm install

COPY frontend/public ./public
COPY frontend/src ./src

# Build frontend
RUN npm run build

# Stage 2: Backend with frontend
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy built frontend from builder
COPY --from=frontend-builder /app/frontend/build ./frontend/build

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Expose port
EXPOSE 8080

# Run using standalone server (avoids module caching issues)
CMD ["python", "run_server.py"]
