#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import string
import urllib
import urllib2
import datetime
import binascii
import shutil
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook
from bs4 import BeautifulSoup

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
urlall = url

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

content = res_data.read()
#print content
#content1 = content.decode('utf-8', 'ignore')
#soup = BeautifulSoup(content, 'lxml', from_encoding='utf8')
soup = BeautifulSoup(content, 'lxml')
#print (soup.title.string)
#print soup.head
#print soup.head.contents

item = soup.select('div.transaction')
n = 0
while n<len(item):
	#print item[n].text.encode('utf8')
	str = item[n].text
	tf_fl.write( item[n].text.encode('utf8') )
	tf_fl.write( '\n' )

	tfp = u'深沪停复牌'
	if str.find(tfp) == -1:
		n += 1
		continue
	item1 = item[n].div
	print item1
	break
	n += 1


#item = soup.find_all('div', id='suspensionAndResumption1')
#print "suppppppppppppppp1:"
#chd = item[0].children
#for child in  item[0].children:
#	print '==========='
#	print child

n = 0
item = soup.find('div', class_='column2')
#print item
for divitem in item:
	#print item[n].text.encode('utf8')
	#str = item[n].text
	#tf_fl.write( item[n].text.encode('utf8') )
	#tf_fl.write( '\n' )
	if n>0:
		print "BRKKKKK", n
		break

	#item1 = item[n].find('div')
	print "<<<", divitem, ">>>"
	str = divitem.stripped_strings
	print "str:::", str, ":>"
	if str is None or str=='':
		n += 1
		print "CCCCCCCC", n
		continue
	n += 1
	print "ccc",n
	continue
	
	
	tfp = u'今起停牌'
	if str.find(tfp) == 0:
		print 111111
	#print divitem
	#break
	n += 1

'''
flag = 0
count = 0
ignore = 0
line = res_data.readline()
checkStr = '复牌日'
stockCode = []
stockIdx = -1
while line:
	try:
		l = line.decode('utf8')
		print "============",l
		tf_fl.write(line)
		#tf_fl.write(line)
	except:
		print "?????????????",line.decode('utf8')
		#l = line.decode('gbk', 'ignore')
		#tf_fl.write(l)
	#else
	#print line.decode('utf8')
	line = res_data.readline()
	continue
'''


tf_fl.close()
exit(0)