# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 13:37:01 2020

@author: Sjs98
"""

# -*- coding: utf-8 -*-

import web
import os
import hashlib
import time
from lxml import etree

urls = (
	'/(.*)','WeixinInferface'
)

app = web.application(urls,globals())


class WeixinInterface:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root,'templates')
        self.render = web.template.render(self.templates_root)
        
    def GET(self):
        data = web.input()
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr
        token = 'allen'
        
        l = [token, timestamp, nonce]
        l.sort()
        sha1 = haslib.sha1()
        map(sha1.update,l)
        hashcode = sha1.hexdigest()
        
        if hashcode == signature:
            return echostr
        
    def POST(self):
        str_xml = web.data()
        xml = etree.fromstring(str_xml)
        msgType = xml.find('MsgType').text
        fromUser = xml.find('FromUserName').text
        toUser = xml.find('ToUserName').text
        if msgType == 'text':
            content = xml.find('Content').text
            return self.render.reply(fromUser,toUser,int(time.time()),content)


if __name__ == "__main__":
	app.run()