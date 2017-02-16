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

df = ts.get_today_all()
if df is None:
	print "Fail to get data!"
	exit(1)

print ""
df.to_csv(prepath+"info.txt")
df.to_excel(prepath+"today.xlsx")
'''
for index,row in df.iterrows():
	if index<40:
		print index, row['code'], row['name'], row['changepercent']
	if index>2800:
		print index, row['code'], row['name'], row['changepercent']
'''

