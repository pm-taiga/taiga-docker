# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2019/4/25 14:43

# desc: 自己的配置文件加载器

import logging
import main_frame.config_loader as config_loader


class MyConfigLoader(config_loader.ConfigLoader):
    """"""
    
    def __init__(self, szConfFullPath):
        super(MyConfigLoader, self).__init__(szConfFullPath)

        self.m_szTest = None

        self.m_szSetupConfigPath = None

    def ParseConf(self):
        self.m_szSetupConfigPath = self.ParseStr("common", "SetupConfigPath")
        logging.getLogger("myLog").info("SetupConfigPath:" + self.m_szSetupConfigPath)

        return True

    # ********************************************************************************
    # common
    # ********************************************************************************
    @property
    def Test(self):
        return self.m_szTest

    @property
    def SetupConfigPath(self):
        return self.m_szSetupConfigPath

