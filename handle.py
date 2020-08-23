# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web
import lxml
import time
import os
import reply
import receive
import urllib
import cv2
import numpy as np
import OCRread
import pyodbc
from OCRread import OCRread
from DBmanager import DBmanager


class Handle(object):

    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "mywechat" #你的暗号

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception, Argument:
            return Argument

    def POST(self):
        try:
            webData = web.data()
            print webData
            recMsg = receive.parse_xml(webData)

            toUser = recMsg.FromUserName 
            fromUser = recMsg.ToUserName
            menu = "以下为菜单，输入“菜单”重新获取：\n ⭐ 如果您在寻找同一节课的兄弟姐妹们，请回复”1“\n ⭐ 如果您对Penn State各大社团感兴趣，请回复“2”\n ⭐ 想了解各个专业微信群信息，请回复“3”"
            
            if recMsg.MsgType == 'event':
                if recMsg.EventType == 'subscribe':

       	    		content = "你要关注我，我有什么办法。随便发点什么试试吧" + '\n\n' + menu
		
			replyMsg = reply.TextMsg(toUser, fromUser, content)

            		return replyMsg.send()
		elif recMsg.EventType == 'CLICK':
			if recMsg.Eventkey == 'lookFor':
				content = '感谢使用我们的OCR功能，请以图片格式发送您的课表。\n 👉请尽量截图以保证图片质量 \n 👉目前功能还处于试验阶段，还不能保证100%识别准确率'

            elif  recMsg.MsgType == 'image':
                mediaId = recMsg.MediaId
                picUrl = recMsg.PicUrl
                print('image processing..')
                courselst, ocrOut = self.Match_Class(self.savePic(toUser,picUrl))
                print('insert succeed \n')
                content = '识别出结果：\n'
                couter = 0
                if courselst !=[]:
                    for i in ocrOut:
                        content = content + "<a href = '"+ bytes(courselst[couter]).encode('utf-8') + "'>" + bytes(i[0]) +" "+ bytes(i[1]) + "</a> "
                        # content = content + "<a href = ' http://40.76.91.78/img?id=" + str(courselst[couter])+ " '>" + bytes(i[0]) +" "+ bytes(i[1]) + "</a> "
                        # print(courselst[couter],i[0],i[1])
                        content = content + '\n'
                        couter = couter + 1
                content = content + '请问以上是否为您选的课？'
                print '回复用户：'+ toUser + '\n内容：'+ content
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            else:
                content = recMsg.Content
                if content == '1':
                    content = '感谢使用我们的OCR功能，请以图片格式发送您的课表。\n 👉请尽量截图以保证图片质量 \n 👉目前功能还处于试验阶段，还不能保证100%识别准确率'
                elif content == '2':
                    content = """       社团招新群列表🌈
                        <a href = 'http://mmbiz.qpic.cn/mmbiz_jpg/oVD3HQB6P83VEsMKQmVF1dmgjbBCpKpNyDn8zxWH3uJmDMtjvqPDQTPAx5DmlpiaibjiayOTh3sWsUukK6PIXib4Og/0?wx_fmt=jpeg'>👉PSU CSSA</a>\n
                        <a href = 'http://mmbiz.qpic.cn/mmbiz_jpg/oVD3HQB6P83VEsMKQmVF1dmgjbBCpKpNkEuFYrx3FHmrk2DCTX8MphpJ9woNVa2SHRz7O5nZNeoWtzow4s4Aicw/0?wx_fmt=jpeg'>👉NP摄影社</a>\n
                        <a href = 'http://mmbiz.qpic.cn/mmbiz_jpg/oVD3HQB6P83VEsMKQmVF1dmgjbBCpKpN5vGzibickxMo1A6RmpicLY9PMC43yCSlR2ibC8ALOO4ozjgm0PNxVATr8Q/0?wx_fmt=jpeg'>👉心家团契</a>\n
                        <a href = 'http://mmbiz.qpic.cn/mmbiz_jpg/oVD3HQB6P83VEsMKQmVF1dmgjbBCpKpNzZv8M3VrtUbJWiamdoRhUv5tHhnED0xWAkpgcDk9nIc9FSm7D2kuTnw/0?wx_fmt=jpeg'>👉RoboX</a>\n
                        <a href = 'http://mmbiz.qpic.cn/mmbiz_jpg/oVD3HQB6P83VEsMKQmVF1dmgjbBCpKpNEoezsrhl71TgUeKmhx0My3QYzhyWIwicMLXPOxicE5cWe7Cl0WOvjVog/0?wx_fmt=jpeg'>👉Bounce街舞社</a>\n
                        <a href = 'http://mmbiz.qpic.cn/mmbiz_jpg/oVD3HQB6P83VEsMKQmVF1dmgjbBCpKpNvDjQD2EZDnEXj4Jkp3cMeZs0qTlMBXnkCKY4djrc3ZSn1ZZWxN6aOQ/0?wx_fmt=jpeg'>👉ECO环境保护社</a>\n
                        <a href = 'http://mmbiz.qpic.cn/mmbiz_jpg/oVD3HQB6P83VEsMKQmVF1dmgjbBCpKpNBlR8BMWWKshYibyphHaPE0bpicK2GgiapXbktnIZYU7kcV8fY2q3hqX3g/0?wx_fmt=jpeg'>👉中国象棋社</a>\n
                        <a href = 'http://mmbiz.qpic.cn/mmbiz_jpg/oVD3HQB6P83VEsMKQmVF1dmgjbBCpKpNdfiatdhpe4YYMB1kRMBepy9pCicdlqDlHxy9L7aPIicZ3SrnVzFn3OPUQ/0?wx_fmt=jpeg'>👉ACMA民乐社</a>\n
                        <a href = 'http://mmbiz.qpic.cn/mmbiz_jpg/oVD3HQB6P83VEsMKQmVF1dmgjbBCpKpNlASmE8QHeLIhdNP7Ho2plVs3lAkrKFwoiaicT5gXoyLpeKzBAr8qraOA/0?wx_fmt=jpeg'>👉华人网球社</a>\n
                        <a href = 'http://mmbiz.qpic.cn/mmbiz_jpg/oVD3HQB6P83VEsMKQmVF1dmgjbBCpKpNoXrn1TGtxJeLlCVWiaTibAHOTVgFVrRkjxLFrnkP7diatsZia7XyJBrxxg/0?wx_fmt=jpeg'>👉PSU CUSA</a>\n更多社团介绍 <a href = 'https://zhuanlan.zhihu.com/p/61912110'>👉点击这里</a>  """
                    	

                elif content == '3':
                    content = '感谢您的回复，目前功能还在开发，敬请期待'
                elif content == '菜单':
                    content = menu
                else:
                    course_list, course_with_no_num = self.find_course(recMsg.Content)
                    content = '检测到您发送的消息包含以下课程：\n'
                    for i in course_list:
                    	content += i[0]+ ' ' + i[1]+ '\n'
                    content += '您是否想要寻找以上课程的课友群？'
            replyMsg = reply.TextMsg(toUser, fromUser, content)
            return replyMsg.send()

        except Exception as e:
            print(e)
            return 'success'


    # def Match_Class(self,imgDir):
    #     try:
    #         OCRreader=OCRread()
    #         OCRreader.ReadClass(str(imgDir))
    #         print 'read succeed'
    #         server_name = 'wechatnameserver.database.windows.net'
    #         database = 'MyWeChat'
    #         conn = DBmanager(server_name = server_name, database = database)
    #         print 'connect server'
    #         courselst = conn.insert_student(OCRreader)
    #         print 'insert succeed'
    #         return courselst, OCRreader.classtable
    #     except Exception as e:
    #         print(err)

    def Match_Class(self,imgDir):
        try:
            OCRreader=OCRread()
            OCRreader.ReadClass(str(imgDir))
            print 'read succeed'
            server_name = 'wechatnameserver.database.windows.net'
            database = 'MyWeChat'
            conn = DBmanager(server_name = server_name, database = database)
            print 'connect server'
            OCRreader.classtable = self.checkNum(OCRreader.classtable)
            print(OCRreader.classtable)
            courselst = conn.insert_student(OCRreader)
            print 'insert succeed'
            return courselst, OCRreader.classtable
        except Exception as err:
            print(err)
            


    def savePic(self, userID, picUrl):
        path = '/home/AzureUser/WeChat/userImage'
        try:
            url_response = urllib.urlopen(picUrl)
            img_array = np.array(bytearray(url_response.read()), dtype = np.uint8)
            img = cv2.imdecode (img_array, -1)
            tmp = userID+'.png'
            print '++ Saving the image', tmp
            file_path = os.path.join(path,tmp)
            cv2.imwrite(file_path, img)
            print 'image saved!'
            return file_path
        except Exception as e:
            print(1,e)
        
    def checkNum(self,classArray):
    # '''
    #   OCR classArray is a 2D list, contains 0:className 1:classNum
    # '''

        for row in classArray:
            row[0] = row[0].upper()
            row[1] = row[1].replace('I','1')
            row[1] = row[1].replace('O','0')
        return classArray

    def find_course(self, p):
	with open('CLASSLIST') as f:  # get list of class for reading 
            classlist = f.readlines()
            classlist = [x.strip() for x in classlist]
            classlist = filter(None, classlist)
            # for i in classlist:
            # 	if i =='':

	classFound = []
	class_no_num = []
	for i in classlist:
		n = 0
		while n < len(p):
			if p[n:len(p)].upper().find(i) == -1:
				
				break
			#if not p[n:len(p)].upper().find(i) == -1:
			classNum = ''
			
			n += p[n:len(p)].upper().find(i)
			n = n + len(i)
			
			while n<len(p) and p[n] == ' ':
				n += 1
				
			tmp = n

			while n<len(p) and p[n] in ['0','1','2','3','4','5','6','7','8','9']:
				
				classNum = classNum + p[n]
				n += 1
			if not n == tmp:
				if n<len(p) and p[n].isalpha() and not p[n+1].isalpha():	
					classNum = classNum + p[n].upper()
				#print i,classNum
				classFound.append([i, classNum])
			else:
				class_no_num.append(i)
				print i +': class number not found'
			

	for i in classFound:
		for j in classFound:
			#str = 
			if j[0].find(i[0])!=-1 and len(i[0]) < len(j[0]) and i[1] == j[1]:
				classFound.remove(i)
	print classFound
	return classFound, class_no_num