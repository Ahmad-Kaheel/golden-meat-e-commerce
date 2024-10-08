#!/bin/sh
echo 'Waiting for postgres...'
while ! nc -z db 5432; do
    sleep 1
done
echo 'PostgreSQL started'
echo 'Running migrations...'
python manage.py migrate
echo 'Collecting static files...'
python manage.py collectstatic --no-input
exec "$@"