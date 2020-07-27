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
	LOOP_COUNT = 0
	while LOOP_COUNT<3:
		try:
			stockData = urllib2.urlopen(url,timeout=3).read()
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
	
def get_163_lastday():
	todayUrl = "http://hq.sinajs.cn/?_=0.7577027725009173&list=sh000001"
	try:
		req = urllib2.Request(todayUrl)
		stockData = urllib2.urlopen(req, timeout=5).read()
	except:
		print "URL timeout"
	else:
		print(stockData)
		stockObj = stockData.split(',')
	return

def get_qq_lastday():
	todayUrl = "http://hq.sinajs.cn/?_=0.7577027725009173&list=sh000001"
	try:
		req = urllib2.Request(todayUrl)
		stockData = urllib2.urlopen(req, timeout=5).read()
	except:
		print "URL timeout"
	else:
		print(stockData)
		stockObj = stockData.split(',')
	return

param_config = {
	"Source":'sina',	#数据来源
	"End":'',	 		#结束时间
	"Type":'',			#获取的板块，总体,Main,ZX,CY
	"Force":0,			#是否强制刷新
}

#Main
#for i in range(0,1000):
#	formatRand()
if __name__ == "__main__":
	optlist, args = getopt.getopt(sys.argv[1:], 's:e:t:f:')
	for option, value in optlist:
		if option in ["-s","--src"]:
			param_config["Source"] = value
		elif option in ["-e","--end"]:
			param_config["End"] = value
		elif option in ["-t","--type"]:
			param_config["Type"] = value
		elif option in ["-f","--force"]:
			param_config["Force"] = int(value)

	value = ''
	if param_config["Source"]=='sina':
		value = get_sina_lastday()
	elif param_config["Source"]=='163':
		value = get_163_lastday()
	elif param_config["Source"]=='qq':
		value = get_qq_lastday()
