#!/usr/bin/env bash
# Unified start script for Swahilipot Hub Portal.
# Development  (DJANGO_DEBUG=True or not set)  → Django dev server with hot-reload
# Production   (DJANGO_DEBUG=False via secrets) → Gunicorn (production WSGI server)
set -e
cd "$(dirname "$0")"

DEBUG_VAL="${DJANGO_DEBUG:-True}"

if [ "$DEBUG_VAL" = "False" ] || [ "$DEBUG_VAL" = "false" ] || [ "$DEBUG_VAL" = "0" ]; then
  echo "[start] Production mode — Gunicorn"

  echo "[start] Collecting static files..."
  python manage.py collectstatic --noinput

  echo "[start] Applying migrations..."
  python manage.py migrate --noinput

  echo "[start] Starting Gunicorn on port ${PORT:-8000}..."
  exec gunicorn swahilipot_portal.wsgi:application \
    --bind "0.0.0.0:${PORT:-8000}" \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
else
  echo "[start] Development mode — Django runserver (hot-reload enabled)"
  python manage.py migrate --noinput 2>/dev/null || true
  exec python manage.py runserver "0.0.0.0:${PORT:-8000}"
fi
