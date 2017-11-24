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
#�ɽ�ʱ��	�ɽ���	�ǵ���	�۸�䶯	�ɽ���(��)		�ɽ���(Ԫ)	����
#	<tr ><th>11:29:48</th><td>14.57</td><td>-3.06%</td><td>+0.01</td><td>16</td><td>23,312</td><th><h1>������</h1></th></tr>
#<tr ><th>11:29:36</th><td>14.56</td><td>-3.13%</td><td>--</td><td>9</td><td>13,104</td><th><h6>����</h6></th></tr>
#<tr ><th>11:29:21</th><td>14.56</td><td>-3.13%</td><td>-0.02</td><td>10</td><td>14,560</td><th><h6>����</h6></th></tr>

#�����Ҫ��¼��csv�ļ��У��޸�addcsv=1
addcsv = 0
prepath = "../data/"
url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php"
urlToday = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php"
xmlfile = "internal/array.xml"

pindex = len(sys.argv)
if pindex<4:
	sys.stderr.write("Usage: " +os.path.basename(sys.argv[0])+ " ���� ��ʼʱ��<YYYYMMDD or MMDD> ����ʱ��<YYYYMMDD or MMDD> [arr=[number, number...]]\n")
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
	#����ǵ��յ�����ͨ��history����Ŀǰ���ܵõ���������ʱ�õ�ǰһ�������
	#��������ͨ��getToday��ȡ
	edate = edate - delta1
else:
	ret,eddate = parseDate(eddate, today)
	if ret==-1:
		exit(1)
	edate = datetime.datetime.strptime(eddate, '%Y-%m-%d').date()
#print sdate, edate

sarr = ''
if pindex==5:
	sarr = sys.argv[4]
else:
	sarr = get_data_array(sys.argv[1], xmlfile)

prepath = prepath+ code+ "/"

delta = edate - curdate
while (delta.days>=0):
	dltoday = curdate - today
	if (dltoday.days>0):
		print "��ǰ����(" +curdate.strftime("%Y-%m-%d")+ ")�������������ˣ�"
		break
	qdate = curdate.strftime("%Y-%m-%d")
	handle_data(addcsv, prepath, 1, url, code, qdate, sarr)
	curdate = curdate + delta1
	delta = edate - curdate

if cmp(sys.argv[3], '.')==0:
	t = datetime.datetime.now()
	if (t.hour>=15 and t.minute>0):
		qdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)
		handle_data(addcsv, prepath, 2, urlToday, code, qdate, sarr)
