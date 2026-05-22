#!/bin/sh
set -e

python manage.py collectstatic --noinput

gunicorn config.wsgi:application -b 0.0.0.0:8000 --workers 3 --timeout 120
