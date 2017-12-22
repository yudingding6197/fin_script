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

#�����Ҫ��¼��csv�ļ��У��޸�addcsv=1
addcsv = 0
prepath = "../data/"
url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php"
xmlfile = "internal/array.xml"

pindex = len(sys.argv)
if pindex<3:
	sys.stderr.write("Usage: " +os.path.basename(sys.argv[0])+ " ���� ʱ��<YYYY-MM-DD or MM-DD> ǿ���滻<0 or 1> [arr=[number, number...]]\n")
	exit(1);

code = sys.argv[1]
if (len(code) != 6):
	sys.stderr.write("Len should be 6\n")
	exit(1);

ret, code = parseCode(code)
if ret!=0:
	exit(1);
#print code

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
	print "Warning:���ڿ��ܲ���ȷ���������ݴ���"

ts_handle_data(addcsv, prepath, 1, url, code, stdate, replace, sarr)
