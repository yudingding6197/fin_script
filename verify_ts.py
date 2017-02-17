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
import internal.ts_common
import tushare as ts

reload(sys)
sys.setdefaultencoding('gbk')

prepath = "..\\Data\\"
pindex = len(sys.argv)

df = ts.get_realtime_quotes('000807')
#c = df[['name','price','bid','ask','volume','amount','time']]
print df
for index,row in df.iterrows():
	stname = row['name']
	open = float(row['open'])
	if open==0.0:
		print 111
	else:
		print 222


'''
for index,row in df.iterrows():
	if index<40:
		print index, row['code'], row['name'], row['changepercent']
	if index>2800:
		print index, row['code'], row['name'], row['changepercent']
'''

