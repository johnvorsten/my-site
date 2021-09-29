#!/bin/bash

# Create the default Nginx configuration file with a self-signed certificate
envsubst '${WEBAPP_HOSTNAME_LOCAL},${WEBAPP_INTERNAL_PORT},${REVERSE_PROXY_HOSTNAME},${PROXY_INTERNAL_PORT_HTTP},${PROXY_INTERNAL_PORT_HTTPS},${PROXY_EXTERNAL_PORT_HTTPS}' < /etc/nginx/conf.d/nginx.local.group.template > /etc/nginx/conf.d/nginx.conf

# Start nginx
exec nginx -g 'daemon off;'