# taiga-docker
docker for taiga

## install env
* [python3.5](https://www.python.org/downloads/)
* [docker](https://www.runoob.com/docker/docker-architecture.html)
* [docker-compose](https://docs.docker.com/compose/install/)

## download
~~~
git clone --recursive git@github.com:pm-taiga/taiga-docker.git
~~~

## config
* modify config：src/gen_config/conf/setup_config.yml
~~~
PROJECT_BASE_IN_HOST: ../..
TAIGA:
  HOSTNAME: localhost
  SECRET_KEY: fasdfadsg3qret34542fgvfd
  API_URL: /api/v1/ 
  EVENTS_URL: ws://localhost/events
  HOME: /home/taiga
  
URL_SCHEME: http

BACK_END:
  DEBUG: True
  DB_CHECK_LIMIT_RETRIES: 5
  DB_CHECK_SLEEP_INTERVAL: 5
  PUBLIC_REGISTER_ENABLED: True

FRONT_END:
  DEBUG: 'true'
  PUBLIC_REGISTER_ENABLED: 'true'

POST_GRES_SQL:
  NAME: taiga 
  USER: taiga
  PASSWORD: 123
  HOST: postgresql
~~~

* install python lib
~~~
cd src/gen_config/bin
setup.bat
~~~

* update taiga version：src/gen_config/logic/main.py中修改SubmoduleCheckout函数
~~~
def SubmoduleCheckout():
    dictSubmoduleToVersion = {
        "../../submodule/taiga-front-dist": "3.3.7-stable",
        "../../submodule/taiga-events": "master",
        "../../submodule/taiga-back": "3.3.7",
    }
    for szSubmodule, szVersion in dictSubmoduleToVersion.items():
        logging.getLogger("myLog").debug("git checkout version:%s,%s", szSubmodule, szVersion)
        git_util.checkout(szSubmodule, szVersion)
~~~

> dictSubmoduleToVersion：定义了不同模块的路径及对应的分支版本

* run
~~~
src/gen_config/bin/run.bat
~~~

* deploy taiga-front
We need to deploy taiga-front that web browser can understand the words.

~~~
# open images
cd tools
./gulp-deploy.sh

# run deploy
gulp deploy
~~~

## run
~~~
docker-compose up
~~~

## stop
one of way

* ctrl + c
* docker-compose down


## other 
### make taiga-front-dist-gen
#### create dockerfile
~~~
FROM ubuntu:18.04

COPY package.json /taiga-docker/submodule/taiga-front/package.json
~~~

#### 创建一个images
~~~
docker build -t taiga-front-dist-gen:v1 .
~~~

#### run docker images 
~~~
docker run -it taiga-front-dist-gen:v1 /bin/bash
~~~

#### install in images
~~~
apt update
apt install -y git curl vim
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash

source ~/.bashrc

nvm install v7.7.2

npm install -g gulp

cd /taiga-docker/submodule/taiga-front
npm install
~~~

#### commit
* docker ps 查看containerid
* docker commit containerid taiga-front-dist-gen:v3