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
prepath = "../data/"
url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php"
urlToday = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php"
xmlfile = "internal/array.xml"

pindex = len(sys.argv)
if pindex<4:
	sys.stderr.write("Usage: " +os.path.basename(sys.argv[0])+ " 代码 开始时间<YYYYMMDD or MMDD> 结束时间<YYYYMMDD or MMDD> 强制替换<0 or 1> [arr=[number, number...]]\n")
	exit(1);

code = sys.argv[1]
if (len(code) != 6):
	sys.stderr.write("Len should be 6\n")
	exit(1);

ret, code = parseCode(code)
if ret!=0:
	exit(1);
#print code

delta1=datetime.timedelta(days=1)
today = datetime.date.today()
ret,stdate = parseDate(sys.argv[2], today, ai=1)
if ret==-1:
	exit(1)
sdate = datetime.datetime.strptime(stdate, '%Y-%m-%d').date()
curdate = sdate

eddate = sys.argv[3]
if cmp(eddate, '.')==0:
	eddate = '%04d-%02d-%02d' %(today.year, today.month, today.day)
	edate = datetime.datetime.strptime(eddate, '%Y-%m-%d').date()
	#如果是当日的数据通过history链接目前不能得到，所以暂时得到前一天的数据
	#今日数据通过getToday获取
	edate = edate - delta1
else:
	ret,eddate = parseDate(eddate, today)
	if ret==-1:
		exit(1)
	edate = datetime.datetime.strptime(eddate, '%Y-%m-%d').date()
print "Ready fetch", sdate, edate

replace=0
if pindex>=5:
	replace = int(sys.argv[4])

sarr = ''
if pindex==6:
	sarr = sys.argv[5]
else:
	sarr = get_data_array(sys.argv[1], xmlfile)

prepath = prepath+ code+ "/"

init_trade_obj()

delta = edate - curdate
while (delta.days>=0):
	dltoday = curdate - today
	if (dltoday.days>0):
		print "当前日期(" +curdate.strftime("%Y-%m-%d")+ ")超过当天日期了！"
		break
	qdate = curdate.strftime("%Y-%m-%d")
	ts_handle_data(addcsv, prepath, 1, url, code, qdate, replace, sarr)
	curdate = curdate + delta1
	delta = edate - curdate

if cmp(sys.argv[3], '.')==0:
	t = datetime.datetime.now()
	if (t.hour>=15 and t.minute>0):
		qdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)
		ts_handle_data(addcsv, prepath, 2, urlToday, code, qdate, replace, sarr)
		print ""
print "Batch History Done"
