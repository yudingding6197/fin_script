#!/usr/bin/env python
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
data_path = "debug/_self_define.txt"
stockCode = []

today = datetime.date.today()
curdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)
#print curdate

#˵��show_flag
#0�������ÿһֻ����ͨ�̣�������㻻����
#1�����ÿһֻ����ͨ�̣����Ҽ��㻻����
#2����ʾÿһֻ���µ����ţ����������ȫ����ʾ������û��ֻ��ʾһ��news
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

show_idx = ['000001', '399001', '399005', '399006']
idx_df=ts.get_index()
show_index_info(idx_df, show_idx)

codeArray = ['399678']
show_extra_index(codeArray)

st_bas = None
if show_flag==2:
	st_bas=ts.get_stock_basics()
list_realtime_info(st_bas, stockCode)
