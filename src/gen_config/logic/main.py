# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2019/4/25 11:22

# desc: 主函数入口

import os
import sys
import yaml
import logging

import common.util as util
from common.my_exception import MyException
import common.git_util as git_util


# submodule checkout version
def SubmoduleCheckout():
    dictSubmoduleToVersion = {
        "../../submodule/taiga-front": "master",
        "../../submodule/taiga-front-dist": "4.2.5-stable",
        "../../submodule/taiga-events": "master",
        "../../submodule/taiga-back": "master",
    }
    for szSubmodule, szVersion in dictSubmoduleToVersion.items():
        logging.getLogger("myLog").debug("git checkout version:%s,%s", szSubmodule, szVersion)
        git_util.checkout(szSubmodule, szVersion)

# 转换所有的配置文件，多层key合并为一个key，并用'_'连接
# 比如 a["BOY"]["NAME"]="xjc" ==> a["BOY_NAME"]="xjc"
def LoadConfig(szFilePath):
    logging.getLogger("myLog").debug("yaml file path:" + szFilePath)

    with open(szFilePath, 'r') as fp:
        dictConfig = yaml.load(fp)
        if dictConfig is None:
            return {}
        logging.getLogger("myLog").debug("file dictConfig:%s", str(dictConfig))

        def RecursiveSetDict(dictConfigTemp, szPrefix, dictOutputConfigTemp):
            for szKey, szValue in dictConfigTemp.items():
                if isinstance(szValue , dict):
                    RecursiveSetDict(szValue, szPrefix + szKey + "_", dictOutputConfigTemp)
                else:
                    dictOutputConfigTemp[szPrefix + szKey] = szValue

        dictOutputConfig = {}

        RecursiveSetDict(dictConfig, "", dictOutputConfig)

        dictOutputConfig["PROJECT_BASE_IN_HOST"] = os.path.abspath(dictOutputConfig["PROJECT_BASE_IN_HOST"])

        return dictOutputConfig

def RenderConfig(dictConfig, bRelease):
    # render file to target
    dictFileMap = {
        # backend
        "../../submodule/taiga-back/requirements.txt": "../../temp/backend/requirements.txt",
        "logic/template/backend/Dockerfile": "../../temp/backend/Dockerfile",
        "logic/template/backend/scripts/checkdb.py": "../../temp/backend/scripts/checkdb.py",
        "logic/template/backend/scripts/entrypoint.sh": "../../temp/backend/scripts/entrypoint.sh",
        "logic/template/backend/local.py": "../../submodule/taiga-back/settings/local.py",
        "logic/template/backend/celery_local.py": "../../submodule/taiga-back/settings/celery_local.py",

        # events
        "logic/template/events/Dockerfile": "../../temp/events/Dockerfile",
        "../../submodule/taiga-events/package.json": "../../temp/events/package.json",
        "logic/template/events/config.json": "../../submodule/taiga-events/config.json",

        # frontend
        "logic/template/frontend/Dockerfile": "../../temp/frontend/Dockerfile",
        "logic/template/frontend/nginx/default.conf": "../../temp/frontend/nginx/default.conf",
        "logic/template/frontend/conf.json": "../../submodule/taiga-front-dist/dist/conf.json",
        "logic/template/frontend/conf.json": "../../submodule/taiga-front/dist/conf.json",
        ## gulp deploy
        "logic/template/frontend/gulp-deploy/Dockerfile": "../../temp/frontend/gulp-deploy/Dockerfile",
        "../../submodule/taiga-front/package.json": "../../temp/frontend/gulp-deploy/package.json",
        "logic/template/frontend/gulp-deploy/make-gulp-deploy-image.sh": "../../tools/make-gulp-deploy-image.sh",
        "logic/template/frontend/gulp-deploy/gulp-deploy.sh": "../../tools/gulp-deploy.sh",
        "logic/template/frontend/gulp-default/gulp-default.sh": "../../tools/gulp-default.sh",
        ## gulp deploy release
        "logic/template/frontend/gulp-deploy-release/Dockerfile": "../../temp/frontend/gulp-deploy-release/Dockerfile",
        "../../submodule/taiga-front/package.json": "../../temp/frontend/gulp-deploy-release/package.json",
        "logic/template/frontend/gulp-deploy-release/make-gulp-deploy-image-release.sh": "../../tools/make-gulp-deploy-image-release.sh",
        "logic/template/frontend/gulp-deploy-release/gulp-deploy-release.sh": "../../tools/gulp-deploy-release.sh",
    }

    if bRelease:
        dictFileMap["logic/template/docker-compose.yml-release"] = "../../docker-compose.yml"
    else:
        dictFileMap["logic/template/docker-compose.yml"] = "../../docker-compose.yml"

    for szKey, szValue in dictFileMap.items():
        logging.getLogger("myLog").debug("render config:%s, %s", szKey, szValue)
        util.RenderConfig(szKey, szValue, dictConfig)
    pass

def Main(args):
    logging.getLogger("myLog").debug("main start")

    # 加载配置表
    import logic.my_config_loader as my_config_loader
    szConfFullPath = my_config_loader.MyConfigLoader.CheckConf(args)
    configLoader = my_config_loader.MyConfigLoader(szConfFullPath)
    configLoader.ParseConf()

    # checkout version
    SubmoduleCheckout()

    # load config
    dictConfig = LoadConfig(configLoader.SetupConfigPath)
    if dictConfig is None:
        raise MyException("Load yaml file failed:" + configLoader.SetupConfigPath)
    logging.getLogger("myLog").debug("dictConfig" + str(dictConfig))

    # render config
    RenderConfig(dictConfig, configLoader.IsRelease)


    logging.getLogger("myLog").debug("finished")

