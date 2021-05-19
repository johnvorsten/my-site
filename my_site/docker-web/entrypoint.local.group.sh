#!/bin/sh

# Collect static files in application server
gunicorn --bind 0.0.0.0:${WEBAPP_INTERNAL_PORT} --timeout 600 --chdir /home/app/web my_site.wsgi:application

exec "$@"