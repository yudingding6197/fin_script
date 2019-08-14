#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import urllib2
import json
import zlib
import random
from bs4 import BeautifulSoup

def http_req(urlall, send_headers1, data):
	#print (urlall)
	#print (send_headers1)
	filename = 'debug/_html.txt'
	res_data = None
	tf_fl = open(filename, 'w+')
	LOOP_COUNT = 0
	while LOOP_COUNT<3:
		try:
			#方法1
			#res_data = urllib2.urlopen(urlall)

			#方法2
			req = urllib2.Request(urlall,headers=send_headers1)
			res_data = urllib2.urlopen(req, timeout=1)
		except:
			if LOOP_COUNT==2:
				print "Error fupai urlopen"
			LOOP_COUNT = LOOP_COUNT+1
		else:
			break
		
	#print res_data
	if res_data is None:
		print "Open URL fail"
		exit(0)

	content = res_data.read()
	respInfo = res_data.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
		print "Content compressed"
		content = zlib.decompress(content, 16+zlib.MAX_WBITS);
	else:
		print "Content not zip"
	#print content.decode('utf8')

	tf_fl.write(content)

	'''
	line = res_data.readline()
	while line:
		try:
			tf_fl.write(line)
		except:
			#print "?????????????",line.decode('utf8')
			tf_fl.write(line)
		line = res_data.readline()
	'''
	tf_fl.close()

	data = json.loads(content)

def genRand(length):
	r1 = random.random()

	fmt = "%." + str(length) + "f"
	r1 = float(fmt % r1)

	sr1 = repr(r1)
	return sr1

def formatRand(length=16):
	sr1 = genRand(length)
	rlen = len(sr1)
	while rlen<3:
		print("Warning: too short", sr1);
		sr1 = genRand(length)
		rlen = len(sr1)
	rlen -= 2

	if (rlen>length):
		print ("Warning: Great", rlen, sr1)
		sr1 = sr1[0:length+2]
	elif (rlen<length):
		delta = length-rlen
		while delta>0:
			sr1 += random.choice('123456789')
			delta -= 1
		#print ("Less", sr1)
	return sr1

#Main
#for i in range(0,1000):
#	formatRand()

rand = formatRand()
dt = '2019-08-12'
urlall = 'http://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&CATALOGID=1803&TABKEY=tab1&txtQueryDate='+dt+'&random='+rand
send_headers = {
'Host': 'www.szse.cn',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': 1,
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
'DNT': 1,
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9'
}

data = []
http_req(urlall, send_headers, data)
#print(type(data))

#exit(0)
