#!/bin/bash
set -e

# Create the default Nginx configuration file with a self-signed certificate
envsubst '${WEBAPP_HOSTNAME},${WEBAPP_INTERNAL_PORT},${REVERSE_PROXY_HOSTNAME},${HOME}' < /etc/nginx/conf.d/nginx.prod.template > /etc/nginx/conf.d/johnvorstne.me.conf

# Debugging
if [ $DEBUG ]; then
    cat /etc/nginx/conf.d/johnvorsten.me.conf
fi

# Start nginx
exec nginx -g 'daemon off;'