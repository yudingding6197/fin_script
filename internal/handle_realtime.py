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
#import tushare as ts
from internal.trade_date import *
from internal.url_dfcf.dc_hangqing import *
from internal.url_sina.fetch_sina import *
from internal.url_sina.sina_inf import *
from internal.url_163.service_163 import *
from internal.price_limit import *
from global_var import g_new_mark

STK_ZT = 1<<0
STK_DT = 1<<1
STK_ZTHL = 1<<2
STK_DTFT = 1<<3
STK_YZZT = 1<<4
STK_YZDT = 1<<5
STK_OPEN_ZT = 1<<6
STK_OPEN_DT = 1<<7
STK_ST_YZZT = 1<<8
STK_ST_YZDT = 1<<9

PRE_DAYS = 33
desc_notkb=u"未开板"
desc_willon=u"待上市"
	
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

def spc_round2(value,bit):
	b = int(value*10000)
	b1 = b+51
	j = b1/100
	rd_val = float(j)/100
	return rd_val


def get_std_realtime_data(cur_list, src='sn'):
	if src=='sn' or src=='':
		get_realtime_data(cur_list)
	else:
		print("WIP...\n")

#分析时间得到ZT时间，上午or下午
# TODO:
def zt_time_analyze(chuban, stcsItem):
	timeObj = re.match(r'(\d{2}):(\d{2})', chuban)
	hour = int(timeObj.group(1))
	minute = int(timeObj.group(2))
	if hour<=11:
		stcsItem.s_sw_zt += 1
	else:
		stcsItem.s_xw_zt += 1

def get_price_list(code, price_dict, src='163'):
	if src=='' or src=='163':
		get_price_list_163(code, price_dict)
	elif src=='sina':
		sn_code = sina_code(code)
		#get_price_list(sn_code, price_dict)
	else:
		print("WIP", src)
	return

#如果是YZZT，确定是不是还没有开板的CX
def check_YZ_not_kb(non_kaiban_list, code):
	for item in non_kaiban_list:
		if code==item['securitycode']:
			print "TODO:Need check"
			#print item['securitycode'],item['securityshortname']
			return 1
	return 0

# 判断新股第一天是否YZZT
def check_YZ_new_market(code, stcsItem):
	price_dict = {}
	get_price_list(code, price_dict)
	p_len = len(price_dict)
	if p_len==0:
		print ("Error: no price")
		return 0
	elif p_len>3:
		return -1
	#print(price_dict)
	stcsItem.s_cx_yzzt += 1
	return 1

def analyze_status(st_dict, code, name, props, stcsItem, yzcx_flag, trade_date):
	if len(code)!=6 or code.isdigit() is False:
		print("Invalid code", code)
		return -1

	fp_list = st_dict['fup_stk']
	new_st_list = st_dict['new_stk']
	non_kb_list = st_dict['nkb_stk']
	
	status = 0
	'''
	high = round(float(row['high']),2)
	low = round(float(row['low']),2)
	open = round(float(row['open']),2)
	price = round(float(row['price']),2)
	pre_close = round(float(row['pre_close']),2)
	volume = int(row['volume'])
	0,688058,宝兰德,145.52,4.52,3.21%,5.28,11262,164007310,141.00,140.50,147.95,140.50,-,-,-,-,-,-,-,-,0.01%,1.32,11.85,-,2019-11-01
	0,688159,有方科技,54.15,-0.56,-1.02%,3.33,14117,76108605,54.71,54.85,54.85,53.03,-,-,-,-,-,-,-,-,-0.02%,0.86,7.57,-,2020-01-23
	0,688178,万德斯,41.21,-0.05,-0.12%,1.89,6398,26208442,41.26,41.19,41.45,40.67,-,-,-,-,-,-,-,-,0.29%,0.63,3.31,102.20,2020-01-14
	0,688300,XD联瑞新,64.56,-0.54,-0.83%,4.78,11708,76229745,65.10,64.83,67.20,64.09,-,-,-,-,-,-,-,-,0.03%,0.64,5.73,77.80,2019-11-15
	0,688566,吉贝尔,44.97,-0.33,-0.73%,3.89,38958,174909424,45.30,45.18,45.86,44.10,-,-,-,-,-,-,-,-,0.02%,0.74,10.13,83.72,2020-05-18
	'''
	high = round(float(props[11]),2)
	low = round(float(props[12]),2)
	open = round(float(props[10]),2)
	price = round(float(props[3]),2)
	pre_close = round(float(props[9]),2)
	volume = int(props[8])
	#print(code, name, price, high, low, open, pre_close, volume)

	#排除当天没有交易
	if pre_close==0:
		print "PRE_CLOSE Not exist!!!", code, name
		return -1

	if high==0 or low==0:
		print("code", code, high, low)
		return -1

	b_ST = 0
	if name.find("ST")>=0 or name[0:1]=="S":
		b_ST = 1
		#print code,name

	o_percent = (open-pre_close)*100/pre_close
	c_percent = (price-pre_close)*100/pre_close
	h_percent = (high-pre_close)*100/pre_close
	l_percent = (low-pre_close)*100/pre_close
	open_percent = spc_round2(o_percent,2)
	change_percent = spc_round2(c_percent,2)
	high_zf_percent = spc_round2(h_percent,2)
	low_df_percent = spc_round2(l_percent,2)

	#获取ZT
	if b_ST==1:
		zt_price1 = pre_close * 1.05
		dt_price1 = pre_close * 0.95
	else:
		zt_price1 = pre_close * 1.1
		dt_price1 = pre_close * 0.9
	zt_price = spc_round2(zt_price1,2)
	dt_price = spc_round2(dt_price1,2)
	#print name, pre_close, zt_price, dt_price

	#YZ状态处理
	stk_list = [0, 0]
	if high==low:
		if open>pre_close:
			#刚开盘，只有1笔成交，会大量的输出，不合适检查
			#if high!=zt_price:
			#	print "Warning: YZ, not ZT??? ", code, high, zt_price
			if b_ST==1 and high==zt_price:
				stcsItem.s_st_yzzt += 1
				status |= STK_ST_YZZT
			elif b_ST==0 and high==zt_price:
				if high_zf_percent>15:
					pass
				else:
					stcsItem.s_yzzt += 1
					status |= STK_YZZT
					stcsItem.s_zt += 1
					status |= STK_ZT
					stcsItem.s_open_zt += 1
					status |= STK_OPEN_ZT
					stcsItem.s_close_zt += 1
					#list = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent]
					#pd_list.append(list)
					#ret = check_YZ_not_kb(non_kb_list, code)
					if yzcx_flag==0:
						count = get_zf_days(code, 1, trade_date, 1, stk_list)
						if stk_list[0]<300:
							stcsItem.s_cxzt += 1
						list = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent, count, stk_list[0]]
						stcsItem.lst_non_yzcx_yzzt.append(list)
						#print "Not YZCXXXX",code,name
					#print stcsItem.s_zt,code,name,price,change_percent,open
		elif open<pre_close:
			#if low!=dt_price:
			#	print "Warning: YZ, not DT??? ", code, low, dt_price
			if b_ST==1 and low==dt_price:
				stcsItem.s_st_yzdt += 1
				status |= STK_ST_YZDT
			elif b_ST==0 and low==dt_price:
				stcsItem.s_yzdt += 1
				status |= STK_YZDT
				stcsItem.s_dt += 1
				status |= STK_DT
				stcsItem.s_open_dt += 1
				status |= STK_OPEN_DT
				count = get_zf_days(code, 2, trade_date, 1, stk_list)
				if stk_list[0]<300:
					stcsItem.s_cxdt += 1
				list = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent, count, stk_list[0]]
				stcsItem.lst_yzdt.append(list)
		#print code,name,open,low,high,price,pre_close
	else:
		if high==zt_price:
			if b_ST==0:
				tmArr = []
				get_zdt_time(code, trade_date, zt_price, 0, tmArr)
				chuban = tmArr[0]
				openban = tmArr[1]
				zt_st = ''
				if price==zt_price:
					#仅仅计算最后还是ZT的item
					#zt_time_point(code, zt_price, trade_date, stcsItem)
					zt_time_analyze(chuban, stcsItem)
					stcsItem.s_zt += 1
					status |= STK_ZT
					if open==zt_price:
						stcsItem.s_open_zt += 1
						status |= STK_OPEN_ZT
						if price==open:
							stcsItem.s_close_zt += 1
							stcsItem.s_open_T_zt += 1
							zt_st = 'T'
					#list = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent]
					#pd_list.append(list)
					count = get_zf_days(code, 1, trade_date, 1, stk_list)
					if yzcx_flag==0:
						if stk_list[0]<300:
							stcsItem.s_cxzt += 1
						list = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent, count, stk_list[0], chuban, zt_st]
						stcsItem.lst_non_yzcx_zt.append(list)
				else:
					count = get_zf_days(code, 1, trade_date, 0, stk_list)
					stcsItem.s_zthl += 1
					status |= STK_ZTHL
					if open==zt_price:
						stcsItem.s_open_zt += 1
						status |= STK_OPEN_ZT
						stcsItem.s_dk_zt += 1
						zt_st = 'K'
						#print stcsItem.s_zthl,code,name,price,high,zt_price
					list = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent, count, stk_list[0], chuban, openban, zt_st]
					#print len(stcsItem.lst_non_yzcx_zthl)
					#print list
					stcsItem.lst_non_yzcx_zthl.append(list)
				if change_percent<=3:
					stcsItem.lst_kd.append(name)
				if price<open:
					stcsItem.s_zt_o_gt_c += 1

		if low==dt_price:
			if b_ST==0:
				tmArr = []
				get_zdt_time(code, trade_date, dt_price, 1, tmArr)
				chuban = tmArr[0]
				openban = tmArr[1]
				dt_st = ''
				if open==dt_price:
					stcsItem.s_open_dt += 1
					status |= STK_OPEN_DT
					if price!=dt_price:
						stcsItem.s_open_dt_dk += 1

				if price==dt_price:
					stcsItem.s_dt += 1
					status |= STK_DT
					if open==dt_price:
						dt_st = 'DT'
					count = get_zf_days(code, 2, trade_date, 1, stk_list)
					if stk_list[0]<300:
						stcsItem.s_cxdt += 1

					#DT Data
					list = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent, count, stk_list[0], chuban, dt_st]
					stcsItem.lst_dt.append(list)
				else:
					stcsItem.s_dtft += 1
					status |= STK_DTFT
					if open==dt_price:
						dt_st = 'K'

					#DTFT Data
					count = get_zf_days(code, 2, trade_date, 0, stk_list)
					list = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent, count, stk_list[0], chuban, openban, dt_st]
					stcsItem.lst_dtft.append(list)

	#统计开盘涨跌幅度
	if open_percent>0:
		stcsItem.s_open_sz += 1
		if open_percent>=4.0:
			stcsItem.s_open_dz += 1
	elif open_percent<0:
		stcsItem.s_open_xd += 1
		if open_percent<=-4.0:
			stcsItem.s_open_dd += 1
	else:
		#print("%s,%s,%f"%(code,name,open_percent))
		stcsItem.s_open_pp += 1

	#统计开盘涨跌幅度
	if change_percent>0:
		stcsItem.s_close_sz += 1
		if change_percent>=4.0:
			stcsItem.s_close_dz += 1
	elif change_percent<0:
		stcsItem.s_close_xd += 1
		if change_percent<=-4.0:
			stcsItem.s_close_dd += 1
	else:
		stcsItem.s_close_pp += 1
	stcsItem.s_total += 1

	#统计最大涨跌幅度
	if high_zf_percent>=4.0:
		stcsItem.s_high_zf += 1
	if low_df_percent<=-4.0:
		stcsItem.s_low_df += 1

	#统计表现震撼个股 排除YZZT的新股
	zf_range = high_zf_percent-low_df_percent
	if zf_range>=15.0 and yzcx_flag==0:
		if change_percent>=6.0:
			list = [code, name, change_percent, price, zf_range]
			stcsItem.lst_nb.append(list)
		elif change_percent<=-6.0:
			list = [code, name, change_percent, price, zf_range]
			stcsItem.lst_jc.append(list)
	'''
	'''
	return status

def check_CX_open_ban(non_kb_list, code, name, props, stcsItem, trade_date, pre30_date, today_open):
	itemLen = 26
	if len(props)!=itemLen:
		print("Stock item length not ", itemLen, code, name)
		return -1

	market_date = props[itemLen-1]
	mkDt = datetime.datetime.strptime(market_date, '%Y-%m-%d').date()
	pre30Dt = datetime.datetime.strptime(pre30_date, '%Y-%m-%d').date()

	if (pre30Dt-mkDt).days>0:
		#Not CX
		return 1

	#if props[1]=='300850':
	#	for i in range(len(props)):
	#		print i,props[i]

	#强制认为都是KB状态
	bopen = 1
	for item in non_kb_list:
		if item['securitycode']!=code:
			continue
		if item['kb']==desc_notkb:
			#标识为未开，检查今日实际数据
			#print "handle NOTKB",item['securitycode'], item['securityshortname']
			preClose = float(props[9])
			price = float(props[3])
			high = float(props[11])
			low = float(props[12])
			zt_price1 = preClose * 1.1
			zt_price = spc_round2(zt_price1,2)

			if not (high==low and price==zt_price):
				klist = get_kday_data(code, 60)
				yzzt_day = len(klist)
				tail_day = klist[yzzt_day-1]['day']
				if tail_day == trade_date:
					yzzt_day -= 1
				chg_perc = round((price-preClose)*100/preClose,2)
				open_list = [code, name, chg_perc, price, yzzt_day]
				today_open.append(open_list)
			else:
				bopen = 0
		#KB的item，今天是否KB，上一交易日还是封板状态
		else:
			listing_date = item['listingdate'][:10]
			yzb_days = int(float(item['sl']))
			kb_date = calcu_back_date(listing_date, yzb_days)
			if kb_date!="" and kb_date==trade_date:
				#print "handle KB",code,name,item['kb'],item['sl'],yzb_days,kb_date
				preClose = float(props[9])
				price = float(props[3])
				chg_perc = round((price-preClose)*100/preClose,2)

				open_list = [code, name, chg_perc, price, yzb_days]
				today_open.append(open_list)
		break
	if bopen==0:
		print "Not OpenBan", code, name
		stcsItem.s_cx_yzzt += 1

	return bopen

#检查是否当日上市新股
def check_new_market(new_stock_list, code, name, props, stcsItem, trade_day, today_open):
	itemLen = 26
	if len(props)!=itemLen:
		print("Stock item length not ", itemLen, code, name)
		return -1

	market_date = props[itemLen-1]
	if market_date!=trade_day:
		return 0

	#print(props)
	if code in new_stock_list:
		#TODO: KeChuanBan KCB
		if code[:3] in g_new_mark:
			return 1
		ret = check_YZ_new_market(code, stcsItem)
		if ret==-1:
			price = props[1]
			chg_perc = round((price-pre_close)*100/pre_close,2)
			open_list = [code, name, chg_perc, price, 0]
			today_open.append(open_list)
	else:
		#如果上市日期是当前日期，但是并不是新股，这是重新复牌上市的票子
		if market_date==trade_date:
			print( "Check the item: %s %s"%(code, name) )
	return 1

	
#获取当日上市New STK
def get_new_market_stock(trade_day, new_list, non_kaiban_list, new_code_list=None, src=''):
	sort_list = []
	if src=='' or src=='dc':
		getNewStockMarket(sort_list)
	else:
		print("Unknown source", src)
		return
	pre30_date = get_preday(PRE_DAYS, trade_day)

	for item in sort_list:
		#if item['securitycode']=='300855' or item['securitycode']=='603087':
		#	for key,value in (item.items()): print "CXkey-val:",key, value

		#print "get_new_market_stock", item['securitycode'],item['securityshortname']
		if item['listingdate'][:10]==trade_day:
			new_list.append(item)
			if new_code_list is not None:
				new_code_list.append(item['securitycode'])
		elif item['kb']==desc_willon:
			#print "WillOn", item['securitycode'], item['securityshortname'],item['listingdate'][:10]
			continue
		else:
			listing = item['listingdate'][:10]
			listingDt = datetime.datetime.strptime(listing, '%Y-%m-%d').date()
			pre30Dt = datetime.datetime.strptime(pre30_date, '%Y-%m-%d').date()
			if (listingDt-pre30Dt).days<=0:
				continue
			non_kaiban_list.append(item)
			#print "CXItem", item['securitycode'], item['securityshortname'],item['kb'],item['sl']
	return

def collect_all_stock_data(st_dict, today_open, stcsItem, trade_date, debug=0):
	sysstr = platform.system()
	
	st_list = st_dict['all_stk']
	fp_list = st_dict['fup_stk']
	new_st_list = st_dict['new_stk']
	non_kb_list = st_dict['nkb_stk']
	
	#print ("non_kb:", non_kb_list)
	#for item in non_kb_list:
	#	for key,value in item.items(): print key, value
	#	break
	#	print item['securitycode'],item['securityshortname']
	#print ("new_st:", new_st_list)

	stcsItem.s_new = len(new_st_list)
	
	pre30_date = get_preday(PRE_DAYS, trade_date)
	#print ("collect_all_stock1_data:", pre30_date)

	for item in st_list:
		if debug==0:
			code = item[1]
			name = item[2]
		else:
			code = item
			name = "XXXX"

		#if item[1]=='300291':
		#	for i in range(len(item)):
		#		print "DBG_SK,",i,item[i]

		#TODO: KeChuanBan KCB
		if code[:3] in g_new_mark:
			continue

		#如果是当天上的就忽略了
		ret=check_new_market(new_st_list, code, name, item, stcsItem, trade_date, today_open)
		if ret!=0:
			continue

		#检查是否今日KB
		ret = check_CX_open_ban(non_kb_list, code, name, item, stcsItem, trade_date, pre30_date, today_open)
		if ret==-1:
			continue
		elif ret==0:
			yzcx_flag=1
		elif ret==1:
			yzcx_flag=0

		analyze_status(st_dict, code, name, item, stcsItem, yzcx_flag, trade_date)
		#ret, code = parseCode1(item[:6])
		#if ret==-1:
		#	print ("Invalid code", item[:6])
		#cur_list.append(code)
		#print(item[0], item[1], item[2])
		#print cur_list
		#get_std_realtime_data(cur_list, 'sn')
		#print (i)
	
	pass