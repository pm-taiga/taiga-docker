# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2019/06/09 21:00:56

# desc: desc


import os
import git as git

def checkout(szDir, szVersion):
    assert(os.path.exists(szDir) and not os.path.isfile(szDir))

    # 情况一，路径不是git路径
    # 情况二，输入的version版本号不存在
    repoObj = git.Repo(szDir)

    repoObj.git.checkout(szVersion)