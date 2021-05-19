#!/bin/bash

# This file will substitute environment variables available to the script
# Into the Nginx configuration file located at etc/nginx/conf.d/nginx.vm.template
# And create the file /etc/nginx/conf.d/nginx.conf

## Example before substitution ##
# server {
#     if ($host = www.${REVERSE_PROXY_HOSTNAME}) {
#         return 301 https://${REVERSE_PROXY_HOSTNAME}$request_uri;
#     } 

#     if ($host = ${REVERSE_PROXY_HOSTNAME}) {
#         return 301 https://${REVERSE_PROXY_HOSTNAME}$request_uri;
#     } 

#     listen 80;
#     server_name ${REVERSE_PROXY_HOSTNAME} www.${REVERSE_PROXY_HOSTNAME};
#     return 404; 
# }

## After substitution ##
# server {
#     if ($host = www.johnvorsten.me}) {
#         return 301 https://johnvorsten.me$request_uri;
#     } 

#     if ($host = johnvorsten.me) {
#         return 301 https://johnvorsten.me$request_uri;
#     } 

#     listen 80;
#     server_name johnvorsten.me www.johnvorsten.me;
#     return 404; 
# }

# Create the default Nginx configuration file with a self-signed certificate
envsubst '${WEBAPP_HOSTNAME_AZURE},${WEBAPP_INTERNAL_PORT},${REVERSE_PROXY_HOSTNAME}' < /etc/nginx/conf.d/nginx.vm.template > /etc/nginx/conf.d/nginx.conf

# Start nginx
exec nginx -g 'daemon off;'