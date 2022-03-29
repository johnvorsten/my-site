## Docker-compose for production
https://docs.docker.com/compose/production/
* (done) Remove unnecessary volumes before production
* (done) Bind to the correct ports on the host
* (done) Set environment variables correct for the environment (database, secret keys, authentication tokens)
* (done) restart:always
* (done) Add a log aggregator for the service

## Common command line instructions:
Build docker files from compose for local test containers `docker compose -f ./docker-deploy/docker-compose.test.yml build`
Create containers and start the container `docker compose -f ./docker-deploy/docker-compose.test.yml up`. -d for detached mode
Start containers for local testing (if the container has already been created) `docker compose -f ./docker-deploy/docker-compose.test.yml start`
Stop containers `docker compose -f ./docker-deploy/docker-compose.test.yml stop`
To rebuild after code changes `docker compose build web` & `docker compose up --no-deps -d web`
Note - `docker compose up` will build, recreate, and start containers
Use `d` to run in detached mode

## Manual files (Remplace these before rebuilding for production)
/docker-deploy/docker-compose.test.env
/docker-deploy/letsencrypt_archive.tar.gz
/my_site/production.secret
/my_site/static-serve/

## Deployment instructions
Log onto production computer
pull latest changes from git
Update any credentials if necessary
collect static files `python manage.py collectstatic`
Copy media files if excluded from git repository
Rebuild docker files `docker compose -f ./docker-deploy/docker-compose.prod.yml build`
Create and start images `docker compose -f ./docker-deploy/docker-compose.prod.yml up -d`
Renew letsencrypt/certbot certificates `certbot renew`

## Debugging
#### Get a bash shell in running container
docker ps
docker exec -it <container hash> /bin/sh
#### Gunicorn log file
See log file at project root.. /home/app/web/my-site/my_site/my_site.log
#### Nginx logging
Access and error logs should be redirected to standard output and error
docker logs <container name or ID> | docker logs docker-deploy-nginx-1

## Change during production
proxy hostname environment variable

## Symbolic links
Create relative symbolic links for letsencrypt volumnes (this works with windows10 and docker 4.2.0). Absolute symbolic links do not work