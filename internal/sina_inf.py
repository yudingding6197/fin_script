#!/usr/bin/env python
# -*- coding:gbk -*-
#中文测试
import sys
import os
import re
import datetime
import urllib2
import json
import zlib

urlkline = "http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=%s&scale=%d&ma=%s&datalen=%d"
send_headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'DNT': 1,
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.8'
}

def get_history_trade_info_bysn(len=10, code='sh000001', scale=240, ma='no'):
	urlall = urlkline % (code, scale, ma, len)
	#print(urlall)
	try:
		req = urllib2.Request(urlall,headers=send_headers)
		res_data = urllib2.urlopen(req)
	except:
		print "Error fupai urlopen"
		#LOOP_COUNT = LOOP_COUNT+1
	if res_data is None:
		print "Open URL fail"
		exit(0)

	content = res_data.read()
	respInfo = res_data.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
		#print "Content compressed"
		content = zlib.decompress(content, 16+zlib.MAX_WBITS);
	return content

