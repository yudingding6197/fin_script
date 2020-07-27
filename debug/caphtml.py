#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import string
import urllib
import urllib2
import datetime


#urlall = "http://www.cninfo.com.cn/cninfo-new/memo-2"
urlall = "http://www.cninfo.com.cn/information/companyinfo_n.html?fulltext?szmb000615"
urlall = "http://www.cninfo.com.cn/cninfo-new/disclosure/szse/showFulltext/000615"
filename = 'debug/_html.txt'

tf_fl = open(filename, 'w+')
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
		#print "?????????????",line.decode('utf8')
		tf_fl.write(line)
	line = res_data.readline()
tf_fl.close()
