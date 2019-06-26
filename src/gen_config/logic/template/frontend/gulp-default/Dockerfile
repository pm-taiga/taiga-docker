FROM ubuntu:18.04

RUN mkdir -p /taiga-docker
WORKDIR /taiga-docker

# env
ENV LIBSASS_EXT "no"

# install
RUN apt update 

RUN apt install -y ruby ruby-all-dev nodejs npm git vim
RUN update-alternatives --install /usr/bin/node nodejs /usr/bin/nodejs 100

RUN npm install -g gulp

RUN echo "" >> ~/.bashrc
RUN echo "if which ruby >/dev/null && which gem >/dev/null; then \nPATH=\"$(ruby -r rubygems -e 'puts Gem.user_dir')/bin:$PATH\" \nfi" >> ~/.bashrc

RUN /bin/bash -c "source ~/.bashrc"
RUN /bin/bash -c "gem install --user-install sass scss_lint"
RUN /bin/bash -c "npm rebuild node-sass"

ARG username
ARG password
RUN git clone https://${username}:${password}@github.com/pm-taiga/taiga-front.git

WORKDIR /taiga-docker/taiga-front
RUN /bin/bash -c "npm install"
WORKDIR /taiga-docker

RUN rm -rf /taiga-docker/taiga-front

CMD ["gulp"]