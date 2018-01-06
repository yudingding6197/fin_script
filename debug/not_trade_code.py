#!/usr/bin/env python
# -*- coding:gbk -*-

import sys
import re
import os
import time
import getopt
import datetime
sys.path.append(".")
sys.path.append("..")
from internal.ts_common import *
import tushare as ts

#验证获得以前交易时间停牌的股票
def verify_not_bid_code(trade_dt, codes_list, not_trade_list):
	df = None
	LOOP_COUNT = 0
	tdxcn = ts.get_apis()
	for item in codes_list:
		if LOOP_COUNT>3:
			print "Too many error, retry"
			break
		code = item
		try:
			df = ts.bar(code, tdxcn)
		except Exception as e:
			print "ERROR:", code, e
			ts.close_apis(tdxcn)
			tdxcn = ts.get_apis()
		if df is None:
			print code, "get bar is None"
			LOOP_COUNT += 1
			continue
		LOOP_COUNT = 0
		try:
			dtList=list(df.index)
			dtList = map(str, dtList)
			chkDt = trade_dt + ' 00:00:00'
			if chkDt not in dtList:
				print code, td, "NO TRADE"
				not_trade_list.append(code)
		except Exception as e:
			print df.head(5)
			print code, "ERROR:", e
	ts.close_apis(tdxcn)
	return

#获取所有item的code
def get_all_last_codes(folder, codes_list):
	fpath = folder + "latest_stock.txt"
	file = open(fpath, 'r')
	line=file.readline()
	while (line):
		code = line[:6]
		codes_list.append(code)
		line = file.readline()
	file.close()
	return

#Main 
# 
param_config = {
	"Date":''
}

if __name__=='__main__':
	init_trade_obj()
	td = ''
	nowToday = datetime.date.today()
	optlist, args = getopt.getopt(sys.argv[1:], '?d:')
	for option, value in optlist:
		if option in ["-d","--date"]:
			ret,stdate = parseDate(value, nowToday)
			if ret==-1:
				exit()
			param_config['Date'] = stdate
			td = stdate
		elif option in ["-?","--??"]:
			print "Usage:", os.path.basename(sys.argv[0]), "-d MMDD/YYYYMMDD"
			exit()

	days = 5
	tradeList = []
	get_pre_trade_date(tradeList, days)
	if len(tradeList)!=days:
		print "Fail to get trade date"
		exit()

	lastTd = str(tradeList[0])
	if lastTd==td:
		print "Latest trade date, not call this function"
		exit()
	if td=='':
		print "Usage:", os.path.basename(sys.argv[0]), "-d MMDD/YYYYMMDD"
		exit()
	if chk_holiday(td):
		print td, "is holiday, Quit"
		exit()

	codes_list = []
	folder = '../data/entry/market/'
	get_all_last_codes(folder, codes_list)
	
	#codes_list = ['603999', '603986', '603161', '300664']
	not_td_list = []
	verify_not_bid_code(td, codes_list, not_td_list)
	print not_td_list

	print "Start to add tick data"
	file = open(folder + "stock_" + td + ".txt", 'w')
	for item in not_td_list:
		file.write(item + '\n')
	file.close()
	#TODO: 更新没有交易的个股到对应文件中
