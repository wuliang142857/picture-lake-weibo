#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 fileencoding=utf-8 ff=unix ft=python
"""
@author: wuliang142857
@contact: wuliang142857@gmail.com
@date 2019/08/10 23:09
"""

import os
import json
import urllib.parse
import urllib.request

class Config:
    def __init__(self):
        self.username = None
        self.password = None
        self.protocol = "https"
        self.hostname = "tva1.sinaimg.cn"
        self.size = "large"
        # 代理服務器地址，可選
        self.proxy = None

    def toJSON(self):
        return json.dumps(self.__dict__, ensure_ascii=False, indent=4, sort_keys=True)

    def fromJSON(self, c):
        d = json.loads(c, encoding="utf-8")
        for k in d.keys():
            setattr(self, k, d[k])

class ConfigWrapper:
    def __init__(self,
                 configFile = os.path.join(os.environ["HOME"], ".picture-lake-weibo.json")
                 ):
        self.configFile = configFile
        self.config: Config = Config()
        if os.path.exists(configFile):
            self.config = self.deserialize()
        if self.config.proxy is not None:
            parsed = urllib.parse.urlparse(self.config.proxy)
            proxySupport = urllib.request.ProxyHandler({parsed.scheme: parsed.netloc})
            opener = urllib.request.build_opener(proxySupport)
            urllib.request.install_opener(opener)

    def serialize(self):
        fout = open(self.configFile, "w")
        fout.write(self.config.toJSON())
        fout.close()

    def deserialize(self) -> Config:
        fin = open(self.configFile, "r")
        c = fin.read()
        fin.close()
        config: Config = Config()
        config.fromJSON(c)
        return config
