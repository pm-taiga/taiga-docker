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

## run
~~~
docker-compose up
~~~

## stop
one of way

* ctrl + c
* docker-compose down
