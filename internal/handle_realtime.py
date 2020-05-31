#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import re
import os
import time
import string
import datetime
import platform
import shutil
import getopt
import urllib2,time
import datetime
import tushare as ts
from internal.trade_date import *

def show_index_info(df, show_idx):
	if df is None:
		return
	for index,row in df.iterrows():
		if row[0] not in show_idx:
			continue

		open = float(row['open'])
		close = float(row['close'])
		preclose = float(row['preclose'])
		print "%8.2f(%6s)"%(close, row[2])

def show_extra_index(codeArray):
	df = ts.get_realtime_quotes(codeArray)
	for index,row in df.iterrows():
		pre_close = row['pre_close']
		price = row['price']
		f_pclose = float(pre_close)
		f_price = float(price)
		value =  (f_price-f_pclose)*100/f_pclose
		print "%8.2f( %3.2f)"%(f_price, round(value,2))

#不通过get_today_all()接口，使用东财接口
def get_today_new_stock(new_st_list):
	'''
	LOOP_COUNT=0
	st_today_base = None
	while LOOP_COUNT<3:
		try:
			st_today_base = ts.get_today_all()
		except:
			LOOP_COUNT += 1
			time.sleep(0.5)
		else:
			break
	if st_today_base is None:
		print "Timeout to get stock basic info, check new stk info manually!!!"
	else:
		st_today_df = st_today_base.sort_values(['changepercent'], 0, False)
		for index,row in st_today_df.iterrows():
			code = row[0].encode('gbk')
			if row['changepercent']>11:
				new_st_list.append(code)
	print ''
	'''

	url = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._A&sty=FCOIATA&sortType=C&sortRule=-1&page=1&pageSize=20&js={rank:[(x)],pages:(pc)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c"
	LOOP_COUNT = 0
	response = None
	while LOOP_COUNT<3:
		try:
			req = urllib2.Request(url)
			response = urllib2.urlopen(req, timeout=5)
		except:
			LOOP_COUNT += 1
			print "URL request timeout"
		else:
			break
	if response is None:
		print "Please check no data from DongCai"
		return

	line = response.read()
	obj = re.match(r'{rank:\["(.*)"\].*', line)
	rank = obj.group(1)
	array = rank.split('","')
	for i in range(0, len(array)):
		props = array[i].split(',')
		if props[2][0]=='N':
			code = props[1]
			new_st_list.append(code)
	return

def get_all_stk_info(st_list, dc_data, today_open, stcsItem):
	sysstr = platform.system()
	today = datetime.date.today()
	number = len(st_list)
	if number<=0:
		return -1

	'''
	#得到ZS的信息，但是当天交易的时候，得不到当天的
	delta1=datetime.timedelta(days=30)
	sdate = today-delta1
	fmt_start = '%d-%02d-%02d' %(sdate.year, sdate.month, sdate.day)
	kdf = ts.get_k_data('000001', index=True, start=fmt_start)
	kdf = kdf.sort_values(['date'], 0, False)
	last_idx_date = kdf.iloc[0,0]
	#idx_date 得到最近一天交易的日期
	idx_date = datetime.datetime.strptime(last_idx_date, '%Y-%m-%d').date()

	#得到最近一天的实时信息，得到日期
	rq_idx = get_last_trade_dt()
	print rq_idx
	rq_idx_dt = datetime.datetime.strptime(rq_idx, '%Y-%m-%d').date()

	cmp_delta = rq_idx_dt-idx_date
	if cmp_delta.days>0:
		idx_date = rq_idx_dt
	'''
	idx_date = get_lastday()
	print(idx_date)

	'''
	b_get_data = 1
	#ZT一次取出 base 个
	#截取list，通过配置起始位置
	base = 23
	loop_ct = number/base
	if number%base!=0:
		loop_ct += 1

	pd_list = []
	for i in range(0, loop_ct):
		end_idx = min(base*(i+1), number)
		cur_list = st_list[i*base:end_idx]
		if len(cur_list)==0:
			break
		#print cur_list
		LOOP_COUNT = 0
		stdf = None
		while LOOP_COUNT<5:
			try:
				stdf = ts.get_realtime_quotes(cur_list)
			except:
				print cur_list, "Get real time except:", LOOP_COUNT
				time.sleep(0.5)
				LOOP_COUNT += 1
				stdf = None
			else:
				break
		if stdf is None:
			print "Get list fail at:", cur_list
			continue

		#print stdf
		for index,row in stdf.iterrows():
			stockInfo = []
			code = cur_list[index]
			# Ignore KCB TODO: support it
			if (code[0:3]=='688'):
				#print("Filter " + code)
				continue
			index += 1
			if sysstr=="Windows":
				name = row[0].encode('gbk')
			elif sysstr == "Linux":
				name = row[0].encode('utf8')
			pre_close = float(row['pre_close'])
			price = float(row['price'])
			volumn = int(row['volume'])

			ask = float(row['ask'])
			if volumn==0 and dc_data==1:
				return 0
			if pre_close==0:
				print ("%s %s invalid value" %(code, name))
				continue
			change_perc = (price-pre_close)*100/pre_close
			today_high = float(row['high'])
			today_low = float(row['low'])
			today_b1_p = float(row['b1_p'])
			today_a1_p = float(row['a1_p'])
			today_bid = float(row['bid'])
			#判断今日是否trade suspend
			if today_high==today_low and today_high==0.0:
				continue
			elif today_b1_p==0.0 and today_a1_p==0.0 and today_bid==0.0:
				continue

			#通过获得K线数据，判断是否YZZT新股
			yzcx_flag = 0
			if b_get_data == 1:
				#获得每只个股每天交易数据
				day_info_df = None
				#新股上市可能有Bug
				try:
					day_info_df = ts.get_k_data(code)
				except:
					print "Error for code:", code, name
				if day_info_df is None:
					continue
				#print code, day_info_df
				trade_days = len(day_info_df)

				b_open=0
				yzzt_day = 0
				if trade_days==0:
					if name[0:1]=='N':
						stcsItem.s_new += 1
						yzcx_flag = 1
						continue
				if trade_days==1:
					if name[0:1]=='N':
						stcsItem.s_new += 1
						yzcx_flag = 1
				for tdidx,tdrow in day_info_df.iterrows():
					open = tdrow[1]
					close = tdrow[2]
					high = tdrow['high']
					low = tdrow['low']
					if high!=low:
						if yzzt_day!=0:
							if (yzzt_day+1)==trade_days:
								chg_perc = round((price-pre_close)*100/pre_close,2)
								open_list = [code, name, chg_perc, price, yzzt_day]
								today_open.append(open_list)
							b_open = 1
							break
					#当ZT打开，就会break for 循环
					yzzt_day += 1
					pre_close = close
				if b_open==0:
					try:
						dt_str=day_info_df.iloc[trade_days-1,0]
					except:
						print code,trade_days
						print day_info_df
						exit()
					last_date = datetime.datetime.strptime(dt_str, '%Y-%m-%d').date()
					#print code, name, idx_date,last_date
					cmp_delta = idx_date-last_date
					if cmp_delta.days==0:
						stcsItem.s_cx_yzzt += 1
						yzcx_flag = 1

				#如果是通过东财获得个股排行，不要判断新股的上市天数
				if dc_data==0:
					#认为YZZT不会超过 33 个交易日
					if trade_days>33:
						b_get_data = 0
				else:
					if trade_days>1:
						l_volume = float(day_info_df.iloc[trade_days-2,2])
						l_pclose = float(day_info_df.iloc[trade_days-2,2])
						l_close = float(day_info_df.iloc[trade_days-1,2])
						l_high = float(day_info_df.iloc[trade_days-1,3])
						chg_perc = round((l_close-l_pclose)*100/l_pclose,2)
						if l_close != l_high or chg_perc<9.5:
							b_get_data = 0
			# end if b_get_data
			#print(index)
			stk_type = analyze_status(code, name, row, stcsItem, yzcx_flag, pd_list, idx_date)
	return 0
	'''
	return 0

