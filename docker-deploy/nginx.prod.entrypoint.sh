#!/bin/bash
set -e

# Create the default Nginx configuration file with a self-signed certificate
envsubst '${WEBAPP_HOSTNAME},${WEBAPP_INTERNAL_PORT},${REVERSE_PROXY_HOSTNAME},${HOME},${MIL_HOSTNAME},${MIL_PORT},${RANKING_PORT},${RANKING_HOSTNAME}' < /etc/nginx/conf.d/nginx.prod.template > /etc/nginx/conf.d/johnvorsten.me.conf

# Debugging
if [ $DEBUG = "TRUE" ]; then
    cat /etc/nginx/conf.d/johnvorsten.me.conf
fi

# Start nginx
exec nginx -g 'daemon off;'