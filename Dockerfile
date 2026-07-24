FROM python:3.12-slim

# =============================================================================
# Environment variables
# =============================================================================
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DJANGO_SETTINGS_MODULE=swahilipot_portal.settings

# =============================================================================
# Working directory
# =============================================================================
WORKDIR /app

# =============================================================================
# System dependencies
# =============================================================================
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# =============================================================================
# Python dependencies
# =============================================================================
COPY requirements.txt .

RUN python -m pip install --upgrade pip setuptools wheel && \
    python -m pip install -r requirements.txt && \
    python -m pip install gunicorn psycopg2-binary

# =============================================================================
# Copy project
# =============================================================================
COPY . .

# =============================================================================
# Create required directories
# =============================================================================
RUN mkdir -p /app/staticfiles /app/media /app/logs

# =============================================================================
# Copy entrypoint
# =============================================================================
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# =============================================================================
# Collect static files at build time
# =============================================================================
RUN DJANGO_SECRET_KEY=build-secret \
    DJANGO_DEBUG=False \
    python manage.py collectstatic --noinput

# =============================================================================
# Create non-root user
# =============================================================================
RUN groupadd --system app && \
    useradd --system --gid app --create-home app && \
    chown -R app:app /app

USER app

# =============================================================================
# Network
# =============================================================================
EXPOSE 8000

# =============================================================================
# Health check
# =============================================================================
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/', timeout=5)" || exit 1

# =============================================================================
# Start application
# =============================================================================
ENTRYPOINT ["/app/docker-entrypoint.sh"]