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

#TODO: 增加股票代码合法性检查，sn, tt, nt下载的文件格式不一样，sn错误的时候，输出日志取消
def handle_data_source(entry, code, trdate):
	tickdf = None
	ds = ['sn', 'tt', 'nt']
	i = 0
	for item in ds:
		try:
			tickdf = ts.get_tick_data(code, td, src=item)
		except:
			print code, "Switch src, cur is", item
		else:
			break
	if tickdf is None:
		print code, trdate, "is None"
		return
	cdpath = entry + '/' + code
	fpath = cdpath + '/' + code + '_' + trdate +'.csv'
	tickdf.to_csv(fpath, encoding="gbk")
	return

def check_code_path(entry, code, trdate):
	cdpath = entry + '/' + code
	if not os.path.exists(cdpath):
		os.makedirs(cdpath)

	fpath = cdpath + '/' + code + '_' + trdate +'.csv'
	if not os.path.exists(fpath):
		return 0
	if not os.path.isfile(fpath):
		print "Error: check file:", fpath
	return 1

def verify_bid_code(codes_list, tdx_chk):
	if tdx_chk==0:
		file = open(fpath, 'r')
		line=file.readline()
		while (line):
			code = line[:6]
			codes_list.append(code)
			line=file.readline()
		file.close()
		return

	file = open(fpath, 'r')
	line=file.readline()
	df = None
	LOOP_COUNT = 0
	tdxcn = ts.get_apis()
	while (line):
		if LOOP_COUNT>3:
			print "Too many error, retry"
			break
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
			#line=file.readline()
			LOOP_COUNT += 1
			continue
		LOOP_COUNT = 0
		if not df[td].empty:
			ncode = df[td]['code'][0]
			print ncode
			codes_list.append(ncode)
		line=file.readline()

	file.close()
	ts.close_apis(tdxcn)

if __name__=='__main__':
	entry = '../data/entry/resp'
	fpath = '../data/entry/market/latest_stock.txt'
	days = 5
	tradeList = []
	get_pre_trade_date(tradeList, 5)
	if len(tradeList)!=days:
		print "Fail to get trade date"
		exit()
	td = tradeList[0]
	if not os.path.exists(entry):
		os.makedirs(entry)

	codes_list = []
	verify_bid_code(codes_list, 0)

	print "Start to add tick data"
	for code in codes_list:
		result = check_code_path(entry, code, td)
		if result==0:
			handle_data_source(entry, code, td)
		