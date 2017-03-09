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
import pandas as pd
#import matplotlib.pyplot as plt

#reload(sys)
#sys.setdefaultencoding('gbk')

yzzt_list = ['000520','300613','300608','300553','603615']

day_info_df = ts.get_k_data('000520')
print day_info_df.head(3)


excecount = 0
stdf = None
while excecount<5:
	try:
		stdf = ts.get_realtime_quotes(yzzt_list)
	except:
		print "Get except:"
		time.sleep(0.5)
		excecount += 1
		stdf = None
	else:
		break
if stdf is None:
	print "Get list fail at:", yzzt_list
	exit(0)
print stdf.head(3)

'''
a = pd.Series([11,34,54,89,39,20,25])
b = pd.Series(['aa','cc','asd','ew','asd','ew','ce',])
#df = pd.DataFrame([a,b])
df = pd.DataFrame({'code':a, 'name':b})

df1 = df[df.code>40]['name']
#print a
#print type(a)
print type(df1)
print df1
for i in df1:
	print i

df=ts.get_today_all()
print ''
df.to_excel('atemp_today1.xlsx');


#for index,row in df.iterrows():
#	print type(row['open'])
#print df

sr = df[df.changepercent>11]['code']
print type(sr)
print sr

#for i in sr.index:
print sr['code']
#lst = list(sr)
#print lst
#df.to_excel('atemp_today1.xlsx');
'''

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

