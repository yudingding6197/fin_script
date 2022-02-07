#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import json
import re
import urllib2
import zlib
import datetime
sys.path.append(".")
from internal.format_parse import *

common_qq_fetch = {
	'Host': 'qt.gtimg.cn',
	'Connection': 'keep-alive',
	'Cache-Control': 'max-age=0',
	'Upgrade-Insecure-Requests': 1,
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'zh-CN,zh;q=0.9',
}


#这是得到最新的JYR信息，可能才开始一会儿
def get_qq_lastday():
	param = 'sh000001'
	content = ''
	url = "https://qt.gtimg.cn/q=" + param
	LOOP_COUNT  = 0
	#print "QQ lastDay", url
	while LOOP_COUNT<3:
		try:
			req = urllib2.Request(url, headers=common_qq_fetch)
			res_data = urllib2.urlopen(req, timeout=3)
		except Exception as e:
			LOOP_COUNT += 1
			time.sleep(0.5)
			if LOOP_COUNT==2:
				print "Error:", e
		else:
			break

	content = res_data.read()
	respInfo = res_data.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
		#print "Content compressed"
		content = zlib.decompress(content, 16+zlib.MAX_WBITS);
	idx = content.index('0~~')
	dt_cnt = content[idx+3:idx+3+8]
	
	nowToday = datetime.date.today()
	ret,dt_cnt = parseDate(dt_cnt,nowToday)
	print dt_cnt

#获取多个STK的实时信息
#还有另外一个链接，但是数据信息不大
#https://qt.gtimg.cn/r=0.8409869808238&q=s_sz000559,s_sz000913,s_sz002048
def get_qq_mul_info(codeList):
	scode = ",".join(codeList)
	print scode
	url = "http://qt.gtimg.cn/q=" + scode
	LOOP_COUNT  = 0
	#print "qq lastDay", url
	while LOOP_COUNT<3:
		try:
			req = urllib2.Request(url, headers=common_qq_fetch)
			res_data = urllib2.urlopen(req, timeout=3)
		except Exception as e:
			LOOP_COUNT += 1
			time.sleep(0.5)
			if LOOP_COUNT==2:
				print "Error:", e
		else:
			break

	content = res_data.read()
	respInfo = res_data.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
		#print "Content compressed"
		content = zlib.decompress(content, 16+zlib.MAX_WBITS);
	#print content
	objCont = content.split(';')
	stInfo = objCont[0][12:-2]
	print stInfo
	print '\n'
	stInfo = objCont[1][12:-2]
	print stInfo
	#print cnt


if __name__ == "__main__":
	#get_qq_lastday()
	lst = ['sz000002','sz000001','sz000881','sh601398']
	get_qq_mul_info(lst)
