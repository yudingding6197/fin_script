#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import string
import urllib
import urllib2
import datetime
import json
from bs4 import BeautifulSoup


#urlall = "http://quote.eastmoney.com/center/list.html#33"
#urlall = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._A&sty=FCOIATA&sortType=C&sortRule=-1&page=1&pageSize=20&js=var%20quote_123%3d{rank:[(x)],pages:(pc)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.6295543580707108"
#urlall = "http://www.cninfo.com.cn/cninfo-new/disclosure/szse/fulltext"

url = "http://www.cninfo.com.cn/cninfo-new/memo-2"
urlall = url + "?queryDate=2017-09-08"

print urlall

filename = 'debug/_html.txt'

res_data = None
tf_fl = open(filename, 'w+')
try:
	#req : urllib2.Request(urlall)
	res_data = urllib2.urlopen(urlall)
except:
	print "Error fupai urlopen"
	#LOOP_COUNT = LOOP_COUNT+1
if res_data is None:
	print "Open URL fail"
	exit(0)

content = res_data.read()
tf_fl.write(content)


'''
line = res_data.readline()
while line:
	try:
		tf_fl.write(line)
	except:
		#print "?????????????",line.decode('utf8')
		tf_fl.write(line)
	line = res_data.readline()
'''
tf_fl.close()

