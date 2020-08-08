#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import json
import re
import getopt
import urllib2
import time

#对数据解析
def get_sina_lastday():
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
	while LOOP_COUNT<3:
		try:
			#print "create url"
			urlObj = urllib2.urlopen(url,timeout=3)
			#print "urlObj", urlObj
			stockData = urlObj.read()
			#print "Read Data Fin"

			#stockData = urllib2.urlopen(url,timeout=3).read()
		except:
			LOOP_COUNT += 1
			time.sleep(0.5)
		else:
			break

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
