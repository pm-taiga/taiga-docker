FROM nginx:1.13-alpine

LABEL maintainer="stephenxjc@gmail.com"
LABEL taiga_version="tag:3.3.7-stable"

ENV TAIGA_VERSION 3.3.7-stable

# src
RUN mkdir -p {{TAIGA_HOME}}/taiga-front-dist/dist
WORKDIR {{TAIGA_HOME}}/taiga-front-dist/dist

# nginx
COPY nginx/ /etc/nginx/conf.d/
RUN chown -R nginx {{TAIGA_HOME}}

CMD ["nginx", "-g", "daemon off;"]
