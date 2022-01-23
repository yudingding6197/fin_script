#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import string
import urllib2
import datetime
import bs4
import json
from bs4 import BeautifulSoup
from internal.ts_common import *
from internal.global_var import g_shcd
from internal.global_var import g_szcd

'''
html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

#通过class(.) 或者 id(#) 查找,用'.' or '#'
#print soup.select('.sister') 
#print soup.select('#link1')

print soup.select("head title")
print soup.select("head > title")
#属性查找
print soup.select('a[href="http://example.com/elsie"]')
print soup.select('p a[href="http://example.com/elsie"]')
'''

def list_ting_pai_news(stockCode, stockName, curdate, file):
	if len(stockCode)==0:
		return

	#stockCode = ['000526','002398']
	index = 0
	urlall = "http://www.cninfo.com.cn/cninfo-new/disclosure/szse/fulltext"
	dict = {'searchkey':'','category':'','pageNum':'1','pageSize':'15','column':'szse_gem','tabName':'latest','sortName':'','sortType':'','limit':'','seDate':''}
	for stkcode in stockCode:
		dict['stock']=stkcode.encode('ascii')
		name = stockName[index]
		print stkcode, stockName[index]
		str = u'%s	' % (stkcode)
		file.write(str)
		file.write(name.encode('utf8'))
		file.write("\n")
		index += 1

		data = urllib.urlencode(dict)
		LOOP_COUNT = 0
		res_data = None
		while LOOP_COUNT<3:
			try:
				#req : urllib2.Request(urlall)
				res_data = urllib2.urlopen(urlall, data)
			except:
				print "Error",sys._getframe().f_code.co_name
				LOOP_COUNT = LOOP_COUNT+1
			else:
				break
		if res_data is None:
			print stkcode, "Fail to get latest news"
			continue

		content = res_data.read()
		s = json.loads(content)
		clsAnno = s['classifiedAnnouncements']
		annoLen = len(clsAnno)
		if annoLen==0:
			print stkcode, "classifiedAnnouncements No Data"
			break
		#items = clsAnno[0]
		matchdate = curdate
		currentdate = datetime.datetime.strptime(curdate, '%Y-%m-%d').date()
		for items in clsAnno:
			count = 0
			for info in items:
				issuedt = info['adjunctUrl']
				obj = re.match(r'.*/(.*)/.*', issuedt)
				if obj is None:
					continue
				issuedate = datetime.datetime.strptime(obj.group(1), '%Y-%m-%d').date()
				delta = currentdate-issuedate
				if delta.days>0:
					if count==0:
						matchdate = obj.group(1)
				if issuedt.find(matchdate)!=-1:
					str = info['announcementTitle']
					if str.find(u'自查')!=-1 or str.find(u'核查')!=-1:
						prom = "************  "
						print prom, str
						file.write(prom)
						file.write(str.encode('utf8'))
					else:
						print str
						file.write(str.encode('utf8'))
					file.write("\n")
					count += 1
			if count>0:
				break
		print ""
		file.write("\n")
					
		


#main Main
prepath = "../data/"
filetxt = prepath + 'tingpai_detail.txt'
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
		print "Error",sys._getframe().f_code.co_name
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
stockName = []
#首先找到此节点
sritem = soup.find(id='suspensionAndResumption1')
if sritem is None:
	print "Not find node suspensionAndResumption1"
	exit(0)
clmitems = sritem.find_all(class_='column2')
if clmitems is None:
	nodata = u'没有数据'
	str = sritem.text
	if str.find(nodata)==-1:
		print curdate, "Not find node column2"
	else:
		print curdate, nodata
	exit(0)

bmatch = 0
for clmitem in clmitems:
	if clmitem is None:
		continue
	for child in clmitem.children:
		if isinstance(child, bs4.element.Tag) is False:
			continue
		#child['class'],如果没有'class'属性就会出错
		clslist = child.get('class')
		if clslist is None:
			continue

		clsattr = ''.join(clslist)
		if clsattr=='column2-right':
			obj = child.find(class_='column2-left')
			value = obj.string
			if value==u'今起停牌':
				bmatch=1
			break
	if bmatch==1:
		break

if bmatch==0:
	print curdate, 'No data'
	exit(0)

#将 column2 下的节点遍历
for child in clmitem.children:
	#推荐使用isinstance， 代替 type
	#if type(child)==bs4.element.NavigableString:
	#	continue
	#if type(child)!=bs4.element.Tag:
	#	continue

	#过滤非Tag节点
	if isinstance(child, bs4.element.Tag) is False:
		continue
	#child['class'],如果没有'class'属性就会出错
	clslist = child.get('class')
	if clslist is None:
		continue

	clsattr = ''.join(clslist)
	if clsattr=='list-a' or clsattr=='list-b':
		#for lidesc in child.descendants:
		#	print type(lidesc), lidesc
		#print child.descendants, type(child.children)
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
				if ignore==0:
					stockName.append(value)
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

print ""
tf_fl.write("\n====================================================================================\n")
list_ting_pai_news(stockCode, stockName, curdate, tf_fl)
	
tf_fl.close()
