# -*- coding:gbk -*-
import sys
import re
import os
import datetime
import urllib
import urllib2
from openpyxl import Workbook
from openpyxl.reader.excel import load_workbook
from internal.common import handle_data

#url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php?symbol=sz300001&date=2015-09-10&page=48"
#url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php?symbol=sz300001&date=2015-09-10&page=1"
#成交时间	成交价	涨跌幅	价格变动	成交量(手)		成交额(元)	性质
#	<tr ><th>11:29:48</th><td>14.57</td><td>-3.06%</td><td>+0.01</td><td>16</td><td>23,312</td><th><h1>中性盘</h1></th></tr>
#<tr ><th>11:29:36</th><td>14.56</td><td>-3.13%</td><td>--</td><td>9</td><td>13,104</td><th><h6>卖盘</h6></th></tr>
#<tr ><th>11:29:21</th><td>14.56</td><td>-3.13%</td><td>-0.02</td><td>10</td><td>14,560</td><th><h6>卖盘</h6></th></tr>

#如果需要记录到csv文件中，修改addcsv=1
addcsv = 0
prepath = "..\\Data\\"
url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php"

pindex = len(sys.argv)
if pindex<3:
	sys.stderr.write("Usage: " +os.path.basename(sys.argv[0])+ " 代码 时间<YYYY-MM-DD or MM-DD> [arr=[number, number...]]\n")
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

qdate = sys.argv[2]
today = datetime.date.today()
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

qdate = '%04d-%02d-%02d' %(year, month, day)
#print qdate

qarr = ''
if pindex==4:
	qarr = sys.argv[3]

edate = datetime.datetime.strptime(qdate, '%Y-%m-%d').date()
delta = edate - today
if (delta.days>=0):
	print "Warning:日期可能不正确，导致数据错误！"

handle_data(addcsv, prepath, 1, url, code, qdate, qarr)


