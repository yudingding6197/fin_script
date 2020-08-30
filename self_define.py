#!/usr/bin/env python
# -*- coding:utf8 -*-

#新增更新juchao交易tips
import sys
import re
import os
import time
import string
import datetime
import getopt
import pandas as pd

from internal.output_general import *
from internal.dfcf_inf import *
from internal.trade_date import *
from internal.inf_juchao.daily_trade_tips import *

def rt_quotes(dtFrame, source, qt_stage):
	print(source)
	for index,row in dtFrame.iterrows():
		#print(row)
		r1_len = len(row[1])
		r1 = row[1].decode('gbk')
		for i in range(10-r1_len):
			r1 += ' '

		if row['state']!='00':
			line = "%06s %-s --   --" %(row[0], r1)
			print (line)
			continue

		open = row['open']
		pre_close = row['p_close']
		price = row['price']
		high = row['high']
		low = row['low']
		volume = int(row['volume'])

		price_f = float(price)
		pre_close_f = float(pre_close)
		bidb_f = float(row['bidb'])
		bidb_s = float(row['bids'])
		if float(price)==0 or float(high)==0:
			change = '-'
			change_l = '-'
			change_h = '-'
			change_o = '-'
			if bidb_f==0 and bidb_s==0:
				pass
			elif bidb_f!=0:
				price_f = bidb_f
				change = '%02.02f'%( ((price_f-pre_close_f)/pre_close_f)*100 )
			elif bidb_s!=0:
				price_f = bids_f
				change = '%02.02f'%( ((price_f-pre_close_f)/pre_close_f)*100 )
			else:
				print("Error: Special Case", price, bidb, bids)
				print(row)
		else:
			change = '%02.02f'%( ((price_f-pre_close_f)/pre_close_f)*100 )
			change_l = '%02.02f'%( ((float(low)-pre_close_f)/pre_close_f)*100 )
			change_h = '%02.02f'%( ((float(high)-pre_close_f)/pre_close_f)*100 )
			change_o = '%02.02f'%( ((float(open)-pre_close_f)/pre_close_f)*100 )
		str_fmt = "%06s %-s %6.2f(%6s%%)   %8s(%6s) %8s(%6s)"
		line = str_fmt %(row[0], r1, price_f, change, low, change_l, high, change_h)
		print(line)

def index_follow_zd(head, index_ud):
	if len(index_ud)>3:
		zhang = index_ud[0]
		ping  = index_ud[1]
		die   = index_ud[2]
		total = int(zhang) + int(ping) + int(die)
		zh_per = int(zhang) * 100 / total
		die_per = int(die) * 100 / total
		
		print("%s    %4s  %4s  %4s  (%2d vs %2d) "%(head, zhang, ping, die, zh_per, die_per))
	else:
		print(head)
	
def index_info(df, show_idx, idxDict):
	if df is None:
		return
	sh_info = ''
	sz_info = ''
	for index,row in df.iterrows():
		if row[0] not in show_idx:
			continue
		open = float(row['open'])
		close = float(row['close'])
		preclose = float(row['preclose'])
		if idxDict.has_key(row['code']):
			head = "%8.2f(%6s)"%(close, row[2])
			index_follow_zd(head, idxDict[row['code']])
		else:
			print("%8.2f(%6s)"%(close, row[2]))

def read_def(data_path, stockCode, stockCode_sn):
	file = open(data_path, 'r')
	if file is None:
		print("Error open file", data_path)
		return
	if '_self_define' in data_path:
		flag=0
		lines = file.readlines(10000)
		for line in lines:
			line=line.strip()
			if line=='STK':
				flag=1
				continue
			elif flag==1 and line=='END':
				break
			if flag==0:
				continue
			code=line.strip()
			if len(code)!=6:
				continue;
			if not code.isdigit():
				continue;
			stockCode.append(code)
			ncode = sina_code(code)
			stockCode_sn.append(ncode)
	else:
		line = file.readline()
		while line:
			if len(line)>=6:
				code = line[0:6]
				if code.isdigit():
					stockCode.append(code)
					ncode = sina_code(code)
					stockCode_sn.append(ncode)
			line = file.readline()
	file.close()

def update_juchao_tips():
	curr = datetime.datetime.now()
	trade_date = get_lastday()
	if curr.hour<9:
		return
	t_fmt = '%d-%02d-%02d'
	cur_date = t_fmt%(curr.year, curr.month, curr.day)
	
	today = datetime.date.today()
	pre20Dt = today - datetime.timedelta(days=20)
	pre20_date = t_fmt%(pre20Dt.year, pre20Dt.month, pre20Dt.day)

	#print cur_date,pre20_date
	fetch_jc_trade_tips(pre20_date, cur_date)

#Main
curdate = ''
data_path = "debug/_self_define.txt"
exclude = 0
show_flag = 0
stockCode = []
stockCode_sn = []
qt_stage = 0
if __name__=="__main__":
	optlist, args = getopt.getopt(sys.argv[1:], '?f:en')
	for option, value in optlist:
		if option in ["-f","--file"]:
			if value=='.':
				data_path='../data/entry/miner/filter.txt'
			else:
				data_path=value
		elif option in ["-e","--exclude"]:
			exclude = 1
		elif option in ["-n","--notice"]:
			show_flag = 1
		elif option in ["-?","--???"]:
			print("Usage:", os.path.basename(sys.argv[0]), " [-f filename] [-e] [-t type]")
			exit()

	if not os.path.isfile(data_path):
		print("No file:",data_path)
		exit(0)

	today = datetime.date.today()
	curdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)
	#更新巨潮的tips信息
	update_juchao_tips()

	read_def(data_path, stockCode, stockCode_sn)
	if show_flag==1:
		list_latest_news(stockCode, curdate)
		exit(0)
	#当前时间对应情况
	qt_stage = quotation_st()
	#Index实时信息
	qt_index = getHSIndexStat()
	idxDict = {}
	ret = get4IndexInfo(idxDict)

	#show_idx = ['000001', '399001', '399005', '399006']
	#idx_df=ts.get_index()
	#index_info(idx_df, show_idx, idxDict)
	show_idx = ['000001', '399001', '399005', '399006','399678']
	show_real_index(show_idx)

	#codeArray = ['399678']
	#list_extra_index(codeArray)


	column = []
	create_column(column)
	#print(column)

	rt_list = []
	realtime_price(stockCode_sn, rt_list)
	#print(rt_list)

	df = pd.DataFrame(rt_list, columns=column)
	#print (df)
	#df.set_index('code')
	rt_quotes(df, '', qt_stage)

	#Get self def from DFCF(DongCai)
	rt_list = []
	stockCode_sn = []
	if exclude==0:
		stock_array = []
		getSelfDefStock(stock_array)
		if len(stock_array)==0:
			print "Fail to get self defined from DFCF"
			exit()
		stockCode = []
		for i in  stock_array:
			stockCode.append(i[:6])
			ncode = sina_code(i[:6])
			stockCode_sn.append(ncode)
			#print ("i===" + ncode)
		realtime_price(stockCode_sn, rt_list)
		df = pd.DataFrame(rt_list, columns=column)
		rt_quotes(df, 'DFCF', qt_stage)

