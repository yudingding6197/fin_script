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
from openpyxl.reader.excel  import  load_workbook
import internal.common
import internal.ts_common

addcsv = 0
prepath = "../Data/"
url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php"
pindex = len(sys.argv)
if pindex<2:
	sys.stderr.write("Usage: " +os.path.basename(sys.argv[0])+ " 代码 [arr=[number, number...]]\n")
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

internal.ts_common.init_trade_obj()
ret = internal.ts_common.ts_handle_data(addcsv, prepath, 0, url, code, qdate, sarr)
if ret==0:
	print "Get %s:%s OK!"%(code, qdate)


