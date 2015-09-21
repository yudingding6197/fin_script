# -*- coding:gbk -*-
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook
import sys
import re
import os
import time
import datetime

from internal.common import *


ascid = 65
chid = chr(65)
s0 = '2012-12-13'
s1 = '	<tr ><th>11:29:48</th><td>14.57</td><td>-3.06%</td><td>+0.01</td><td>16</td><td>23,312</td><th><h1>中性盘</h1></th></tr>'
s2 = '<iframe id="list_frame" name="list_frame" src="http://market.finance.sina.com.cn/transHis.php?date=2015-07-10&symbol=sz300001" frameborder="0" style="width:948px; margin:0 -10px; overflow:hidden;" scrolling="no"></iframe>'
s3 = '<tr ><th>11:29:21</th><td>14.56</td><td>-3.13%</td><td>-0.02</td><td>10</td><td>14,560</td><th><h6>卖盘</h6></th></tr>'
s4 = '	<tr class="huge"><th>15:00:35</th><td>14.37</td><td>-4.39%</td><td>--</td><td>2437</td><td>3,503,320</td><th><h1>中性盘</h1></th></tr>'
s5 = '<tr class="medium"><th>14:56:59</th><td>14.37</td><td>-4.39%</td><td>--</td><td>136</td><td>195,432</td><th><h6>卖盘</h6></th></tr>'
s6 = '<tr ><th>14:56:48</th><td>19.66</td><td>0.01</td><td>64</td><td>125,824</td><th><h5>买盘</h5></th></tr>'
s7 = "<td width='103' align='left'><a title='重大事项' target='_blank' href='/information/companyinfo.html' onClick=\"setLmCode2('fulltext?','000016','012002');\">"
s8 = '<tr ><th>11:29:21</th><td>14.56</td><td>-0.02</td><td>10</td><td>14,560</td><th><h6>卖盘</h6></th></tr>'

time1 = time.time()
#要度量时间的程序
tm1 = datetime.time(23, 46, 10)
tm2 = datetime.time(12, 46, 10)
print tm2, tm1

time2 = time.time()
print time2
print time2 - time1
dt1=datetime.timedelta(hours=18, minutes=46, seconds=10).seconds
dt2=datetime.timedelta(hours=16, minutes=46, seconds=10).seconds
print dt1, dt2
if dt2-dt1>0:
	print ">>"
else:
	print "<<"


val1="10:32:00"
t1 = time.strptime(val1, "%H:%M:%S")
time.mktime(t1)
val2="7:32:00"
t2 = time.strptime(val2, "%H:%M:%S")
print t1, t2

#key = re.match(r'\D+(\d{2}:\d{2}:\d{2})\D+(\d+.\d{1,2})</td><td>(--|\+\d+.\d+|-\d+.\d+)\D+(\d+)</td><td>([\d,]+)</td><th><h\d+>(卖盘|买盘|中性盘)\D', s6)
key = re.match(r'.*name=\"list_frame\" src=\"(.*)\" frameborder', s2)
if (key):
	print key.groups()
#	print key.group(1)
else:
	print "NONE"

val = "19.342"
print float(val)

path = "..\\Data\\"
for (dirpath, dirnames, filenames) in os.walk(path):  
	print('dirpath = ' + dirpath)
	i = len(filenames)
	print len(filenames)
	j = -1
	while i>0:
		i -= 1
		print filenames[j]
		j -= 1

	for filename in filenames:
		i += 1
		if i>2:
			break

		extname = filename.split('.')[-1]
		if cmp(extname,"xlsx")!=0:
			continue

		#parseFile(path, filename)
		
	#仅仅得到父文件夹的文件，忽略子文件夹下文件
	break;

