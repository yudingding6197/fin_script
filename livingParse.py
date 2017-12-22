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

#url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php?symbol=sz300001&date=2015-09-10&page=48"
#�ɽ�ʱ��	�ɽ���	�ǵ���	�۸�䶯	�ɽ���(��)		�ɽ���(Ԫ)	����
#	<tr ><th>11:29:48</th><td>14.57</td><td>-3.06%</td><td>+0.01</td><td>16</td><td>23,312</td><th><h1>������</h1></th></tr>
#<tr ><th>11:29:36</th><td>14.56</td><td>-3.13%</td><td>--</td><td>9</td><td>13,104</td><th><h6>����</h6></th></tr>
#<tr ><th>11:29:21</th><td>14.56</td><td>-3.13%</td><td>-0.02</td><td>10</td><td>14,560</td><th><h6>����</h6></th></tr>

addcsv = 0
prepath = "../data/"
url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php"
pindex = len(sys.argv)
if pindex<2:
	sys.stderr.write("Usage: " +os.path.basename(sys.argv[0])+ " ���� [arr=[number, number...]]\n")
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
#print qdate

sarr = '300'
if pindex==3:
	sarr = sys.argv[2]
	arrObj = sarr.split(',')
	for i in range(0, len(arrObj)):
		val = arrObj[i].isdigit()
		if val is False:
			print "Invalide parameter:" + sarr
			exit(1)
	ret = 0
	while ret!=0:
		ret = internal.common.handle_living(addcsv, prepath, 0, url, code, qdate, sarr)
else:
	print "Need third parameter"




