## Docker-compose for production
https://docs.docker.com/compose/production/
* Remove volumes before production
* Bind to the correct ports on the host
* Set environment variables correct for the environment (database, secret keys, authentication tokens)
* restart:always
* Add a log aggregator for the service

## Common command line instructions:
Build docker files from compose for local test containers `docker compose -f ./docker-deploy/docker-compose.test.yml build`
Create containers and start the container `docker compose -f ./docker-deploy/docker-compose.test.yml up`
Start containers for local testing (if the container has already been created) `docker compose -f ./docker-deploy/docker-compose.test.yml start`
Stop containers `docker compose -f ./docker-deploy/docker-compose.test.yml stop`
To rebuild after code changes `docker compose build web` & `docker compose up --no-deps -d web`
Note - `docker compose up` will build, recreate, and start containers

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

