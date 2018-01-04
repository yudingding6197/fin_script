#!/usr/bin/env python
# -*- coding:gbk -*-

import sys
import re
import os
import datetime
sys.path.append(".")
sys.path.append("..")
from internal.ts_common import *
from internal.dfcf_interface import *
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

def handle_item_data(stk_item, stockInfo):
	str_arr = stk_item.split(',')
	name = str_arr[2]
	code = str_arr[1]
	#if code=='603999':
	#	for i in range(0, len(str_arr)):
	#		print "%02d	%s"%(i, str_arr[i])
	#print "%6s	%s	%s"%(code, str_arr[31], str_arr[34])

	close = str_arr[3]
	close = handle_float(close)

	change_price = str_arr[4]
	change_price = handle_float(change_price)

	change_perc = str_arr[5]
	if change_perc=='-':
		change_perc = None
	else:
		change_perc = change_perc[:-1]
		change_perc = float(change_perc)
		if change_perc<2:
			return 0
		elif change_perc>9.9:
			return 1

	stockInfo.append(stk_item[2:])
	return 1

#选出符合条件的item
if __name__=='__main__':
	days = 5
	tradeList = []
	get_pre_trade_date(tradeList, 5)
	if len(tradeList)!=days:
		print "Fail to get trade date"
	print tradeList
	
	stkList = []
	get_market_by_chg_per(stkList)
	print "Start to handle data"

	filterList = []
	for item in stkList:
		val = handle_item_data('1,'+item, filterList)
		if val==0:
			break

	fname = '../data/entry/filter/' + 'f_1.txt'
	file = open(fname, 'w')
	for item in filterList:
		file.write(item+'\n')
	file.close()