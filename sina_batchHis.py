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

#url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php?symbol=sz300001&date=2015-09-10&page=48"
#url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php?symbol=sz300001&date=2015-09-10&page=1"
#成交时间	成交价	涨跌幅	价格变动	成交量(手)		成交额(元)	性质
#	<tr ><th>11:29:48</th><td>14.57</td><td>-3.06%</td><td>+0.01</td><td>16</td><td>23,312</td><th><h1>中性盘</h1></th></tr>
#<tr ><th>11:29:36</th><td>14.56</td><td>-3.13%</td><td>--</td><td>9</td><td>13,104</td><th><h6>卖盘</h6></th></tr>
#<tr ><th>11:29:21</th><td>14.56</td><td>-3.13%</td><td>-0.02</td><td>10</td><td>14,560</td><th><h6>卖盘</h6></th></tr>

#如果需要记录到csv文件中，修改addcsv=1
addcsv = 0
prepath = "../Data/"
url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php"
urlToday = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php"

pindex = len(sys.argv)
if pindex<4:
	sys.stderr.write("Usage: " +os.path.basename(sys.argv[0])+ " 代码 开始时间<YYYYMMDD or MMDD> 结束时间<YYYYMMDD or MMDD> [arr=[number, number...]]\n")
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
#print code

delta1=datetime.timedelta(days=1)
today = datetime.date.today()
ret,stdate = parseDate(sys.argv[2], today)
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
#print sdate, edate

qarr = ''
if pindex==5:
	qarr = sys.argv[4]
prepath = prepath+ code+ "/"

delta = edate - curdate
while (delta.days>=0):
	dltoday = curdate - today
	if (dltoday.days>0):
		print "当前日期(" +curdate.strftime("%Y-%m-%d")+ ")超过当天日期了！"
		break
	qdate = curdate.strftime("%Y-%m-%d")
	handle_data(addcsv, prepath, 1, url, code, qdate, qarr)
	curdate = curdate + delta1
	delta = edate - curdate

if cmp(sys.argv[3], '.')==0:
	t = datetime.datetime.now()
	if (t.hour>=15 and t.minute>0):
		qdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)
		handle_data(addcsv, prepath, 2, urlToday, code, qdate, qarr)
