#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import urllib2
import re
import datetime

url = "http://hq.sinajs.cn/list="

def get_rt_data(code):
	urllink = url + code
	stockData = None
	try:
		#print urllink
		req = urllib2.Request(urllink)
		stockData = urllib2.urlopen(req, timeout=2).read()
	except:
		print "URL timeout"
	else:
		stockObj = stockData.split(',')
	return stockData

#Main 开始
code = 'sz002855'
stockData = get_rt_data(code)
print stockData


