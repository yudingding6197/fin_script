#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import string
import urllib2
import datetime
import bs4
from bs4 import BeautifulSoup
sys.path.append(".")
sys.path.append("..")
from internal.ts_common import *
from internal.global_var import g_shcd
from internal.global_var import g_szcd

def get_tingfu_item(child, tf_fl):
	info = ''
	ignore = 0
	for liitem in child.find_all('li'):
		lilist = liitem.get('class')
		if lilist is None:
			continue
		liattr = ''.join(lilist)
		value = liitem.string
		if liattr=='ta-1':
			head3 = value[0:3]
			if ball==1 or (head3 in headlist):
				stockCode.append(value)
			elif ball==0 and (head3 not in headlist):
				ignore=1
		elif liattr=='ta-2':
			value = "%-8s"%(value)
		elif liattr=='ta-4':
			if value=='&nbsp':
				value = "%16s"%(" ")
		elif liattr=='ta-5':
			value = "%-8s"%(value)

		#print liitem.string
		info += value
		info += "\t"
	tf_fl.write(info.encode('utf8'))
	tf_fl.write('\n')
	if ignore==0:
		print info


prepath = "../data/"
filetxt = prepath + 'tingfu_pai.txt'
ball = 0
headlist = g_shcd + g_szcd

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

tf_fl = open(filetxt, 'w+')
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

content = res_data.read()
#print content
#content1 = content.decode('utf-8', 'ignore')
#soup = BeautifulSoup(content, 'lxml', from_encoding='utf8')
soup = BeautifulSoup(content, 'lxml')
#print (soup.title.string)
#print soup.head
#print soup.head.contents

stockCode = []
#首先找到此节点
sritem = soup.find(id='suspensionAndResumption1')
if sritem is None:
	print "Not find node suspensionAndResumption1"
	exit(0)

clmitem = sritem.find_all(class_='column2')
if clmitem is None:
	nodata = u'没有数据'
	str = sritem.text
	if str.find(nodata)==-1:
		print curdate, "Not find node column2"
	else:
		print curdate, nodata
	exit(0)

#print clmitem

#将 column2 下的节点遍历
item = 0
for liitem in sritem.find_all(class_='column2'):
	for child in liitem.children:
		if isinstance(child, bs4.element.Tag) is False:
			continue
		clslist = child.get('class')
		if clslist is None:
			continue
		item += 1
		clsattr = ''.join(clslist)
		if clsattr=="column2-right":
			divtext = child.div.get_text()
			print divtext
		elif clsattr=='list-a' or clsattr=='list-b':
			get_tingfu_item(child, tf_fl)
	if item!=0:
		print "\n"
tf_fl.close()
