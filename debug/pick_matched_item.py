#!/usr/bin/env python
# -*- coding:gbk -*-

import sys
import re
import os
import datetime
sys.path.append(".")
sys.path.append("..")
from internal.ts_common import *
from internal.dfcf_inf import *
import tushare as ts

def handle_float(str):
	if str=='-':
		obj = None
	else:
		obj = float(str)
	return obj

def handle_int(str):
	if str=='-':
		obj = None
	else:
		obj = int(str)
	return obj

def handle_item_data(stk_item, stockInfo, pos=0):
	str_arr = stk_item.split(',')
	name = str_arr[pos+1]
	code = str_arr[pos]

	close = str_arr[pos+2]
	close = handle_float(close)

	change_price = str_arr[pos+3]
	change_price = handle_float(change_price)

	change_perc = str_arr[pos+4]
	if change_perc=='-':
		change_perc = None
	else:
		change_perc = change_perc[:-1]
		change_perc = float(change_perc)
		if change_perc<2:
			return 0
		elif change_perc>9.9:
			return 1

	stockInfo.append(stk_item)
	return 1

def filter_share(stkList, filterList):
	for item in stkList:
		ret = strategy_price_increase(item, filterList)
		if ret==0:
			break
	return

#选出符合条件的item
if __name__=='__main__':
	cur=datetime.datetime.now()
	tmstr = '%02d%02d'%(cur.hour, cur.minute)
	tdate = get_last_trade_dt()
	
	stkList = []
	get_market_by_chg_per(stkList)
	print "Start to handle data"	

	filterList = []
	filter_share(stkList, filterList)

	folder='../data/entry/filter'
	if not os.path.exists(folder):
		os.makedirs(folder)

	fname = '%s/filter_%s_%s.txt' % (folder, tdate, tmstr)
	file = open(fname, 'w')
	index=1
	for item in filterList:
		file.write(item+'\n')
	file.close()