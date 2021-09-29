I dont know exactly what the difference is between the different dockerfiles on this directory because I'm writing this on 2021-09-28, and the dockerfile was made back in 2020-03.  I'll try to include everything I can remember below.

## Summary of major differences:
The directory docker-nginx contains container files which start a Nginx proxy server
Dockerfiles with .local. in it are intended for testing on a development machine. They do not include an SSH server. The environment variables associated with these files are intended for debugging

Dockerfiels with .azure. in it are intended for deployment on an Microsoft Azure container group.  Individual containers communicate with each other through localhost ports.  The ports exposed on the server are different than those exposed in .local. files. An SSH server is installed and running for testing purposes.