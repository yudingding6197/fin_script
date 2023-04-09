#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import json
import urllib2
import zlib
import time

common_163_fetch = {
	'Host': 'api.money.126.net',
	'Connection': 'keep-alive',
	'Cache-Control': 'max-age=0',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'zh-CN,zh;q=0.9',
}

#这是得到最新的JYR信息，可能才开始一会儿
def get_163_lastday():
	scode = '0000001'
	url = "https://api.money.126.net/data/feed/" + scode
	LOOP_COUNT  = 0
	#print "163 lastDay", url
	while LOOP_COUNT<3:
		try:
			req = urllib2.Request(url, headers=common_163_fetch)
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
	pre = '_ntes_quote_callback'
	cnt = content[len(pre)+1:-2]
	js163 = json.loads(cnt)
	
	exdate = js163[scode]['update'][0:10]
	exdate = exdate.replace("/","-")
	#print exdate
	return exdate

#获取多个STK的实时信息
def get_163_mul_info(codeList):
	scode = ",".join(codeList)
	print scode
	url = "https://api.money.126.net/data/feed/" + scode
	LOOP_COUNT  = 0
	#print "163 lastDay", url
	while LOOP_COUNT<3:
		try:
			req = urllib2.Request(url, headers=common_163_fetch)
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
	pre = '_ntes_quote_callback'
	cnt = content[len(pre)+1:-2]
	js163 = json.loads(cnt)
	#print cnt
	print js163[codeList[0]]
	print js163[codeList[1]]

if __name__ == "__main__":
	#get_163_lastday()
	lst = ['1000002','1000001','1000881','0601398']
	get_163_mul_info(lst)
