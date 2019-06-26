FROM ubuntu:18.04

# Replace shell with bash so we can source files
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

COPY package.json /taiga-docker/submodule/taiga-front/package.json
WORKDIR /taiga-docker/submodule/taiga-front

# env
ENV LIBSASS_EXT "no"

# install
RUN apt update 

RUN apt update
RUN apt install -y git curl vim ruby ruby-all-dev

RUN echo "" >> ~/.bashrc
RUN echo "if which ruby >/dev/null && which gem >/dev/null; then \nPATH=\"$(ruby -r rubygems -e 'puts Gem.user_dir')/bin:$PATH\" \nfi" >> ~/.bashrc

RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash

WORKDIR /taiga-docker/submodule/taiga-front

RUN source ~/.bashrc; \ 
    gem install --user-install sass scss_lint;

RUN source ~/.nvm/nvm.sh;\
    npm rebuild node-sass; \
    nvm install v7.7.2; \
    npm install -g gulp; \
    npm rebuild node-sass; \
    npm install;

CMD ["gulp"]