#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import datetime
import urllib
import urllib2
from openpyxl import Workbook
from openpyxl.reader.excel import load_workbook
from internal.common import *
from internal.ts_common import *

#如果需要记录到csv文件中，修改addcsv=1
addcsv = 0
prepath = "../Data/"
url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php"
xmlfile = "internal/array.xml"

pindex = len(sys.argv)
if pindex<3:
	sys.stderr.write("Usage: " +os.path.basename(sys.argv[0])+ " 代码 时间<YYYY-MM-DD or MM-DD> 强制替换<0 or 1> [arr=[number, number...]]\n")
	exit(1);

code = sys.argv[1]
if (len(code) != 6):
	sys.stderr.write("Len should be 6\n")
	exit(1);

head3 = code[0:3]
result = (cmp(head3, "000")==0) or (cmp(head3, "002")==0) or (cmp(head3, "300")==0)
if result is True:
	code = "sz" + code
else:
	result = (cmp(head3, "600")==0) or (cmp(head3, "601")==0) or (cmp(head3, "603")==0)
	if result is True:
		code = "sh" + code
	else:
		print "非法代码:" +code+ "\n"
		exit(1);

today = datetime.date.today()
ret,stdate = parseDate(sys.argv[2], today)
if ret==-1:
	exit(1)

replace=0
if pindex>=4:
	replace = int(sys.argv[3])

sarr = ''
if pindex==5:
	sarr = sys.argv[4]
else:
	sarr = get_data_array(sys.argv[1], xmlfile)

init_trade_obj()

edate = datetime.datetime.strptime(stdate, '%Y-%m-%d').date()
delta = edate - today
if (delta.days>=0):
	print "Warning:日期可能不正确，导致数据错误！"

ts_handle_data(addcsv, prepath, 1, url, code, stdate, replace, sarr)
