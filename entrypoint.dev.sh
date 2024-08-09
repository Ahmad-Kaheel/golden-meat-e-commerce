#!/bin/sh

echo 'Running migrations...'
python manage.py migrate


echo 'Starting development server...'
exec python manage.py runserver 0.0.0.0:8000
