# Multi-stage Dockerfile for Library Management FastAPI Application
# Stage 1: Build stage - Install dependencies
# Stage 2: Runtime stage - Minimal production image

# =============================================================================
# Stage 1: Build Stage
# =============================================================================
FROM python:3.12-slim AS builder

# Set build-time metadata
LABEL maintainer="Library Management Team"
LABEL stage="builder"

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /build

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Create virtual environment and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies into virtual environment
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# =============================================================================
# Stage 2: Runtime Stage
# =============================================================================
FROM python:3.12-slim AS runtime

# Set production metadata
LABEL maintainer="Library Management Team"
LABEL version="1.0.0"
LABEL description="Library Management System - Book API"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    ENVIRONMENT="production" \
    DEBUG="False"

# Create non-root user for security
RUN groupadd -r appuser && \
    useradd -r -g appuser -u 1000 appuser && \
    mkdir -p /app /data && \
    chown -R appuser:appuser /app /data

# Set working directory
WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY --chown=appuser:appuser app/ ./app/
COPY --chown=appuser:appuser requirements.txt .

# Create directory for SQLite database with proper permissions
RUN mkdir -p /app/data && chown -R appuser:appuser /app/data

# Switch to non-root user
USER appuser

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# Health check (pings the /health endpoint every 30s)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Start the application with Uvicorn
# Using app.main:app format (module:app_instance)
# Host 0.0.0.0 to accept external connections in Docker
# Workers=1 for SQLite (SQLite doesn't support multiple concurrent writers)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
