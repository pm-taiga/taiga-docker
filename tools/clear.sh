#!/bin/bash
cd ..

rm docker-compose.yml
rm -rf temp

docker rm $(docker ps -a -q)
docker volume prune -f

docker rmi taiga-docker_backend taiga-docker_celeryworker taiga-docker_events taiga-docker_frontend