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
from internal.ts_common import *
from internal.dfcf_inf import *

def list_realtime_info(basic, codeArray):
	if len(codeArray)==0:
		return
	df = ts.get_realtime_quotes(codeArray)
	#print df
	#c = df[['name','price','bid','ask','volume','amount','time']]
	#name    open pre_close   price    high     low     bid     ask     volume 
	#amount   ...      a2_p  a3_v    a3_p  a4_v    a4_p  a5_v    a5_p  date      time    code
	print ''
	for index,row in df.iterrows():
		stname = row['name']
		stlen=len(stname.encode('gbk'))
		maxlen=10
		if len(stname)<maxlen:
			left=maxlen-stlen
			while left>0:
				stname += ' '
				left-=1
		open = row['open']
		pre_close = row['pre_close']
		price = row['price']
		high = row['high']
		low = row['low']
		volume = int(row['volume'])
		if basic is None:
			turnover_rt = 0
		else:
			total_vol = float(basic.ix[codeArray[index]]['outstanding'])
			turnover_rt = ((volume/10000) / (total_vol*100))
			
		price_f = float(price)
		pre_close_f = float(pre_close)
		if float(price)==0 or float(high)==0:
			change = '-'
			change_l = '-'
			change_h = '-'
			change_o = '-'
		else:
			change = '%02.02f'%( ((price_f-pre_close_f)/pre_close_f)*100 )
			change_l = '%02.02f'%( ((float(low)-pre_close_f)/pre_close_f)*100 )
			change_h = '%02.02f'%( ((float(high)-pre_close_f)/pre_close_f)*100 )
			change_o = '%02.02f'%( ((float(open)-pre_close_f)/pre_close_f)*100 )

		if basic is None:
			str_fmt = "%6s %s %8s(%6s%%)    %8s(%6s) %8s(%6s)"
			print str_fmt%(codeArray[index], stname, price, change, low, change_l, high, change_h)
		else:
			str_fmt = "%6s %s %8s(%6s%%) (%4.02f%%)     %8s(%6s) %8s(%6s)"
			print str_fmt%(codeArray[index], stname, price, change, turnover_rt, low, change_l, high, change_h)
	return
	
#Main
curdate = ''
data_path = "debug/_self_define.txt"
exclude = 0
optlist, args = getopt.getopt(sys.argv[1:], '?fe')
for option, value in optlist:
	if option in ["-f","--file"]:
		data_path='../data/entry/miner/filter.txt'
	elif option in ["-e","--exclude"]:
		exclude = 1
	elif option in ["-?","--???"]:
		print "Usage:", os.path.basename(sys.argv[0]), " [-f filename]"
		exit()

stockCode = []
today = datetime.date.today()
curdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)
#print curdate

#说明show_flag
#0：不获得每一只的流通盘，不会计算换手率
#1：获得每一只的流通盘，并且计算换手率
#2：显示每一只最新的新闻，当天的新闻全部显示，当天没有只显示一条news
pindex = len(sys.argv)
show_flag = 0
if pindex==2:
	if sys.argv[1]=='1':
		show_flag=1
	elif sys.argv[1]=='2':
		show_flag=2

if not os.path.isfile(data_path):
	print "No file:",data_path
	exit(0)

file = open(data_path, 'r')
if '_self_define' in data_path:
	flag=0
	lines = file.readlines(100000)
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
		#print code
else:
	line = file.readline()
	while line:
		if len(line)>=6:
			code = line[0:6]
			if code.isdigit():
				stockCode.append(code)
		line = file.readline()
	pass
file.close()

if show_flag==1:
	list_latest_news(stockCode, curdate)
	exit(0)

show_idx = ['000001', '399001', '399005', '399006']
idx_df=ts.get_index()
show_index_info(idx_df, show_idx)

codeArray = ['399678']
show_extra_index(codeArray)

st_bas = None
if show_flag==2:
	st_bas=ts.get_stock_basics()
list_realtime_info(st_bas, stockCode)

if exclude==0:
	stock_array = []
	getSelfDefStock(stock_array)
	if len(stock_array)==0:
		print "Fail to get self defined from DFCF"
		exit()
	stockCode = []
	for i in  stock_array:
		stockCode.append(i[:6])
	list_realtime_info(None, stockCode)
