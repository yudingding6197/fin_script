# -*- coding:gbk -*-
import sys
import re
import os
import string
import datetime
import urllib
import urllib2
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook
import internal.common

#将TDX的数据转换为excel

addcsv = 0
prepath = "..\\Data\\TDX\\"
convAll = 0
pindex = len(sys.argv)
if pindex<2:
	sys.stderr.write("转换通达信的数据到Excel中, 如果没有指定日期，转换所有文件\n")
	sys.stderr.write("Usage: " +os.path.basename(sys.argv[0])+ " 代码 [日期]\n")
	sys.stderr.write("日期:d=YYYY-MM-DD | d=MM-DD | d=MM-DD~MM-DD | d=YYYY-MM-DD~YYYY-MM-DD] \n")
	sys.stderr.write("     前两种是单独日期, 后两种是范围\n")
	exit(1);

code = sys.argv[1]
if (len(code) != 6):
	sys.stderr.write("Len should be 6\n")
	exit(1);
	
if pindex==2:
	convAll = 1

qdate = ""
convType = 0
if (pindex==3):
	today = datetime.date.today()
	defdate = sys.argv[2]
	dateObj = defdate.split('~')
	dtLen = len(dateObj)
	print "dlen=%d" %(dtLen)
	if (len(dateObj)==1):
		convType = 0
		qdate = dateObj[0]
		dateObj = re.match(r'^(\d{4})-(\d+)-(\d+)', qdate)
		if (dateObj is None):
			dateObj = re.match(r'^(\d+)-(\d+)', qdate)
			if (dateObj is None):
				print "非法日期格式：" +qdate+ ",期望格式:YYYY-MM-DD or MM-DD"
				exit(1);
			else:
				year = today.year
				month = int(dateObj.group(1))
				day = int(dateObj.group(2))
		else:
			year = int(dateObj.group(1))
			month = int(dateObj.group(2))
			day = int(dateObj.group(3))
		qdate = '%04d%02d%02d' %(year, month, day)
		print qdate
	else:
		convType = 1
		sdate = dateObj[0]
		edate = dateObj[1]
		dateObj = re.match(r'^(\d{4})-(\d+)-(\d+)', sdate)
		if (dateObj is None):
			dateObj = re.match(r'^(\d+)-(\d+)', sdate)
			if (dateObj is None):
				print "非法日期格式：" +sdate+ ",期望格式:YYYY-MM-DD or MM-DD"
				exit(1);
			else:
				year = today.year
				month = int(dateObj.group(1))
				day = int(dateObj.group(2))
		else:
			year = int(dateObj.group(1))
			month = int(dateObj.group(2))
			day = int(dateObj.group(3))
		sdate = '%04d%02d%02d' %(year, month, day)
		
		dateObj = re.match(r'^(\d{4})-(\d+)-(\d+)', edate)
		if (dateObj is None):
			dateObj = re.match(r'^(\d+)-(\d+)', edate)
			if (dateObj is None):
				print "非法日期格式：" +edate+ ",期望格式:YYYY-MM-DD or MM-DD"
				exit(1);
			else:
				year = today.year
				month = int(dateObj.group(1))
				day = int(dateObj.group(2))
		else:
			year = int(dateObj.group(1))
			month = int(dateObj.group(2))
			day = int(dateObj.group(3))
		edate = '%04d%02d%02d' %(year, month, day)
		
		print sdate
		print edate

path = prepath + code
print path
if convAll==0:
	if convType==0:
		filename = qdate + "-" + code + ".txt"
	elif convType==1:
		pass
elif convAll==1:
	for (dirpath, dirnames, filenames) in os.walk(path):  
		print('dirpath = ' + dirpath)
		i = 0
		for filename in filenames:
			extname = filename.split('.')[-1]
			if cmp(extname,"txt")!=0:
				continue

			print filename
			#parseFile(path, filename)
			i += 1
			
		#仅仅得到父文件夹的文件，忽略子文件夹下文件
		break;


#internal.common.handle_data(addcsv, prepath, 0, url, code, qdate, sarr)


