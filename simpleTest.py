#!/usr/bin/env python
# -*- coding:gbk -*-
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook
import sys
import re
import os
import time
import datetime
import ctypes
import sqlite3
import tushare as ts
from internal.common import *

def fun1():
	print "we are in %s"%__name__ 

if __name__ == '__main__':

	kdf = ts.get_k_data('300474', ktype='5')
	#print kdf

	#ts.get_today_ticks('300474')
	
	today = datetime.date.today()
	delta1=datetime.timedelta(days=30)
	sdate = today-delta1
	fmt_start = '%d-%02d-%02d' %(sdate.year, sdate.month, sdate.day)
	kdf = ts.get_k_data('000001', index=True, start=fmt_start)
	kdf = kdf.sort_values(['date'], 0, False)
	last_idx_date = kdf.iloc[0,0]
	idx_date = datetime.datetime.strptime(last_idx_date, '%Y-%m-%d').date()

	#得到最近一天的实时信息，得到日期
	idx_df = ts.get_realtime_quotes('399001')
	rq_idx = idx_df.ix[0,'date']
	rq_idx_dt = datetime.datetime.strptime(rq_idx, '%Y-%m-%d').date()
	
	ddd = '2017-11-05'
	print (today-rq_idx_dt).days
	if today==ddd:
		print "===="
	else:
		print "!!!=="

	print idx_date, rq_idx_dt
	cmp_delta = rq_idx_dt-idx_date
	exit(0)
	
	

	qdate = '2017-11-03'
	qdate2 = '2017-11-04'
	#df = ts.get_hist_data('603987', ktype='15', start=qdate, end=qdate2)
	df = ts.get_realtime_quotes('603987')
	print df
	for index,row in df.iterrows():
		print index
		#print row
'''
		last_close = float(row['close'])-float(row['price_change'])
		stockInfo.append(row['close'])
		stockInfo.append(row['p_change'])
		stockInfo.append(last_close)
		stockInfo.append(row['open'])
		stockInfo.append(row['high'])
		stockInfo.append(row['low'])
		stockInfo.append(row['volume'])
'''