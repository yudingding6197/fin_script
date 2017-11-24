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
from internal.common import *
from internal.ts_common import *

prepath = "../data/"
prepath1 = "../data/entry/fupai/"
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

url = "http://www.cninfo.com.cn/information/memo/jyts_more.jsp?datePara="

totalline = 0
lasttime = ''
filename = prepath + 'fupai'
filetxt = filename + '.txt'
fl = open(filetxt, 'w')

urlall = url + curdate

LOOP_COUNT = 0
res_data=None
while LOOP_COUNT<3:
	try:
		req = urllib2.Request(urlall)
		res_data = urllib2.urlopen(req)
	except:
		print "Error fupai urlopen"
		LOOP_COUNT = LOOP_COUNT+1
	else:
		break
if res_data is None:
	exit(0)

flag = 0
count = 0
ignore = 0
line = res_data.readline()
checkStr = '������'
stockCode = []
stockIdx = -1
while line:
#	print line
	if flag==0:
		index = line.find(checkStr)
		if (index>=0):
			flag = 1
		line = res_data.readline()
		continue

	key = re.match(r'.+fulltext.+\'(\d+)\',\'(\d+)\'', line)
	if key:
		#print key.groups()
		#��ȡÿһ�У����ȵõ�ST����
		code = key.group(1)
		if (len(code) == 6):
			head3 = code[0:3]
			result = (cmp(head3, "000")==0) or (cmp(head3, "002")==0) or (cmp(head3, "300")==0)
			if result is True:
				stockCode.append(code)
				stockIdx += 1
				fl.write(code + ' ')
			else:
				result = (cmp(head3, "600")==0) or (cmp(head3, "601")==0) or (cmp(head3, "603")==0)
				if result is True:
					stockCode.append(code)
					stockIdx += 1
					fl.write(code + ' ')
				else:
					ignore = 1
		else:
			print "Invalid code:" +code

		#��������У�������һ��
		line = res_data.readline()
		continue
	key = re.match(r'(.+)(</a></td>)', line)
	if key:
		#print key.groups()
		#�ٶ�ȡ�����Ӧ������
		if ignore==0:
			codename = key.group(1)
			fl.write(codename)
			fl.write("\n")
			print "====",stockCode[stockIdx],codename.decode('gbk')
			#list_stock_news(stockCode[stockIdx], curdate, None)
			totalline += 1
		count = 0
		ignore = 0
		line = res_data.readline()
		continue
	count += 1
	if (count>2):
		break;
	line = res_data.readline()

#�����е����ݻ������
list_stock_rt(stockCode, curdate, fl)

fl.close()
if (totalline==0):
	print "No Matched Record"
	os.remove(filetxt)
else:
	prepath1 = prepath1 + "fupai" + curdate + ".txt"
	shutil.copy(filetxt, prepath1)
