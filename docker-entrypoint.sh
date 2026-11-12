#!/bin/sh
set -e

echo "==> [entrypoint] Ejecutando migraciones..."
python manage.py migrate --noinput

echo "==> [entrypoint] Recolectando estaticos..."
python manage.py collectstatic --noinput --clear

echo "==> [entrypoint] Verificando configuracion..."
python manage.py check --deploy 2>/dev/null || python manage.py check

echo "==> [entrypoint] Verificando superusuario..."
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@email.com', '12345')"

echo "==> [entrypoint] Iniciando Gunicorn en 0.0.0.0:${PORT:-8000}..."
exec gunicorn core.wsgi \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --timeout 120 \
    --log-file - \
    --access-logfile -