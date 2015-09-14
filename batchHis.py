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
from internal.common import handle_his_data

#url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php?symbol=sz300001&date=2015-09-10&page=48"
#url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php?symbol=sz300001&date=2015-09-10&page=1"
#成交时间	成交价	涨跌幅	价格变动	成交量(手)		成交额(元)	性质
#	<tr ><th>11:29:48</th><td>14.57</td><td>-3.06%</td><td>+0.01</td><td>16</td><td>23,312</td><th><h1>中性盘</h1></th></tr>
#<tr ><th>11:29:36</th><td>14.56</td><td>-3.13%</td><td>--</td><td>9</td><td>13,104</td><th><h6>卖盘</h6></th></tr>
#<tr ><th>11:29:21</th><td>14.56</td><td>-3.13%</td><td>-0.02</td><td>10</td><td>14,560</td><th><h6>卖盘</h6></th></tr>

#如果需要记录到csv文件中，修改addcsv=1
addcsv = 0
prepath = "..\\Data\\"
url = "http://market.finance.sina.com.cn/transHis.php"

pindex = len(sys.argv)
if pindex<3:
	sys.stderr.write("Usage: " +os.path.basename(sys.argv[0])+ " 代码 时间<YYYY-MM-DD or MM-DD> [arr=[number, number...]]\n")
	exit(1);

code = sys.argv[1]
strdate = sys.argv[2]
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

dObj = strdate.split('~')
if len(dObj)!=2:
	print "非法日期格式：" +strdate+ ",期望格式:(YYYY-MM-DD or MM-DD)~(YYYY-MM-DD or MM-DD)"
	print "如：9-19~9-22 or 2014-8-2~2-14-8-23"
	exit(1)

today = datetime.date.today()
for i in range(0,2):
	qdate = dObj[i]
	dateObj = re.match(r'^(\d{4})-(\d+)-(\d+)', qdate)
	if (dateObj is None):
		dateObj = re.match(r'^(\d+)-(\d+)', qdate)
		if (dateObj is None):
			print "非法日期格式：" +qdate+ ",期望格式:YYYY-MM-DD or MM-DD"
			exit(1);
		else:
			year = str(today.year)
			month = dateObj.group(1)
			day = dateObj.group(2)
	else:
		year = dateObj.group(1)
		month = dateObj.group(2)
		day = dateObj.group(3)

	qdate = year
	if len(month)==1:
		qdate = year+ "-0" +month
	else:
		qdate = year+ "-" +month
	if len(day)==1:
		qdate = qdate+ "-0" +day
	else:
		qdate = qdate+ "-" +day

	if i==0:
		sdate = datetime.datetime.strptime(qdate, '%Y-%m-%d').date()
		curdate = sdate
	elif i==1:
		edate = datetime.datetime.strptime(qdate, '%Y-%m-%d').date()
#print qdate

qarr = ''
if pindex==4:
	qarr = sys.argv[3]
prepath = prepath+ code+ "\\"

delta1=datetime.timedelta(days=1)
delta = edate - curdate
while (delta.days>=0):
	dltoday = curdate - today
	if (dltoday.days>0):
		print "当前日期(" +curdate.strftime("%Y-%m-%d")+ ")超过当天日期了！"
		break
	qdate = curdate.strftime("%Y-%m-%d")
	handle_his_data(addcsv, prepath, url, code, qdate, qarr)
	curdate = curdate + delta1
	delta = edate - curdate
