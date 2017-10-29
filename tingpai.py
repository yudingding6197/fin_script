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
from internal.ts_common import *

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

#ͨ��class(.) ���� id(#) ����,��'.' or '#'
#print soup.select('.sister') 
#print soup.select('#link1')

print soup.select("head title")
print soup.select("head > title")
#���Բ���
print soup.select('a[href="http://example.com/elsie"]')
print soup.select('p a[href="http://example.com/elsie"]')
'''
prepath = "../Data/"
filetxt = prepath + 'tingpai.txt'
ball = 0
headlist = ['600','601','603','000','002','300']

pindex = len(sys.argv)
today = datetime.date.today()
curdate = ''
if (pindex == 1):
	curdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)
	edate = datetime.datetime.strptime(curdate, '%Y-%m-%d').date()
	#����ǵ��յ�����ͨ��history����Ŀǰ���ܵõ���������ʱ�õ�ǰһ�������
	#��������ͨ��getToday��ȡ
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
#�����ҵ��˽ڵ�
sritem = soup.find(id='suspensionAndResumption1')
if sritem is None:
	print "Not find node suspensionAndResumption1"
	exit(0)

clmitems = sritem.find_all(class_='column2')
if clmitems is None:
	nodata = u'û������'
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
		#child['class'],���û��'class'���Ծͻ����
		clslist = child.get('class')
		if clslist is None:
			continue

		clsattr = ''.join(clslist)
		if clsattr=='column2-right':
			obj = child.find(class_='column2-left')
			value = obj.string
			if value==u'����ͣ��':
				bmatch=1
			break
	if bmatch==1:
		break

if bmatch==0:
	print curdate, 'No data'
	exit(0)

#�� column2 �µĽڵ����
for child in clmitem.children:
	#�Ƽ�ʹ��isinstance�� ���� type
	#if type(child)==bs4.element.NavigableString:
	#	continue
	#if type(child)!=bs4.element.Tag:
	#	continue

	#���˷�Tag�ڵ�
	if isinstance(child, bs4.element.Tag) is False:
		continue
	#child['class'],���û��'class'���Ծͻ����
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

tf_fl.close()
