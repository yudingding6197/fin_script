#!/usr/bin/env python
# -*- coding:utf8 -*-
import re
import datetime
from internal.ts_common import *
import tushare as ts

#假设使用中文

rtxt = "../data/realtime.txt"
arr = ['YZZT', 'ZT  ', 'ZTHL', 'YZDT', 'DT  ', 'DTFT']

def parse_rtxt(zdarr):
	idx = 0
	rtfl = open(rtxt, 'r')
	lines = rtfl.readline()
	while lines:
		if len(lines)<4:
			lines = rtfl.readline()
			continue
		key=lines[:4]
		if key in arr:
			#print lines
			idx=arr.index(key)
			lines = rtfl.readline()
			continue
		obj = re.match(r'.*(\d+) (\d{6}) (.*)[\t]+', lines)
		if obj is not None:
			l = []
			l.append(obj.group(2))
			l.append(obj.group(3))
			zdarr[idx].append(l)
		lines = rtfl.readline()
	rtfl.close()

def list_stock_news_sum(codeArray, curdate, file):
	codeLen = len(codeArray)
	for j in range(0, codeLen):
		#if file is None:
		#	continue
		df = None
		try:
			df = ts.get_notices(codeArray[j],curdate)
		except:
			pass
		if df is None:
			df = ts.get_notices(codeArray[j])
		for index,row in df.iterrows():
			#file.write("%s,%s"%(row['date'],row['title'].encode('gbk') ))
			#file.write("\r\n")
			pass
		#file.write("\r\n")
	
if __name__ == '__main__':
	zdarr = [[] for x in range(6)]
	parse_rtxt(zdarr)

	today = datetime.date.today()
	curdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)
	for i in range(len(zdarr)):
		if len(zdarr[i])<=0:
			continue
		print arr[i]
		codeArray = []
		for j in range(len(zdarr[i])):
			code = zdarr[i][j][0]
			codeArray.append(code)
			list_stock_news(code, curdate, None)
		#print codeArray
		#list_stock_news_sum	(codeArray, curdate, None )
		print ''
		#for 
	'''
	print (zdarr)
	print '-------'
	print (zdarr[0])
	print '===='
	print (zdarr[1])
	print '===='
	print (zdarr[2])
	#print a[1]
	'''