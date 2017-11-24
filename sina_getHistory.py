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

#�����Ҫ��¼��csv�ļ��У��޸�addcsv=1
addcsv = 0
prepath = "../data/"
url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php"
xmlfile = "internal/array.xml"

pindex = len(sys.argv)
if pindex<3:
	sys.stderr.write("Usage: " +os.path.basename(sys.argv[0])+ " ���� ʱ��<YYYY-MM-DD or MM-DD> [arr=[number, number...]]\n")
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
		print "�Ƿ�����:" +code+ "\n"
		exit(1);
#print code

today = datetime.date.today()
ret,stdate = parseDate(sys.argv[2], today)
if ret==-1:
	exit(1)

sarr = ''
if pindex==4:
	sarr = sys.argv[3]
else:
	sarr = get_data_array(sys.argv[1], xmlfile)

edate = datetime.datetime.strptime(stdate, '%Y-%m-%d').date()
delta = edate - today
if (delta.days>=0):
	print "Warning:���ڿ��ܲ���ȷ���������ݴ���"

handle_data(addcsv, prepath, 1, url, code, stdate, sarr)


