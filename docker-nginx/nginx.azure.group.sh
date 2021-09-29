#!/bin/bash

# Create the default Nginx configuration file with a self-signed certificate
envsubst '${WEBAPP_HOSTNAME_AZURE},${WEBAPP_INTERNAL_PORT},${REVERSE_PROXY_HOSTNAME}' < /etc/nginx/conf.d/nginx.azure.group.template > /etc/nginx/conf.d/nginx.conf

# Start nginx
exec nginx -g 'daemon off;'