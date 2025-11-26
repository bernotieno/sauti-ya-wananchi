#!/bin/bash
# Railway startup script with better error handling

set -e  # Exit on error

echo "=== Sauti ya Wananchi Startup ==="
echo "Environment: ${RAILWAY_ENVIRONMENT:-development}"
echo "Port: ${PORT:-8000}"
echo ""

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "ERROR: DATABASE_URL is not set"
    echo "Make sure PostgreSQL database is linked in Railway"
    exit 1
fi

echo "✓ Database URL configured"

# Check if SECRET_KEY is set
if [ -z "$SECRET_KEY" ]; then
    echo "WARNING: SECRET_KEY is not set, using default (insecure!)"
else
    echo "✓ SECRET_KEY configured"
fi

# Run migrations
echo ""
echo "Running database migrations..."
python manage.py migrate --noinput

if [ $? -eq 0 ]; then
    echo "✓ Migrations completed successfully"
else
    echo "ERROR: Migrations failed"
    exit 1
fi

# Collect static files (if not done in build)
echo ""
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear || echo "Static collection skipped"

echo ""
echo "=== Starting Gunicorn Server ==="
echo "Binding to 0.0.0.0:${PORT:-8000}"
echo ""

# Start Gunicorn with appropriate settings
exec gunicorn config.wsgi:application \
    --bind "0.0.0.0:${PORT:-8000}" \
    --workers 2 \
    --worker-class sync \
    --worker-tmp-dir /dev/shm \
    --timeout 120 \
    --graceful-timeout 30 \
    --log-level info \
    --access-logfile - \
    --error-logfile - \
    --capture-output
