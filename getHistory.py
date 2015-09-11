# -*- coding:gbk -*-
import sys
import re
import os
import urllib
import urllib2
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook

#url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php?symbol=sz300001&date=2015-09-10&page=48"
#url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php?symbol=sz300001&date=2015-09-10&page=1"
#成交时间	成交价	涨跌幅	价格变动	成交量(手)		成交额(元)	性质
#	<tr ><th>11:29:48</th><td>14.57</td><td>-3.06%</td><td>+0.01</td><td>16</td><td>23,312</td><th><h1>中性盘</h1></th></tr>
#<tr ><th>11:29:36</th><td>14.56</td><td>-3.13%</td><td>--</td><td>9</td><td>13,104</td><th><h6>卖盘</h6></th></tr>
#<tr ><th>11:29:21</th><td>14.56</td><td>-3.13%</td><td>-0.02</td><td>10</td><td>14,560</td><th><h6>卖盘</h6></th></tr>

pindex = len(sys.argv)
if (pindex != 3):
	sys.stderr.write("Usage: command 代码 时间<YYYY-MM-DD>\n")
	exit(1);

code = sys.argv[1]
qdate = sys.argv[2]
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
	
#dateObj = re.search(r'^\d{4}-\d+-\d+', qdate)
dateObj = re.match(r'^(\d{4})-(\d+)-(\d+)', qdate)
if (dateObj is None):
	print "非法日期格式：" +qdate+ ",期望格式:YYYY-MM-DD"
	exit(1);

qdate = dateObj.group(1)
if len(dateObj.group(2))==1:
	qdate = qdate+ "-0" +dateObj.group(2)
else:
	qdate = qdate+ "-" +dateObj.group(2)
if len(dateObj.group(3))==1:
	qdate = qdate+ "-0" +dateObj.group(3)
else:
	qdate = qdate+ "-" +dateObj.group(3)
#print qdate

url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php?symbol=" + code
url = url + "&date=" + qdate

totalline = 0
lasttime = ''
filename = code+ '_' + qdate + '.csv'
fl = open(filename, 'w')
fl.write("成交时间,成交价,涨跌幅,价格变动,成交量,成交额,性质\n")
for i in range(1,1000):
	urlall = url + "&page=" +str(i)
#	print "%d, %s" %(i,urlall)
	
	req = urllib2.Request(urlall)
	res_data = urllib2.urlopen(req)

	flag = 0
	count = 0
	line = res_data.readline()
	checkStr = '成交时间'
	while line:
#		print line
		index = line.find(checkStr)
		if (index<0):
			line = res_data.readline()
			continue

		if flag==0:
			checkStr = '<th>'
			flag = 1
		else:
			key = re.match(r'\D+(\d{2}:\d{2}:\d{2})\D+(\d+.\d{1,2})</td><td>\+?-?(\d+.\d+)\D+(--|\+\d+.\d+|-\d+.\d+)\D+(\d+)</td><td>([\d,]+)</td><th><h\d+>(卖盘|买盘|中性盘)\D', line)
			if (key):
#				print key.groups()
				curtime = key.group(1)
				if re.search(curtime, lasttime):
					pass
				else:
					lasttime = curtime
					amount = key.group(6)
					obj = amount.split(',')
					amount = ''.join(obj)
					strline = curtime +","+ key.group(2) +","+ key.group(3) +","+ key.group(4) +","+ key.group(5) +","+ amount +","+ key.group(7) + "\n"
					fl.write(strline)
					totalline += 1
				count += 1
				pass
			else:
				endObj = re.search(r'</td><td>', qdate)
				if (endObj):
					print "Error line:" + line
				else:
					break;
		line = res_data.readline()

	if (count==0):
		break;

fl.close()
if (totalline==0):
	print "No Record"
	os.remove(filename)

