#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import json
import re
import getopt
import urllib2
import time


# The fucking SINA, need add "Referer":"http://finance.sina.com.cn", otherwise will occur error!
common_sn_fetch = {
	'Connection': 'keep-alive',
	'Cache-Control': 'max-age=0',
	'Referer':'http://finance.sina.com.cn',
	'Upgrade-Insecure-Requests': 1,
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'Accept-Language': 'zh-CN,zh;q=0.9'
}

#对数据解析
def get_sina_lastday():
	#return '2022-01-21'
	param = 'sh000001'
	stockData = ''
	url = "http://hq.sinajs.cn/?_=0.7577027725009173&list=" + param
	'''
	try:
		stockData = urllib2.urlopen(url).read()
	except:
		print "URL timeout"
		return
	'''
	LOOP_COUNT  = 0
	# https://hq.sinajs.cn/?_=0.7577027725009173&list=sh000001,sz300855
	#print "sina lastDay", url
	while LOOP_COUNT<3:
		try:
			req = urllib2.Request(url, headers=common_sn_fetch)
			stockData = urllib2.urlopen(req, timeout=3).read()
		except Exception as e:
			LOOP_COUNT += 1
			time.sleep(0.5)
			if LOOP_COUNT==2:
				print "Error:", e
		else:
			break
	#print "===",stockData

	prestr = "var hq_str_" + param
	objs = re.match(r'^' + prestr + '=\"(.*)\"', stockData)
	if objs is None:
		print("Not find mathed item")

	obj = objs.group(1).split(',')
	#for i,val in enumerate(obj): print(i, val)

	return obj[30]

def get_realtime_data(st_list):
	param = ",".join(i for i in st_list)
	#print (param)

	url = "http://hq.sinajs.cn/?_=0.7577027725009173&list=" + param
	stockData = None
	LOOP_COUNT=0
	while LOOP_COUNT<3:
		try:
			stockData = urllib2.urlopen(url).read()
		except:
			LOOP_COUNT += 1
			continue
		else:
			break
	if stockData is None:
		print("Get sina data fail", url)
		return
	print stockData[:100]
	return

	
	prestr = "var hq_str_" + param
	objs = re.match(r'^' + prestr + '=\"(.*)\"', stockData)
	if objs is None:
		print("Not find mathed item")

	obj = objs.group(1).split(',')
	#for i,val in enumerate(obj): print(i, val)

	return obj[30]

def get_price_list(code):
	url = "https://vip.stock.finance.sina.com.cn/quotes_service/view/cn_price.php?symbol=" + code
	stockData = None
	LOOP_COUNT=0
	print ("get_prc_lst=", url)
	while LOOP_COUNT<3:
		try:
			stockData = urllib2.urlopen(url).read()
		except:
			LOOP_COUNT += 1
			continue
		else:
			break
	if stockData is None:
		print("Get sina data fail", url)
		return
	print stockData[:100]
	return

	

if __name__ == "__main__":
	pass
