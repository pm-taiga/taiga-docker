# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2018/11/25 16:40:28

# desc: 常用函数

import os
import sys
import subprocess
import logging
import shutil
from jinja2 import Template

from common.my_exception import MyException
import common.my_path as my_path


def RunCmd(szCmd, szOutputFile=None, bStdout=False):
    logging.getLogger("myLog").debug("%s,%s,%s", szCmd, szOutputFile, bStdout)

    if szOutputFile is None:
        szOutputFile = open(os.devnull, 'w')
    if bStdout:
        szOutputFile = sys.stdout
    p = subprocess.Popen(
        szCmd, shell=True, stdout=szOutputFile, stderr=szOutputFile)

    return p.wait()


def AssertRunCmd(szCmd, szOutputFile=None):
    logging.getLogger("myLog").debug("%s,%s", szCmd, szOutputFile)

    nRet = RunCmd(szCmd, szOutputFile)
    if nRet != 0:
        raise MyException("Run cmd error=%s" % szCmd)

    return True


def RemoveFileDir(szPath):
    if not os.path.exists(szPath):
        return
    if os.path.isfile(szPath):
        os.remove(szPath)
    else:
        shutil.rmtree(szPath)


def RenderConfig(szTemplatePath, szTargetPath, dictConfig):
    assert os.path.exists(szTemplatePath) and os.path.isfile(szTemplatePath), "template文件不存在" + szTemplatePath

    my_path.CreateFileDir(szTargetPath)

    with open(szTemplatePath, "r") as fpTemplate:
        templateObj = Template(fpTemplate.read())
        szContent = templateObj.render(dictConfig)

        with open(szTargetPath, "w") as fpTarget:
            fpTarget.write(szContent)


