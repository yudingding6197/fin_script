# -*- coding:gbk -*-
import sys
import re
import os
import string
import datetime
from internal.ts_common import *

curdate = ''
data_path = "..\\Data\\_tmp1.txt"
stockCode = []

today = datetime.date.today()
curdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)
#print curdate

if os.path.isfile(data_path) is False:
	print "No file:",data_path
	exit(0)

file = open(data_path, 'r')
while 1:
	lines = file.readlines(100000)
	if not lines:
		break
	for line in lines:
		code=line.strip()
		if code.isdigit() is False:
			continue;
		if len(code)!=6:
			if len(code)==7:
				code = code[1:7]
			else:
				continue;
		stockCode.append(code)
		#print code
file.close()

if len(stockCode)==0:
	exit(0)

buy1_vol = []
df=ts.get_realtime_quotes(stockCode)
#df=ts.get_realtime_quotes('000520')
#df=ts.get_realtime_quotes('603690')
for index,row in df.iterrows():
	b1_v = int(row['b1_v'])
	buy1_vol.append(b1_v)

for index,row in df.iterrows():
	#if row[0] not in show_idx:
	#	continue
	#if row['a1_v']=='':
	#	print "None"
	#else:
	#	print "a1v=",row['a1_v']
	a1_v = row['a1_v']
	a1_p = float(row['a1_p'])
	b1_v = int(row['b1_v'])
	b1_p = float(row['b1_p'])
	if a1_p==0 and a1_v=='':
		if buy1_vol[index]<b1_v:
			buy1_vol[index] = b1_v
		elif buy1_vol[index]>b1_v:
			delta = buy1_vol[index]-b1_v
			if delta > 10000:
				print "!!!!! ",row[0],b1_v
				buy1_vol[index] = b1_v
		continue
	#print row
	#print row[0],row['b1_v'],row['b1_p'],row['a1_v'],row['a1_p'],row[0]
print buy1_vol