#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import string
import datetime
import urllib
import urllib2
from openpyxl import Workbook
from openpyxl.reader.excel import load_workbook
import internal.common
import internal.ts_common

addcsv = 0
prepath = "../data/"
xmlfile = "internal/array.xml"
url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php"
pindex = len(sys.argv)
if pindex<2:
	str = " 代码 [arr=[number, number...]]".decode('gbk')
	print ("Usage: " +os.path.basename(sys.argv[0])+ str)
	exit(1);

code = sys.argv[1]
if (len(code) != 6):
	sys.stderr.write("Len should be 6\n")
	exit(1);

ret, code = internal.common.parseCode(code)
if ret!=0:
	exit(1);

today = datetime.date.today()
qdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)

sarr = ''
if pindex==3:
	sarr = sys.argv[2]
	arrObj = sarr.split(',')
	for i in range(0, len(arrObj)):
		val = arrObj[i].isdigit()
		if val is False:
			print "Invalide parameter:" + sarr
			exit(1)
else:
	sarr = internal.ts_common.get_data_array(sys.argv[1], xmlfile)

internal.ts_common.init_trade_obj()
ret = internal.ts_common.ts_handle_data(addcsv, prepath, 0, url, code, qdate, 0, sarr)
if ret==0:
	print "Get %s:%s OK!"%(code, qdate)
