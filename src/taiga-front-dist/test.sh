#!/bin/bash
# docker run -it --volume /Users/stephenxjc/project/xiewendan/taiga-docker:/taiga-docker ubuntu /bin/bash
docker run -it -p 9001:9001 --volume /Users/stephenxjc/project/xiewendan/taiga-docker:/taiga-docker taiga-front-dist-tools:v1 /bin/bash
# docker run -it --volume /Users/stephenxjc/project/xiewendan/taiga-docker:/taiga-docker -w /taiga-docker/submodule/taiga-front/dist taiga-front-dist-tools:v1 gulp


