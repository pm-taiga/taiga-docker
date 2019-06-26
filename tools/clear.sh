#!/bin/bash
cd ..

rm docker-compose.yml
rm -rf temp

docker rm $(docker ps -a -q)
docker volume prune -f

docker rmi stephenxjc/taiga-docker-events:v2
docker rmi stephenxjc/taiga-docker-front:v2
docker rmi stephenxjc/taiga-docker-back:v2
docker rmi stephenxjc/taiga-front-dist-gen:v3
docker rmi stephenxjc/taiga-front-dist-gen-release:v3

docker rmi $(docker images | grep "none" | awk '{print $3}') 