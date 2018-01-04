#!/usr/bin/env python
# -*- coding:gbk -*-

import sys
import re
import os
import datetime
sys.path.append(".")
sys.path.append("..")
from internal.ts_common import *
import tushare as ts

#下载每一天item的每笔交易数据
'''  
{ #3个可用数据源
'tt': 'http://stock.gtimg.cn/data/index.php?appn=detail&action=download&c=sz300553&d=20180102', 
'nt': 'http://quotes.money.163.com/cjmx/2018/20180102/1300553.xls', 
'sn': 'http://market.finance.sina.com.cn/downxls.php?date=2018-01-02&symbol=sz300553'
}
'''

def handle_data_source(code, trdate):
	tickdf = ts.get_tick_data(code, td)
	if tickdf is None:
		print code, trdate, "is None"
		return
	file = code+trdate+'.csv'
	tickdf.to_csv(file, encoding="gbk")
	return

def check_code_path(code, trdate):
	
	return 0

if __name__=='__main__':
	fpath = '../data/entry/market/latest_stock.txt'
	days = 5
	tradeList = []
	get_pre_trade_date(tradeList, 5)
	if len(tradeList)!=days:
		print "Fail to get trade date"
		exit()
	td = tradeList[0]

	index=0
	tdxcn = ts.get_apis()
	file = open(fpath, 'r')
	line=file.readline()
	df = None
	codes_list = []
	while (line):
		code = line[:6]
		try:
			df = ts.bar(code, tdxcn)
		except:
			print "ERROR:"
			ts.close_apis(tdxcn)
			print "Re-connect"
			tdxcn = ts.get_apis()
		if df is None:
			print code, "get bar is None"
			line=file.readline()
			continue
		#print code
		if df[td].empty:
			pass
		else:
			codes_list.append(df[td]['code'])
		line=file.readline()

		index += 1
		if index>10:
			break
	file.close()
	ts.close_apis(tdxcn)
	
	for code in codes_list:
		if check_code_path(code, td)==1:
			handle_data_source(code, td)
		