#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 fileencoding=utf-8 ff=unix ft=python
"""
@author: wuliang142857
@contact: wuliang142857@gmail.com
@date 2019/08/10 22:51
"""

from __future__ import print_function, absolute_import

from argparse import ArgumentParser, RawTextHelpFormatter
import getpass
from glob import glob
import os
import sys

from picture_lake_weibo.Weibo import Weibo
from picture_lake_weibo.ConfigWrapper import Config, ConfigWrapper
from picture_lake_weibo.MarkdownReplacer import MarkdownReplacer

USAGE = '''
picture-lake-weibo: 把微博作爲圖床

%s action

Action:
login  登錄微博
upload <pictures> ... 上傳圖片
''' % (len(sys.argv) >= 2 and sys.argv[1] or "picture-lake-weibo")

def login():
    username = input("用戶名: ")
    password = getpass.getpass("密碼: ")
    weiboClient = Weibo(username, password)
    (nickName, userId) = weiboClient.login()
    if nickName is not None:
        print("登錄成功!")
        configWrapper: ConfigWrapper = ConfigWrapper()
        configWrapper.config.username = username
        configWrapper.config.password = password
        configWrapper.serialize()
    else:
        print("登陸失敗!", file=sys.stderr)

def upload(picturePatterns):
    for picturePattern in picturePatterns:
        for filepath in glob(picturePattern):
            filepath = os.path.realpath(os.path.expanduser(filepath))
            remoteUrl = uploadOne(filepath)
            if remoteUrl is None:
                print("上傳失敗 => %s" % filepath, file=sys.stderr)
            else:
                print("上傳成功 => %s, %s" % (filepath, remoteUrl))

def uploadOne(picture):
    configWrapper: ConfigWrapper = ConfigWrapper()
    if configWrapper.config.username is None or configWrapper.config.password is None:
        print("請先登錄新浪微博", file=sys.stderr)
        return
    weiboClient = Weibo(configWrapper.config.username, configWrapper.config.password)
    if not weiboClient.isLogined:
        weiboClient.login()

    pictureId = weiboClient.uploadPicture(picture)
    if pictureId is None:
        return None
    else:
        remoteUrl = configWrapper.config.protocol + "://" + configWrapper.config.hostname + "/" + configWrapper.config.size + "/" + pictureId
        return remoteUrl

def replace(markdownPatterns):
    markdownReplacer = MarkdownReplacer()

    for markdownPattern in markdownPatterns:
        for filepath in glob(markdownPattern):
            filepath = os.path.realpath(os.path.expanduser(filepath))
            images = markdownReplacer.getImages(filepath)
            if len(images) <= 0:
                continue
            print("Markdown File => %s, images: %s" % (filepath, images))
            cache = {}
            for image in images:
                remoteUrl = uploadOne(image)
                if remoteUrl is None:
                    print("替換失敗 => %s" % filepath, file=sys.stderr)
                    break
                cache[image] = remoteUrl
                print("%s => %s" % (image, remoteUrl))
            fin = open(filepath, "r")
            content = fin.read()
            fin.close()
            for image in cache.keys():
                content = content.replace(image, cache[image])
            fout = open(filepath, "w")
            fout.write(content)
            fout.close()

def main():
    argumentParser = ArgumentParser(
        add_help=False,
        formatter_class=RawTextHelpFormatter,

    )
    argumentParser.add_argument("command",
                                type=str,
                                choices=["login", "upload", "replace"],
                                help="運行命令，目前支持: login upload replace"
                                )
    argumentParser.add_argument("patterns",
                                nargs="*",
                                default=[],
                                help="需要上傳的圖片/需要替換圖片的Markdown文件"
                                )
    args = argumentParser.parse_args()
    if args.command == "login":
        login()
    elif args.command == "upload":
        upload(args.patterns)
    elif args.command == "replace":
        replace(args.patterns)
    else:
        print("未知的參數", file=sys.stderr)

if __name__ == '__main__':
    main()
