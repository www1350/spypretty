# -*- coding: utf-8 -*-
import ConfigParser
import base64
import json

import re

import binascii
import requests
import rsa as rsa

USER_NAME = ""
PASSWORD = ""
WEBCLIENT = ""


def loadConfig():
    global USER_NAME
    global PASSWORD
    global WEBCLIENT
    config = ConfigParser.ConfigParser()
    config.readfp(open("weiboLogin.ini", "rb"))
    USER_NAME = config.get("global", "username")
    PASSWORD = config.get("global", "passwd")
    WEBCLIENT = config.get("global","webclient")


def encrypt_passwd(password, pubkey, servertime, nonce):
    key = rsa.PublicKey(int(pubkey, 16), int('10001', 16))
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
    passwd = rsa.encrypt(message.encode('utf-8'), key)
    return binascii.b2a_hex(passwd)


def weiboLogin():
    session_requests = requests.session()
    su = base64.b64encode(USER_NAME.encode('utf-8'))
    login_url = "https://login.sina.com.cn/sso/prelogin.php?entry=sso&callback=sinaSSOController.preloginCallBack&su="+ \
          su +"&rsakt=mod&client="+WEBCLIENT+"&_=1491836993433"

    result = session_requests.get(login_url)
    pre_login_str = re.match(r'[^{]+({.+?})', result.content).group(1)
    print pre_login_str
    pre_login = json.loads(pre_login_str)

    data={
        'entry':'weibo',
        'gateway':'1',
        'from':'',
        'savestate':7,
        'useticket':1,
        'pagerefer':'http://login.sina.com.cn/sso/login.php?client='+WEBCLIENT,
        'vsnf':1,
        'su':su,
        'service':'miniblog',
        'servertime':pre_login['servertime'],
        'nonce':pre_login['nonce'],
        'pwencode':'rsa2',
        'rsakv':pre_login['rsakv'],
        'sp':encrypt_passwd(PASSWORD, pre_login['pubkey'],
                             pre_login['servertime'], pre_login['nonce']),
        'sr':1280*800,
        'encoding':'UTF-8',
        'cdult':3,
        'domain':'sina.com.cn',
        'prelt':74,
        'url':"http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
        'returntype':'META'
    }
    result = session_requests.post("https://login.sina.com.cn/sso/login.php?client="+WEBCLIENT+"&_=1491836993588",data=data)
    login_url = re.search('replace\\(\"([^\']+)\"\\)', result.content).group(1)
    result = session_requests.get(login_url)
    login_str = re.search('\((\{.*\})\)', result.content).group(1)
    login_info = json.loads(login_str)
    login_url = login_info["arrURL"][0]
    result = session_requests.get(login_url)
    login_str = re.search('\((\{.*\})\)', result.content).group(1)
    login_info = json.loads(login_str)
    print (u'登陆成功'+str(login_info))
    uniqueId = login_info["userinfo"]["uniqueid"]
    return (session_requests,uniqueId)


def main():
    loadConfig()
    session_requests, uniqueId =weiboLogin()
    print uniqueId
    result = session_requests.get("http://weibo.com/"+uniqueId)
    print result.content


if __name__ == '__main__':
    main()