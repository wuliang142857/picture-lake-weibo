#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 fileencoding=utf-8 ff=unix ft=python
"""
@author: wuliang142857
@contact: wuliang142857@gmail.com
@date 2019/08/10 22:34
"""

import urllib
import urllib.request
import urllib.parse
import base64
import rsa
import json
import http.cookiejar
import binascii
import re
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class Weibo:

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def enableCookies(self):
        # 建立一个cookies 容器
        cookie_container = http.cookiejar.CookieJar()
        # 将一个cookies容器和一个HTTP的cookie的处理器绑定
        cookie_support = urllib.request.HTTPCookieProcessor(cookie_container)
        # 创建一个opener,设置一个handler用于处理http的url打开
        opener = urllib.request.build_opener(cookie_support,
                                             urllib.request.HTTPHandler)
        # 安装opener，此后调用urlopen()时会使用安装过的opener对象
        urllib.request.install_opener(opener)

    # 加密用户名
    def getusername(self):
        username_req_qo = urllib.request.quote(self.username)
        username_bsencode = base64.b64encode(
            bytes(username_req_qo, encoding='utf-8'))
        return username_bsencode.decode("utf-8").split("=")[0]

    # 得到servertime,nonce,pubkey,rsakv
    # 输入用户名和密码之后（不登录）会出现一个prologin的预登陆的包
    def getprelogin(self):
        prelogin_url = "https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su={}&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.19)&_=1507974787556".format(
            self.getusername())
        pre = re.compile('sinaSSOController.preloginCallBack(.*)')
        request = urllib.request.Request(prelogin_url)
        response = urllib.request.urlopen(request)
        read_data = response.read().decode("utf-8")
        date = pre.search(read_data).group(1)[1:-1]
        date_json = json.loads(date)
        servertime = str(date_json['servertime'])
        nonce = date_json['nonce']
        pubkey = date_json['pubkey']
        rsakv = date_json['rsakv']
        return servertime, nonce, pubkey, rsakv

    # 加密密码
    def getpassword(self):
        servertime, nonce, pubkey, rsakv = self.getprelogin()
        pw_string = str(servertime) + '\t' + str(nonce) + '\n' + str(
            self.password)
        key = rsa.PublicKey(int(pubkey, 16), 65537)  # 10001 == 65537  转10进制
        pw_encrypt = rsa.encrypt(pw_string.encode('utf-8'), key)
        self.password = ''  # 安全起见~清空密码~
        passwd = binascii.b2a_hex(pw_encrypt)
        return passwd

    # POST参数
    def build_post_data(self):
        servertime, nonce, pubkey, rsakv = self.getprelogin()
        post_data = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'qrcode_flag': 'false',
            'useticket': '1',
            "pagerefer": "http://passport.weibo.com/visitor/visitor?entry=miniblog&a=enter&url=http%3A%2F%2Fweibo.com%2F&domain=.weibo.com&ua=php-sso_sdk_client-0.6.14",
            'vsnf': '1',
            'su': self.getusername(),
            'service': 'miniblog',
            'servertime': servertime,
            'nonce': nonce,
            'pwencode': 'rsa2',
            'rsakv': rsakv,
            'sp': self.getpassword(),
            'sr': '1920 * 1080',
            'ncoding': 'UTF - 8',
            'prelt': '912',
            'url': "http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
            'returntype': 'META'
        }
        data = urllib.parse.urlencode(post_data).encode('utf-8')
        return data

    def login(self):
        url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
        data = self.build_post_data()
        self.enableCookies()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}
        requests1 = urllib.request.Request(url, data=data, headers=headers)
        reqopen1 = urllib.request.urlopen(requests1)
        reqread1 = reqopen1.read().decode("GBK")
        bs = BeautifulSoup(reqread1, 'lxml')
        bfind = bs.find('script')
        for i in bfind:
            p = i.strip().split('"')[1]
        requests2 = urllib.request.Request(p)
        reqopen2 = urllib.request.urlopen(requests2)
        reqread2 = reqopen2.read()
        bss = BeautifulSoup(reqread2, 'lxml')
        bff = bss.find_all('script')[1]
        try:
            p2 = re.compile(r'location.replace(.*?);}')
            p3 = re.compile(r'"userdomain":"(.*?)"')
            for i in bff:
                get_p2 = p2.findall(i)[0][2:-2]
            requests3 = urllib.request.Request(get_p2)
            reqopen3 = urllib.request.urlopen(requests3)
            reqread3 = reqopen3.read().decode('utf-8')
            userdomain = p3.findall(reqread3)
            login_url = 'http://weibo.com/' + userdomain[0]
            requests4 = urllib.request.Request(login_url)
            reqopen4 = urllib.request.urlopen(requests4)
            reqread4 = reqopen4.read().decode('utf-8')
            bs_date = BeautifulSoup(reqread4, 'lxml')
            bfind_nick_uid = bs_date.find_all('script')
            nick_re = re.compile("CONFIG\['nick'\]='.*?';")
            uin_re = re.compile("CONFIG\['uid'\]='.*?';")
            nickName = None
            userId = None
            for i in bfind_nick_uid[2]:
                nickName = nick_re.search(i.strip()).group().split('=')[1][1:-2]
                userId = uin_re.search(i).group().split('=')[1][1:-2]
            return (nickName, userId)
        except IndexError:
            print("Login Error!")

    def uploadPicture(self, picture):
        uploadUrl = "http://picupload.service.weibo.com/interface/pic_upload.php?mime=image%2Fjpeg&data=base64&url=0&markpos=1&logo=&nick=0&marks=1&app=miniblog"
        b = base64.b64encode(open(picture, "rb").read())
        data = urllib.parse.urlencode({'b64_data': b}).encode("utf-8")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        requests2 = urllib.request.Request(uploadUrl, headers=headers)
        reqopen2 = urllib.request.urlopen(requests2, data=data)
        reqread2 = reqopen2.read().decode("GBK")
        result = re.sub(r"<meta.*</script>", "", reqread2, flags=re.S)
        image_result = json.loads(result)
        image_id = image_result.get('data').get('pics').get('pic_1').get('pid')
        return image_id
