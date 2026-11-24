#!/bin/sh
set -e

if [ "$#" -gt 0 ]; then
    echo "==> [entrypoint] Ejecutando comando: $*"
    exec "$@"
fi

echo "==> [entrypoint] Ejecutando migraciones de base de datos..."
python manage.py migrate --noinput

echo "==> [entrypoint] Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "==> [entrypoint] Verificando la configuración de Django..."
python manage.py check --deploy 2>/dev/null || python manage.py check

echo "==> [entrypoint] Verificando y creando superusuario..."
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@email.com', '12345')"

if [ "${CELERY_EMBEDDED_WORKER:-0}" = "1" ] && [ -n "${REDIS_URL:-}" ]; then
    BEAT_OPTS=""
    if [ "${CELERY_EMBEDDED_BEAT:-1}" = "1" ]; then
        BEAT_OPTS="--beat --schedule=/tmp/celerybeat-schedule"
        echo "==> [entrypoint] Celery Beat embebido ACTIVADO (reporte diario ${REPORTE_DIARIO_HORA:-08:00} hora MX)."
    fi
    echo "==> [entrypoint] Iniciando worker de Celery embebido (cola erp_django)..."
    # shellcheck disable=SC2086
    celery -A core worker \
        --loglevel=info \
        --queues=erp_django \
        --pool=solo \
        --without-gossip --without-mingle --without-heartbeat \
        $BEAT_OPTS &
else
    echo "==> [entrypoint] Worker de Celery embebido DESACTIVADO."
fi

echo "==> [entrypoint] Iniciando Gunicorn en 0.0.0.0:${PORT:-8000}..."
exec gunicorn core.wsgi \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --timeout 120 \
    --log-file - \
    --access-logfile -