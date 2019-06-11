FROM node:8.9-alpine

LABEL maintainer="stephenxjc@gmail.com"
LABEL taiga_version="branch:master"

ENV TAIGA_VERSION master

# add user
RUN addgroup -S taiga && adduser -S -G taiga taiga

# install
WORKDIR {{TAIGA_HOME}}
COPY package.json {{TAIGA_HOME}}/package.json
RUN npm config set unsafe-perm true
RUN npm install --production && npm install -g coffee-script

# add path
RUN mkdir -p {{TAIGA_HOME}}/taiga-events
RUN chown -R taiga {{TAIGA_HOME}}/taiga-events
WORKDIR {{TAIGA_HOME}}/taiga-events

# user
USER taiga

CMD ["coffee", "index.coffee"]

