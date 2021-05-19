#!/bin/sh

# Collect static files in application server
# python manage.py migrate
# python manage.py collectstatic --no-input --clear
# python manage.py createsuperuser --username $DJANGO_SUPERUSER_USERNAME
gunicorn --bind 0.0.0.0:${WEBAPP_INTERNAL_PORT} --timeout 600 --chdir /home/app/web my_site.wsgi:application

exec "$@"