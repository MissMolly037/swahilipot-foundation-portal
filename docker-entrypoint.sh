#!/bin/sh
set -eu

echo "🚀 Starting Swahilipot Foundation Portal..."

# =============================================================================
# Database configuration
# =============================================================================
DB_HOST="${POSTGRES_HOST:-postgres}"
DB_PORT="${POSTGRES_PORT:-5432}"
DB_NAME="${POSTGRES_DB:-swahilipot}"
DB_USER="${POSTGRES_USER:-swahilipot}"
DB_PASSWORD="${POSTGRES_PASSWORD:-swahilipot}"

# =============================================================================
# Wait for PostgreSQL
# =============================================================================
if [ -n "${DATABASE_URL:-}" ] && echo "$DATABASE_URL" | grep -q "postgres"; then
  echo "⏳ Waiting for PostgreSQL at ${DB_HOST}:${DB_PORT}..."

  until python - <<'PY'
import os
import sys
import psycopg2

try:
    conn = psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST', 'postgres'),
        port=os.environ.get('POSTGRES_PORT', '5432'),
        dbname=os.environ.get('POSTGRES_DB', 'swahilipot'),
        user=os.environ.get('POSTGRES_USER', 'swahilipot'),
        password=os.environ.get('POSTGRES_PASSWORD', 'swahilipot'),
    )
    conn.close()
    sys.exit(0)
except Exception:
    sys.exit(1)
PY
  do
    echo "PostgreSQL is not ready yet. Retrying in 2 seconds..."
    sleep 2
  done

  echo "✅ PostgreSQL is ready."
else
  echo "🗄️ Using SQLite; skipping PostgreSQL readiness check."
fi

# =============================================================================
# Apply migrations
# =============================================================================
echo "📦 Applying database migrations..."
python manage.py migrate --noinput

# =============================================================================
# Collect static files
# =============================================================================
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

# =============================================================================
# Create superuser if configured
# =============================================================================
if [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ] && \
   [ -n "${DJANGO_SUPERUSER_EMAIL:-}" ] && \
   [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then

  echo "👤 Creating superuser if needed..."

  python manage.py shell <<'PY'
import os
from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ['DJANGO_SUPERUSER_USERNAME']
email = os.environ['DJANGO_SUPERUSER_EMAIL']
password = os.environ['DJANGO_SUPERUSER_PASSWORD']

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print('Superuser created.')
else:
    print('Superuser already exists.')
PY
fi

# =============================================================================
# Start Gunicorn
# =============================================================================
echo "🌐 Starting Gunicorn on port 8000..."
exec gunicorn \
    --config gunicorn.conf.py \
    swahilipot_portal.wsgi:application