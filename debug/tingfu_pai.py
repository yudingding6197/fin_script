#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import string
import urllib
import urllib2
import datetime
from bs4 import BeautifulSoup
sys.path.append(".")
sys.path.append("..")
from internal.ts_common import *

pindex = len(sys.argv)
today = datetime.date.today()
curdate = ''
if (pindex == 1):
	curdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)
	edate = datetime.datetime.strptime(curdate, '%Y-%m-%d').date()
	#如果是当日的数据通过history链接目前不能得到，所以暂时得到前一天的数据
	#今日数据通过getToday获取
	#edate = edate - delta1
else:
	curdate = sys.argv[1]
	if curdate=='.':
		curdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)
	else:
		ret,curdate = parseDate(sys.argv[1], today)
		if ret==-1:
			exit(1)
#print curdate

url = "http://www.cninfo.com.cn/cninfo-new/memo-2"
urlall = url + "?queryDate="+curdate

tf_fl = open('debug/_ting_fu_pai.txt', 'w+')
LOOP_COUNT = 0
res_data=None
while LOOP_COUNT<3:
	try:
		#req = urllib2.Request(urlall)
		res_data = urllib2.urlopen(urlall)
	except:
		print "Error fupai urlopen"
		LOOP_COUNT = LOOP_COUNT+1
	else:
		break
if res_data is None:
	exit(0)

line = res_data.readline()
while line:
	try:
		tf_fl.write(line)
	except:
		print "?????????????",line.decode('utf8')
		tf_fl.write(line)
	line = res_data.readline()
tf_fl.close()
