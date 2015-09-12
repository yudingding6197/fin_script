# -*- coding:gbk -*-
import sys
import re
import os
import string
import urllib
import urllib2
import datetime
import binascii
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook

prepath = "D:\\stock\\GongSi"
pindex = len(sys.argv)
if (pindex == 1):
	sys.stderr.write("Usage: command 时间<YYYY-MM-DD or MM-DD>\n")
	exit(1);
	
'''
if (len(code) != 6):
	sys.stderr.write("Len should be 6\n")
	exit(1);

head3 = code[0:3]
result = (cmp(head3, "000")==0) or (cmp(head3, "002")==0) or (cmp(head3, "300")==0)
if result is True:
	code = "sz" + code
	print code
else:
	result = (cmp(head3, "600")==0) or (cmp(head3, "601")==0) or (cmp(head3, "603")==0)
	if result is True:
		code = "sh" + code
		print code
	else:
		print "非法代码:" +code+ "\n"
		exit(1);
'''

qdate = sys.argv[1]
#dateObj = re.search(r'^\d{4}-\d+-\d+', qdate)
dateObj = re.match(r'^(\d{4})-(\d+)-(\d+)', qdate)
if (dateObj is None):
	dateObj = re.match(r'^(\d+)-(\d+)', qdate)
	if (dateObj is None):
		print "非法日期格式：" +qdate+ ",期望格式:YYYY-MM-DD or MM-DD"
		exit(1);
	else:
		today = datetime.date.today()
		year = str(today.year)
		month = dateObj.group(1)
		day = dateObj.group(2)
		pass
else:
	year = dateObj.group(1)
	month = dateObj.group(2)
	day = dateObj.group(3)

qdate = year
if len(month)==1:
	qdate = year+ "-0" +month
else:
	qdate = year+ "-" +month
if len(day)==1:
	qdate = qdate+ "-0" +day
else:
	qdate = qdate+ "-" +day
print qdate

url = "http://www.cninfo.com.cn/information/memo/jyts_more.jsp?datePara="

totalline = 0
lasttime = ''
filename = prepath + '\\fupai_' + qdate
filetxt = filename + '.txt'
fl = open(filetxt, 'w')

urlall = url + qdate
req = urllib2.Request(urlall)
res_data = urllib2.urlopen(req)

flag = 0
count = 0
ignore = 0
line = res_data.readline()
checkStr = '复牌日'
while line:
#		print line
	if flag==0:
		index = line.find(checkStr)
		if (index>=0):
			flag = 1
		line = res_data.readline()
		continue

#	print (line)
#	print binascii.b2a_hex(line)
	
	key = re.match(r'.+fulltext.+\'(\d+)\',\'(\d+)\'', line)
	if key:
#		print key.groups()
		code = key.group(1)
		if (len(code) == 6):
			head3 = code[0:3]
			result = (cmp(head3, "000")==0) or (cmp(head3, "002")==0) or (cmp(head3, "300")==0)
			if result is True:
				fl.write(code + ' ')
			else:
				result = (cmp(head3, "600")==0) or (cmp(head3, "601")==0) or (cmp(head3, "603")==0)
				if result is True:
					fl.write(code + ' ')
				else:
					ignore = 1
		else:
			print "Invalid code:" +code
		line = res_data.readline()
		continue
	key = re.match(r'(.+)(</a></td>)', line)
	if key:
#		print key.groups()
		if ignore==0:
			codename = key.group(1)
			fl.write(codename)
			fl.write("\n")
			totalline += 1
		count = 0
		ignore = 0
		line = res_data.readline()
		continue
	count += 1
	if (count>2):
		break;
	line = res_data.readline()

fl.close()
if (totalline==0):
	print "No Matched Record"
	os.remove(filetxt)


