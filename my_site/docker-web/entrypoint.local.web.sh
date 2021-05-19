#!/bin/sh

# Make sure postgres is healthy before applying migrations
# And running server

# Check if the specified database is postgres
# $DATABASE is defined in .env
if ["$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres..."

    # Scan for a listening daemon on a host name and port
    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL started"
else
    echo "Database is not postgres"
fi

# Start Gunicorn on internal port (should be 8000)
gunicorn --bind 0.0.0.0:${WEBAPP_INTERNAL_PORT} --timeout 600 --chdir /home/app/web my_site.wsgi:application

exec "$@"