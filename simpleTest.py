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
keyw = '收盘价|涨跌幅|前收价|开盘价|最高价|最低价|成交量|成交额'
infoRe = re.compile(r'\D+('+keyw+').*>(\+?-?\d+\.\d+)')

s0 = '2012-12-13'
s1 = '	<tr ><th>11:29:48</th><td>14.57</td><td>-3.06%</td><td>+0.01</td><td>16</td><td>23,312</td><th><h1>中性盘</h1></th></tr>'
s2 = '<iframe id="list_frame" name="list_frame" src="http://market.finance.sina.com.cn/transHis.php?date=2015-07-10&symbol=sz300001" frameborder="0" style="width:948px; margin:0 -10px; overflow:hidden;" scrolling="no"></iframe>'
s3 = '<tr ><th>11:29:21</th><td>14.56</td><td>-3.13%</td><td>-0.02</td><td>10</td><td>14,560</td><th><h6>卖盘</h6></th></tr>'
s4 = '	<tr class="huge"><th>15:00:35</th><td>14.37</td><td>-4.39%</td><td>--</td><td>2437</td><td>3,503,320</td><th><h1>中性盘</h1></th></tr>'
s5 = '<tr class="medium"><th>14:56:59</th><td>14.37</td><td>-4.39%</td><td>--</td><td>136</td><td>195,432</td><th><h6>卖盘</h6></th></tr>'
s6 = '<tr ><th>14:56:48</th><td>19.66</td><td>0.01</td><td>64</td><td>125,824</td><th><h5>买盘</h5></th></tr>'
s7 = '<tr><td>收盘价:</td><td><h6><span style="color:#008000">8.47</span></h6></td></tr>'
s8 = '<tr><td>涨跌幅:</td><td><h6><span style="color:#008000">-0.12%</span></h6></td></tr>'

infoObj = infoRe.match(s7)
if infoObj:
	print infoObj.group(1), infoObj.group(2)
infoObj = infoRe.match(s8)
if infoObj:
	print infoObj.group(1), infoObj.group(2)

count = 0
for i in range(1, 10):
	print "i=", i
	if (i==5):
		count += 1
		if (count>3):
			pass
		else:
			i = 4;
	

'''
s1 = '0.000%'
obj = re.match(r'(.*)\%', s1)
print obj
if obj:
	val = obj.group(1)
	print float(val)

if (s0=='2012-12-13'):
	print "==="
else:
	print "!!!!==="
'''

