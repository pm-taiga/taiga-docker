FROM ubuntu:18.04

COPY package.json /taiga-docker/submodule/taiga-front/package.json

# Replace shell with bash so we can source files
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN apt update
RUN apt install -y git curl vim
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash

WORKDIR /taiga-docker/submodule/taiga-front
RUN source ~/.nvm/nvm.sh;\
    nvm install v7.7.2; \
    npm install -g gulp; \
    npm install;

CMD ['/bin/bash']