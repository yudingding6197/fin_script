# -*- coding:gbk -*-
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook
import sys
import re
import os
import time
import datetime

class fitItem:
	volumn = 0
	buyvol = 0
	buyct = 0
	buyavg = 0
	sellvol = 0
	sellct = 0
	sellavg = 0
	def __init__(self,vol):
		self.volumn = vol


s0 = '2012-12-13'
s1 = '	<tr ><th>11:29:48</th><td>14.57</td><td>-3.06%</td><td>+0.01</td><td>16</td><td>23,312</td><th><h1>中性盘</h1></th></tr>'
s2 = '<iframe id="list_frame" name="list_frame" src="http://market.finance.sina.com.cn/transHis.php?date=2015-07-10&symbol=sz300001" frameborder="0" style="width:948px; margin:0 -10px; overflow:hidden;" scrolling="no"></iframe>'
s3 = '<tr ><th>11:29:21</th><td>14.56</td><td>-3.13%</td><td>-0.02</td><td>10</td><td>14,560</td><th><h6>卖盘</h6></th></tr>'
s4 = '	<tr class="huge"><th>15:00:35</th><td>14.37</td><td>-4.39%</td><td>--</td><td>2437</td><td>3,503,320</td><th><h1>中性盘</h1></th></tr>'
s5 = '<tr class="medium"><th>14:56:59</th><td>14.37</td><td>-4.39%</td><td>--</td><td>136</td><td>195,432</td><th><h6>卖盘</h6></th></tr>'
s6 = '<tr ><th>14:56:48</th><td>19.66</td><td>0.01</td><td>64</td><td>125,824</td><th><h5>买盘</h5></th></tr>'
s7 = "<td width='103' align='left'><a title='重大事项' target='_blank' href='/information/companyinfo.html' onClick=\"setLmCode2('fulltext?','000016','012002');\">"
s8 = '<tr ><th>11:29:21</th><td>14.56</td><td>-0.02</td><td>10</td><td>14,560</td><th><h6>卖盘</h6></th></tr>'

#key = re.match(r'\D+(\d{2}:\d{2}:\d{2})\D+(\d+.\d{1,2})</td><td>(--|\+\d+.\d+|-\d+.\d+)\D+(\d+)</td><td>([\d,]+)</td><th><h\d+>(卖盘|买盘|中性盘)\D', s6)
key = re.match(r'.*name=\"list_frame\" src=\"(.*)\" frameborder', s2)
if (key):
	print key.groups()
	print key.group(1)
else:
	print "NONE"


