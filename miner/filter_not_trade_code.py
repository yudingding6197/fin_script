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

#FUNC: ���ĳһ������ͣ�Ƶ�items
#Ŀǰͨ��TDX��ѡ�ɻ�ȡ��
#	���û��TDX��һ���DC��ȡ���½���,debug/last_market.py
#	filterִ�е�ʱ�򣬲��Ӳ���(-d)��������ı�����û�н��׵���ȡ��ָ���ļ���
#	����в���(-d)ָ��������,���ͨ��tdx��get_apis()���д������ѽϳ�ʱ����

#��֤�����ǰ����ʱ��ͣ�ƵĹ�Ʊ
#ͨ��TDX��ȡÿֻitem�����н������ڣ����ָ�������Ƿ��������
#���������ָ�������ڣ���item����ͣ��
def verify_not_bid_code(trade_dt, codes_list, not_trade_list):
	LOOP_COUNT = 0
	tdxcn = ts.get_apis()
	for item in codes_list:
		df = None
		if LOOP_COUNT>3:
			print "Too many error, retry"
			break
		code = item
		try:
			df = ts.bar(code, tdxcn)
		except Exception as e:
			print "ERROR:%s %s"%( code, e)
		if df is None:
			LOOP_COUNT += 1
			continue
		LOOP_COUNT = 0
		try:
			dtList=list(df.index)
			dtList = map(str, dtList)
			chkDt = trade_dt + ' 00:00:00'
			if chkDt not in dtList:
				#print code, td, "NO TRADE"
				not_trade_list.append(code)
		except Exception as e:
			#print df.head(5)
			print code, "ERROR:", e
	ts.close_apis(tdxcn)
	return

#��ȡ����item��code
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
if __name__=='__main__':
	init_trade_obj()
	td = ''
	nowToday = datetime.date.today()
	optlist, args = getopt.getopt(sys.argv[1:], '?d:')
	for option, value in optlist:
		if option in ["-d","--date"]:
			ret,stdate = parseDate(value, nowToday, ai=1)
			if ret==-1:
				exit()
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

	todayStr = '%04d-%02d-%02d' %(nowToday.year, nowToday.month, nowToday.day)
	if todayStr==td:
		lastTd = td
	else:
		lastTd = str(tradeList[0])
	if chk_holiday(lastTd):
		print lastTd, "is holiday for last td, Quit"
		exit()
	if td=='' or td==lastTd:
		folder = '../data/entry/market/'
		fname = "latest_stock.txt"
		fpath = folder + fname
		if not os.path.isfile(fpath):
			print "Error, not find" +fname+ ", first to download by latest_market.py"
			exit()
		fLatest = open(fpath, 'r')

		fpath = folder + "stock_" + lastTd + ".txt"
		if os.path.isfile(fpath):
			print fpath, "exist! not update"
			fLatest.close()
			exit()
		print "Ready to save to ", fpath
		file = open(fpath, 'w')
		line = fLatest.readline()
		while line:
			props = line.split(',')
			length = len(props)
			if length>3:
				if props[3]=='-':
					file.write(props[0]+'\n')
			line = fLatest.readline()
		fLatest.close()
		file.close()
		exit()
	if chk_holiday(td):
		print td, "is holiday, Quit"
		exit()

	codes_list = []
	folder = '../data/entry/market/'
	get_all_last_codes(folder, codes_list)

	not_td_list = []
	verify_not_bid_code(td, codes_list, not_td_list)

	print "Start to add tick data"
	file = open(folder + "stock_" + td + ".txt", 'w')
	for item in not_td_list:
		file.write(item + '\n')
	file.close()
