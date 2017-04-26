#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import string
import datetime
import urllib
import urllib2
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook
import internal.common
import time

def currentData(url, code):
	urllink = url + code
	buy = []
	buyVol = []
	sell = []
	sellVol = []
	try:
		req = urllib2.Request(urllink)
		stockData = urllib2.urlopen(req, timeout=2).read()
	except:
		loginfo(1)
		print "URL timeout"
	else:
		stockObj = stockData.split('~')
		stockLen = len(stockObj)
		#for i in range(0, stockLen):
		#	print "%02d:	%s" % (i, stockObj[i])
		
		curPrice = stockObj[3]
		highPrice = stockObj[41]
		lowPrice = stockObj[42]
		lastPrice = stockObj[4]
		variation = stockObj[43]
		zhangdiejia = stockObj[31]
		zhangdiefu = stockObj[32]
		volume = stockObj[36]
		amount = stockObj[37]
		
		index = 9
		for i in range(0, 5):
			buy.append(stockObj[index+i*2])
		index = 10
		for i in range(0, 5):
			buyVol.append(stockObj[index+i*2])
		index = 19
		for i in range(0, 5):
			sell.append(stockObj[index+i*2])
		index = 20
		for i in range(0, 5):
			sellVol.append(stockObj[index+i*2])
		print "---------------------"
		print "[%s	%s(%s)]	[%s	%s]" % (curPrice, zhangdiefu, zhangdiejia, highPrice, lowPrice)
		index = 4
		for i in range(0, 5):
			print "%s	%s" %(sell[index], sellVol[index])
			index -= 1
		print "===%s" %(curPrice)
		index = 0
		for i in range(0, 5):
			print "%s	%s" %(buy[index], buyVol[index])
			index += 1
		print "---------------------"
		print "	"

pindex = len(sys.argv)
if pindex<2:
	sys.stderr.write("Usage: " +os.path.basename(sys.argv[0])+ " 代码 \n")
	exit(1);

code = sys.argv[1]
if (len(code) != 6):
	sys.stderr.write("Len should be 6\n")
	exit(1);

head3 = code[0:3]
result = (cmp(head3, "000")==0) or (cmp(head3, "002")==0) or (cmp(head3, "300")==0) or (cmp(head3, "131")==0)
if result is True:
	code = "sz" + code
else:
	result = (cmp(head3, "600")==0) or (cmp(head3, "601")==0) or (cmp(head3, "603")==0) or (cmp(head3, "204")==0)
	if result is True:
		code = "sh" + code
	else:
		print "非法代码:" +code+ "\n"
		exit(1);

today = datetime.date.today()
qdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)

sarr = ''
if pindex==3:
	sarr = sys.argv[2]
	arrObj = sarr.split(',')
	for i in range(0, len(arrObj)):
		val = arrObj[i].isdigit()
		if val is False:
			print "Invalide parameter:" + sarr
			exit(1)

while True:
	url = "http://qt.gtimg.cn/q="
	currentData(url, code)
	#url = "http://hq.sinajs.cn/list="
	#currentSinaData(url, code)
	time.sleep(2)
