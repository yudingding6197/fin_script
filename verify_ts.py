# -*- coding:gbk -*-
import sys
import re
import os
import time
import string
import datetime
import urllib
import urllib2
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook
import internal.common
import internal.ts_common
import tushare as ts
#import matplotlib.pyplot as plt

reload(sys)
sys.setdefaultencoding('gbk')

prepath = "..\\Data\\"
pindex = len(sys.argv)
yzzt_list = ['603345','603238','000520','300613','300608','300553','603615']


df = ts.get_stock_basics()
df.to_excel('atemp_today1.xlsx');


'''
listidx=0
df=ts.get_realtime_quotes(yzzt_list)
for index,row in df.iterrows():
	#print "For idx=", index
	high = row['high']
	low = row['low']
	#此时不再是YZZT态
	if high!=low:
		print yzzt_list[listidx],row[0], "NOT YZ"
		yzzt_list.pop(listidx)
		#print "Increase=",listidx
		continue
	print yzzt_list[listidx]
	listidx += 1

print "======"
print yzzt_list
	
dt_list=['000520']
stdf = ts.get_realtime_quotes(dt_list)
print stdf[['code','name']]

df = ts.get_today_all()
df1 = df.sort_index(by=['changepercent','code'])
#df1 = df.sort_index(by=['name'])
print df1
df1.to_excel('temp_today1.xlsx');

today_data= ts.get_today_ticks('000520')
today_data = today_data.sort_index(ascending=False)
time_range = list(today_data['time'])
price= today_data['price']
plt.clf()
plt.figure(figsize=(15,10))
plt.plot(time_range, price, label=code)
plt.show()


c = df[['name','changepercent','open','high','mktcap','nmc']]
#print c
for index,row in df.iterrows():
	if index>20:
		break
	stname = row['name']
	open = float(row['open'])
	print row['mktcap'], row['nmc'], float(row['mktcap'])
	#if open==0.0:
	#	print 111
	#else:
	#	print 222


for index,row in df.iterrows():
	if index<40:
		print index, row['code'], row['name'], row['changepercent']
	if index>2800:
		print index, row['code'], row['name'], row['changepercent']
'''

