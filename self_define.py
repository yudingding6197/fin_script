#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import time
import string
import datetime
import getopt
import tushare as ts
from internal.common_inf import *
from internal.dfcf_interface import *
from internal.ts_common import *

def rt_column(column):
	c0 = ['code', 'name']
	c1 = ['open', 'p_close', 'price', 'high', 'low']
	c2 = ['bidb','bids','volume','amount']
	c3 = ['b1_v','b1','b2_v','b2','b3_v','b3','b4_v','b4','b5_v','b5']
	c4 = ['s1_v','s1','s2_v','s2','s3_v','s3','s4_v','s4','s5_v','s5']
	c5 = ['date','time','state']
	column.extend(c0)
	column.extend(c1)
	column.extend(c2)
	column.extend(c3)
	column.extend(c4)
	column.extend(c5)

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

def index_follow_ud(head, index_ud):
	if index_ud!='':
		obj = index_ud.split('|')
		up = obj[0]
		ping = obj[1]
		down = obj[2]
		print("%s  %4s %4s %4s"%(head, up, ping, down))
	else:
		print(head)
		
	
def index_info(df, show_idx, qt_index):
	if df is None:
		return
	sh_info = ''
	sz_info = ''
	if qt_index is not None:
		qtObj = re.match(r'"(.*?)","(.*)"', qt_index)
		if qtObj is None:
			print("Invalid qt_index", qt_index)
		else:
			index_dt = qtObj.group(1)
			#print (index_dt)
			itemObj = index_dt.split(',')
			sh_info = itemObj[6]
			sz_info = itemObj[7]
	for index,row in df.iterrows():
		if row[0] not in show_idx:
			continue

		open = float(row['open'])
		close = float(row['close'])
		preclose = float(row['preclose'])
		if row['code'] == '000001':
			head = "%8.2f(%6s)"%(close, row[2])
			index_follow_ud(head, sh_info)
		elif row['code'] == '399001':
			head = "%8.2f(%6s)"%(close, row[2])
			index_follow_ud(head, sz_info)
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

#Main
curdate = ''
data_path = "debug/_self_define.txt"
exclude = 0
show_flag = 0
stockCode = []
stockCode_sn = []
qt_stage = 0
if __name__=="__main__":
	optlist, args = getopt.getopt(sys.argv[1:], '?fen')
	for option, value in optlist:
		if option in ["-f","--file"]:
			data_path='../data/entry/miner/filter.txt'
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

	read_def(data_path, stockCode, stockCode_sn)
	if show_flag==1:
		list_latest_news(stockCode, curdate)
		exit(0)
	#当前时间对应情况
	qt_stage = quotation_st()
	#Index实时信息
	qt_index = getIndexStat()
	#print(qt_index)

	show_idx = ['000001', '399001', '399005', '399006']
	idx_df=ts.get_index()
	index_info(idx_df, show_idx, qt_index)

	#codeArray = ['399678']
	#list_extra_index(codeArray)


	column = []
	rt_column(column)
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
