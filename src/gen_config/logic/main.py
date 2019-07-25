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
        "../../submodule/taiga-front-dist": "master",
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
    dictFileMap = {}
    def AddDictFile(szKey, szValue):
        if szKey not in dictFileMap:
            dictFileMap[szKey] = [szValue]
        else:
            dictFileMap[szKey].append(szValue)
    
    # render file to target
    # backend
    AddDictFile("../../submodule/taiga-back/requirements.txt", "../../temp/backend/requirements.txt")
    AddDictFile("logic/template/backend/Dockerfile", "../../temp/backend/Dockerfile")
    AddDictFile("logic/template/backend/scripts/checkdb.py", "../../temp/backend/scripts/checkdb.py")
    AddDictFile("logic/template/backend/scripts/entrypoint.sh", "../../temp/backend/scripts/entrypoint.sh")
    AddDictFile("logic/template/backend/local.py", "../../submodule/taiga-back/settings/local.py")
    AddDictFile("logic/template/backend/celery_local.py", "../../submodule/taiga-back/settings/celery_local.py")

    # events
    AddDictFile("logic/template/events/Dockerfile", "../../temp/events/Dockerfile")
    AddDictFile("../../submodule/taiga-events/package.json", "../../temp/events/package.json")
    AddDictFile("logic/template/events/config.json", "../../submodule/taiga-events/config.json")

    # frontend
    AddDictFile("logic/template/frontend/Dockerfile", "../../temp/frontend/Dockerfile")
    AddDictFile("logic/template/frontend/nginx/default.conf", "../../temp/frontend/nginx/default.conf")
    AddDictFile("logic/template/frontend/conf.json", "../../submodule/taiga-front/dist/conf.json")
    
    # dist
    AddDictFile("logic/template/frontend/conf.json", "../../submodule/taiga-front-dist/dist/conf.json")

    ## gulp deploy
    AddDictFile("logic/template/frontend/gulp-deploy/Dockerfile", "../../temp/frontend/gulp-deploy/Dockerfile")
    AddDictFile("../../submodule/taiga-front/package.json", "../../temp/frontend/gulp-deploy/package.json")
    AddDictFile("logic/template/frontend/gulp-deploy/make-gulp-deploy-image.sh", "../../tools/make-gulp-deploy-image.sh")
    AddDictFile("logic/template/frontend/gulp-deploy/gulp-deploy.sh", "../../tools/gulp-deploy.sh")
    AddDictFile("logic/template/frontend/gulp-default/gulp-default.sh", "../../tools/gulp-default.sh")

    ## gulp deploy release
    AddDictFile("logic/template/frontend/gulp-deploy-release/Dockerfile", "../../temp/frontend/gulp-deploy-release/Dockerfile")
    AddDictFile("../../submodule/taiga-front-dist/package.json", "../../temp/frontend/gulp-deploy-release/package.json")
    AddDictFile("logic/template/frontend/gulp-deploy-release/make-gulp-deploy-image-release.sh", "../../tools/make-gulp-deploy-image-release.sh")
    AddDictFile("logic/template/frontend/gulp-deploy-release/gulp-deploy-release.sh", "../../tools/gulp-deploy-release.sh")

    if bRelease:
        AddDictFile("logic/template/docker-compose.yml-release", "../../docker-compose.yml")
    else:
        AddDictFile("logic/template/docker-compose.yml", "../../docker-compose.yml")

    for szKey, listValue in dictFileMap.items():
        for szValue in listValue:
            logging.getLogger("myLog").debug("render config:%s, %s", szKey, szValue)
            util.RenderConfig(szKey, szValue, dictConfig)

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

