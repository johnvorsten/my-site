#!/bin/sh

# Make sure postgres is healthy before applying migrations
# And running server

# Check if the specified database is postgres
# $DATABASE is defined in .env
if ["$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    # Scan for a listening daemon on a host name and port
    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL started"

fi



python manage.py flush --no-input
python manage.py migrate
python manage.py collectstatic --no-input --clear

exec "$@"