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
from internal.dfcf_inf import *
from internal.ts_common import *

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

def extract_code(file, key_title, index, dict):
	list = []
	stockList = []
	dayList = []
	line = file.readline()
	max_val = 0
	while line:
		if len(line)<=3:
			if index>2:
				if int(max_val)==0:
					return
				#print (stockList)
				#print (dayList)
				for idx in range(len(dayList)):
					#print(idx, dayList[idx], max_val)
					if max_val==dayList[idx]:
						list.append(stockList[idx])
				stockList = list
			dict[key_title[index]] = stockList
			return
		#obj = line.split(' ')
		#print(obj[0], obj[1], obj[2])
		obj = re.match(r' *([\d]+) ([\d]+).* ([-]?\d+\.[\d]+)[ \t]+(\d+) ', line)
		if obj is None:
			print("obj is None" + line)
		else:
			if int(obj.group(4))>2 and index<=2:
				stockList.append(obj.group(2))
			elif index>=3:
				#print(key_title[index], obj.group(2), obj.group(4))
				stockList.append(obj.group(2))
				dayInt = int(obj.group(4))
				dayList.append(dayInt)
				if max_val<dayInt:
					max_val = dayInt
		line = file.readline()
	#end while

#Main
curdate = ''
data_path = "debug/_self_define.txt"
exclude = 0
show_flag = 0
stockCode = []
stockCode_sn = []
qt_stage = 0
pre_day = 1
if __name__=="__main__":
	optlist, args = getopt.getopt(sys.argv[1:], '?d:')
	for option, value in optlist:
		if option in ["-d","--preday"]:
			pre_day=int(value)
			if pre_day<1:
				print("pre_day must greater than 0")
				exit()
		elif option in ["-?","--???"]:
			print("Usage:" + os.path.basename(sys.argv[0]) + " [-d pre_day]")
			exit()

	tradeList = []
	get_pre_trade_date(tradeList, pre_day+3)
	#print("td list:", tradeList)

	data_path = "../data/entry/realtime/rt_" + tradeList[pre_day-1] + ".txt"
	#print(data_path)
	if not os.path.isfile(data_path):
		print("No file:" + data_path)
		exit(0)

	file = open(data_path, 'r')
	if file is None:
		print("Error open file" + data_path)
		exit()

	column = []
	create_column(column)
	qt_stage = quotation_st()
	print(tradeList[pre_day-1] + " Info")

	p_flag = 0
	index = 0
	line = file.readline()
	dict = {}
	key_title = ['YZZT ', 'ZT ', 'ZTHL ', 'YZDT ', 'DT ', 'DTFT ']
	while line:
		if len(line)<=6:
			line = file.readline()
			continue
		if p_flag == 1:
			for i in range(len(key_title)):
				if line[:3]==key_title[i][:3]:
					index = i
					#print(i, key_title[i])
					extract_code(file, key_title, i, dict)
					break
			if line[:6] == "TIME: ":
				p_flag=0
				break
			#print line
			
			line = file.readline()
			continue

		if line[:6] == "TIME: ":
			obj = re.match(r'TIME: (.*) (\d+):(\d+)', line)
			hour = int(obj.group(2))
			minute = int(obj.group(3))
			if hour>=15 and minute>0:
				#print (line)
				p_flag = 1
		line = file.readline()

	for item in key_title:
		if dict.has_key(item):
			#print(dict[item])
			sn_code = []
			for cd in dict[item]:
				ncode = sina_code(cd)
				sn_code.append(ncode)

			rt_list = []
			realtime_price(sn_code, rt_list)
			df = pd.DataFrame(rt_list, columns=column)
			rt_quotes(df, item, qt_stage)
	#end for key_title

	#print(dict)
