# -*- coding:gbk -*-
import sys
import re
import os
import time
import string
import datetime
import tushare as ts
from internal.ts_common import *


curdate = ''
data_path = "..\\Data\\_self_define.txt"
stockCode = []

today = datetime.date.today()
curdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)
#print curdate

pindex = len(sys.argv)
show_flag = 0
if pindex==2:
	if sys.argv[1]=='1':
		show_flag=1
	elif sys.argv[1]=='2':
		show_flag=2

if os.path.isfile(data_path) is False:
	print "No file:",data_path
	exit(0)

file = open(data_path, 'r')
while 1:
	lines = file.readlines(100000)
	if not lines:
		break
	for line in lines:
		code=line.strip()
		if len(code)!=6:
			continue;
		if code.isdigit() is False:
			continue;
		stockCode.append(code)
		#print code
file.close()

if show_flag==1:
	list_latest_news(stockCode, curdate)
	exit(0)

if show_flag==0:
	list_realtime_info(None, stockCode)
else:
	st_bas=ts.get_stock_basics()
	#print st_bas.ix['603098']['outstanding']
	list_realtime_info(st_bas, stockCode)
