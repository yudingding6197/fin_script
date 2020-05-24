#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import json
import re
import getopt
import urllib2

#对数据解析
def get_sina_lastday():
	param = 'sh000001'
	stockData = ''
	url = "http://hq.sinajs.cn/?_=0.7577027725009173&list=" + param
	try:
		stockData = urllib2.urlopen(url).read()
	except:
		print "URL timeout"
		return

	prestr = "var hq_str_" + param
	objs = re.match(r'^' + prestr + '=\"(.*)\"', stockData)
	if objs is None:
		print("Not find mathed item")

	obj = objs.group(1).split(',')
	#for i,val in enumerate(obj): print(i, val)

	return obj[30]

if __name__ == "__main__":
	pass
