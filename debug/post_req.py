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


urlall = "http://www.cninfo.com.cn/cninfo-new/memo-2"
#urlall = "http://www.cninfo.com.cn/information/companyinfo_n.html?fulltext?szmb000615"
#urlall = "http://www.cninfo.com.cn/cninfo-new/disclosure/szse/fulltext"
filename = 'debug/_html.txt'

dict = {'stock':'300418','searchkey':'','category':'','pageNum':'1','pageSize':'15','column':'szse_gem','tabName':'latest','sortName':'','sortType':'','limit':'','seDate':''}
data = urllib.urlencode(dict)
#print dict
#dict['stock']='600060'
#print dict['aaa']
#for k,v in dict.items():
#	print k,v
#exit(0)

tf_fl = open(filename, 'w+')
try:
	#req : urllib2.Request(urlall)
	res_data = urllib2.urlopen(urlall, data)
except:
	print "Error fupai urlopen"
	#LOOP_COUNT = LOOP_COUNT+1
if res_data is None:
	print "Open URL fail"
	exit(0)

content = res_data.read()
tf_fl.write(content)

s = json.loads(content)
clsAnno = s['classifiedAnnouncements']
annoLen = len(clsAnno)
if annoLen==0:
	print "classifiedAnnouncements No Data"
	exit(0)
items = clsAnno[0]
count = 0
for item in items:
	#print type(item)
	#print item
	for k,v in item.items():
		print k,v
	break
#print clsAnno[0][0]
#print type(clsAnno[0][0])

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

