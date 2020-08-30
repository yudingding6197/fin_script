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
import threading

from internal.trade_date import *
from internal.math_common import *
from internal.realtime_common import *
from internal.url_juchao.tips_res import *
from internal.url_dfcf.dc_hangqing import *
from internal.url_sina.fetch_sina import *
from internal.url_sina.sina_inf import *
from internal.url_163.service_163 import *
from internal.price_limit import *
#from internal.global_var import *

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
CX_DAYS = 200
desc_notkb=u"未开板"
desc_willon=u"待上市"

def handle_large_fluctuate(code, name, stcsItem, fluc_rate, pre5_date, market_date, price, zt_price, dt_price):
	#print code, pre5_date, round(fluc_rate,2)
	if code[:3] in G_LARGE_FLUC:
		mkDt = datetime.datetime.strptime(market_date, '%Y-%m-%d').date()
		pre5Dt = datetime.datetime.strptime(pre5_date, '%Y-%m-%d').date()
		if (mkDt-pre5Dt).days>0:
			#print code, name.encode('gbk'), round(fluc_rate,2)
			if fluc_rate>=23.0:
				stcsItem.s_large_5day_cx += 1
		else:
			if fluc_rate>=20.0:
				if price==zt_price:
					stcsItem.s_large_zhenfu_zt += 1
				elif price==dt_price:
					stcsItem.s_large_zhenfu_dt += 1
				stcsItem.s_large_zhenfu += 1
		return

	if price==zt_price:
		stcsItem.s_zhenfu_zt += 1
	elif price==dt_price:
		stcsItem.s_zhenfu_dt += 1
	stcsItem.s_zhenfu += 1
	return
	
def analyze_status(st_dict, code, name, props, stcsItem, preStat, yzcx_flag, trade_date, pre300_date, pre5_date):
	if len(code)!=6 or code.isdigit() is False:
		print("Invalid code", code)
		return -1

	fp_list = st_dict['fup_stk']
	new_st_list = st_dict['new_stk']
	non_kb_list = st_dict['nkb_stk']
	
	fpFlag = 0
	if code in fp_list:
		fpFlag = 1

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
	#print(("%s %s,'%s','%s'"%(code, name, props[11], props[12])).encode('gbk'))
	#TODO: 有时候获取数据不全，需要数据校验，重新获取数据
	if props[11]=='-' or props[12]=='-':
		return 0

	try:
		high1 = round(float(props[11]),2)
		low1 = round(float(props[12]),2)
	except:
		#print(("%s %s,'%s','%s'"%(code, name, props[11], props[12])).encode('gbk'))
		for prop in props:
			if isinstance(prop, unicode):
				prop = prop.encode("gbk")
			print prop
		#debug,force error and quit APP
		aa = float("---")
	'''
	if props[11]=='-' or props[12]=='-':
		return -1
	'''
	high = round(float(props[11]),2)
	low = round(float(props[12]),2)
	open = round(float(props[10]),2)
	price = round(float(props[3]),2)
	pre_close = round(float(props[9]),2)
	volume = int(props[8])
	#print(code, name, price, high, low, open, pre_close, volume)
	market_date = props[len(props)-1]

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
	elif code[:3] in G_LARGE_FLUC:
		mkDt = datetime.datetime.strptime(market_date, '%Y-%m-%d').date()
		pre5Dt = datetime.datetime.strptime(pre5_date, '%Y-%m-%d').date()
		#前5天没有涨跌停限制
		if (mkDt-pre5Dt).days>0:
			zt_price1 = pre_close * 100
			dt_price1 = 0.01
		else:
			zt_price1 = pre_close * 1.2
			dt_price1 = pre_close * 0.8
	else:
		zt_price1 = pre_close * 1.1
		dt_price1 = pre_close * 0.9
	zt_price = spc_round2(zt_price1,2)
	dt_price = spc_round2(dt_price1,2)
	#print name, pre_close, zt_price, dt_price
	if (h_percent-l_percent)>15.0:
		handle_large_fluctuate(code, name, stcsItem, h_percent-l_percent, pre5_date, market_date, price, zt_price, dt_price)

	bGetDays = 0
	#YZ状态处理
	stk_list = [0, 0]
	if high==low:
		if open>pre_close:
			#刚开盘，只有1笔成交，会大量的输出，不合适检查
			#if high!=zt_price:
			#	print "Warning: YZ, not ZT??? ", code, high, zt_price
			#刚开盘，通过比较 high and zt_price，过滤非ZT
			if b_ST==1 and high==zt_price:
				stcsItem.s_st_yzzt += 1
				status |= STK_ST_YZZT
			elif b_ST==0 and high==zt_price:
				if code[:3] in G_LARGE_FLUC:
					stcsItem.s_large_yzzt += 1
					stcsItem.s_large_zt += 1
					stcsItem.s_large_open_zt += 1
					stcsItem.s_large_close_zt += 1
					#print "YZZT1", code, name

					bGetDays, count=checkZDTInfo(code, name, fpFlag, 0, preStat)
					if bGetDays==1 or count==-1:
						count = get_zf_days(code, 1, trade_date, 1, stk_list)
					else:
						count += 1
						verify_one_year_cx(market_date, pre300_date, 1, stk_list)
					if stk_list[0]<CX_DAYS:
						stcsItem.s_large_cxzt += 1

					list = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent, count, stk_list[0]]
					stcsItem.lst_large_non_yzcx_yzzt.append(list)
				else:
					stcsItem.s_yzzt += 1
					stcsItem.s_zt += 1
					stcsItem.s_open_zt += 1
					stcsItem.s_close_zt += 1
					#list = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent]
					#pd_list.append(list)
					#ret = check_YZ_not_kb(non_kb_list, code)
					if yzcx_flag==0:
						bGetDays, count=checkZDTInfo(code, name, fpFlag, 0, preStat)
						if bGetDays==1 or count==-1:
							count = get_zf_days(code, 1, trade_date, 1, stk_list)
						else:
							count += 1
							verify_one_year_cx(market_date, pre300_date, 1, stk_list)
						if stk_list[0]<CX_DAYS:
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
				if code[:3] in G_LARGE_FLUC:
					stcsItem.s_large_yzdt += 1
					stcsItem.s_large_dt += 1
					stcsItem.s_large_open_dt += 1
					bGetDays, count=checkZDTInfo(code, name, fpFlag, 1, preStat)
					#print "YZDT1", code, name

					if bGetDays==1 or count==-1:
						count = get_zf_days(code, 2, trade_date, 1, stk_list)
					else:
						count += 1
						verify_one_year_cx(market_date, pre300_date, 2, stk_list)
					if stk_list[0]<CX_DAYS:
						stcsItem.s_large_cxdt += 1

					list = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent, count, stk_list[0]]
					stcsItem.lst_large_yzdt.append(list)
				else:
					stcsItem.s_yzdt += 1
					status |= STK_YZDT
					stcsItem.s_dt += 1
					status |= STK_DT
					stcsItem.s_open_dt += 1
					status |= STK_OPEN_DT
					'''
					if fpFlag==1:
						#print "FuPai YZDT", code, name.encode('gbk')
						bGetDays = 1
					elif TS_FLAG==1:
						if name[:2]==u'退市':
							#print code, name.encode('gbk'), "DT"
							count = -1
						elif name[-1:]==u'退':
							#print code, name.encode('gbk'), "DT"
							count = -1
						else:
							count = getPreZDtDays(code, 1, preStat)
					else:
						count = getPreZDtDays(code, 2, preStat)
					'''
					bGetDays, count=checkZDTInfo(code, name, fpFlag, 1, preStat)

					if bGetDays==1 or count==-1:
						count = get_zf_days(code, 2, trade_date, 1, stk_list)
					else:
						count += 1
						verify_one_year_cx(market_date, pre300_date, 2, stk_list)
					if stk_list[0]<CX_DAYS:
						stcsItem.s_cxdt += 1

					list = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent, count, stk_list[0]]
					stcsItem.lst_yzdt.append(list)
		#print code,name,open,low,high,price,pre_close
	else:
		#chubn and kaibn先占位，随后线程更新
		if high==zt_price:
			if b_ST==0:
				tmArr = ['','']
				#不在此处调用了
				#get_zdt_time(code, trade_date, zt_price, 0, tmArr)
				chuban = tmArr[0]
				openban = tmArr[1]
				zt_st = ''
				bGetDays, count=checkZDTInfo(code, name, fpFlag, 0, preStat)
				'''
				if fpFlag==1:
					#print type(name)
					#print "FuPai ZT", code, name.encode('gbk')
					bGetDays = 1
				elif TS_FLAG==1:
					if name[:2]==u'退市':
						#print code, name.encode('gbk'), "ZZT"
						count = -1
					elif name[-1:]==u'退':
						#print code, name.encode('gbk'), "ZZT"
						count = -1
					else:
						count = getPreZDtDays(code, 1, preStat)
				else:
					count = getPreZDtDays(code, 1, preStat)
				'''
				#最新报价处于ZT
				if price==zt_price:
					if bGetDays==1 or count==-1:
						count = get_zf_days(code, 1, trade_date, 1, stk_list)
					else:
						count += 1
						verify_one_year_cx(market_date, pre300_date, 1, stk_list)
					if code[:3] in G_LARGE_FLUC:
						#仅仅计算最后还是ZT的item
						#zt_time_analyze(chuban, stcsItem)
						#print "ZT ", code, name.encode('gbk'), change_percent, zt_price, price
						stcsItem.s_large_zt += 1
						if open==zt_price:
							stcsItem.s_large_open_zt += 1
							if price==open:
								stcsItem.s_large_close_zt += 1
								stcsItem.s_large_open_T_zt += 1
								zt_st = 'T'
						if stk_list[0]<CX_DAYS:
							stcsItem.s_large_cxzt += 1
						list = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent, count, stk_list[0], chuban, zt_st, zt_price]
						stcsItem.lst_large_non_yzcx_zt.append(list)
					else:
						#仅仅计算最后还是ZT的item
						#zt_time_analyze(chuban, stcsItem)
						stcsItem.s_zt += 1
						status |= STK_ZT
						if open==zt_price:
							stcsItem.s_open_zt += 1
							status |= STK_OPEN_ZT
							if price==open:
								stcsItem.s_close_zt += 1
								stcsItem.s_open_T_zt += 1
								zt_st = 'T'
						if stk_list[0]<CX_DAYS:
							stcsItem.s_cxzt += 1
						list = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent, count, stk_list[0], chuban, zt_st, zt_price]
						stcsItem.lst_non_yzcx_zt.append(list)

						'''	
						count = get_zf_days(code, 1, trade_date, 1, stk_list)
						if yzcx_flag==0:
							if stk_list[0]<CX_DAYS:
								stcsItem.s_cxzt += 1
							list = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent, count, stk_list[0], chuban, zt_st]
							stcsItem.lst_non_yzcx_zt.append(list)
						'''						
				#曾经最高报价处于ZT，现在不是了
				else:
					if bGetDays==1 or count==-1:
						count = get_zf_days(code, 1, trade_date, 0, stk_list)
					else:
						verify_one_year_cx(market_date, pre300_date, 1, stk_list)
					if code[:3] in G_LARGE_FLUC:
						#print "ZTHL ", code, name.encode('gbk'), change_percent, zt_price, price
						stcsItem.s_large_zthl += 1
						if open==zt_price:
							stcsItem.s_large_open_zt += 1
							stcsItem.s_large_dk_zt += 1
							zt_st = 'K'
							#print stcsItem.s_zthl,code,name,price,high,zt_price
						list = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent, count, stk_list[0], chuban, openban, zt_st, zt_price]
						#print list
						stcsItem.lst_large_non_yzcx_zthl.append(list)
						if change_percent<=7:
							stcsItem.lst_large_kd.append(name)
						if price<open:
							stcsItem.s_large_zt_o_gt_c += 1
					else:
						stcsItem.s_zthl += 1
						status |= STK_ZTHL
						if open==zt_price:
							stcsItem.s_open_zt += 1
							status |= STK_OPEN_ZT
							stcsItem.s_dk_zt += 1
							zt_st = 'K'
							#print stcsItem.s_zthl,code,name,price,high,zt_price
						list = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent, count, stk_list[0], chuban, openban, zt_st, zt_price]
						#print len(stcsItem.lst_non_yzcx_zthl)
						#print list
						stcsItem.lst_non_yzcx_zthl.append(list)
						if change_percent<=3:
							stcsItem.lst_kd.append(name)
						if price<open:
							stcsItem.s_zt_o_gt_c += 1
		if low==dt_price:
			if b_ST==0:
				tmArr = ['','']
				#get_zdt_time(code, trade_date, dt_price, 1, tmArr)
				chuban = tmArr[0]
				openban = tmArr[1]
				dt_st = ''
				if open==dt_price:
					if code[:3] in G_LARGE_FLUC:
						stcsItem.s_large_open_dt += 1
						status |= STK_OPEN_DT
						if price!=dt_price:
							stcsItem.s_large_open_dt_dk += 1
					else:
						stcsItem.s_open_dt += 1
						status |= STK_OPEN_DT
						if price!=dt_price:
							stcsItem.s_open_dt_dk += 1

				bGetDays, count=checkZDTInfo(code, name, fpFlag, 1, preStat)
				'''
				if fpFlag==1:
					print "FuPai DT or DTFT", code, name
					bGetDays = 1
				elif TS_FLAG==1:
					if name[:2]==u'退市':
						#print code, name.encode('gbk'), "DDT"
						count = -1
					elif name[-1:]==u'退':
						#print code, name.encode('gbk'), "DDT"
						count = -1
					else:
						count = getPreZDtDays(code, 1, preStat)
				else:
					count = getPreZDtDays(code, 2, preStat)
				'''
				if price==dt_price:
					if bGetDays==1 or count==-1:
						count = get_zf_days(code, 2, trade_date, 1, stk_list)
					else:
						count += 1
						verify_one_year_cx(market_date, pre300_date, 2, stk_list)
						
					if code[:3] in G_LARGE_FLUC:
						#print "DT ", code, name, change_percent, zt_price, price
						stcsItem.s_large_dt += 1
						status |= STK_DT
						if open==dt_price:
							dt_st = 'DT'
						if stk_list[0]<CX_DAYS:
							stcsItem.s_large_cxdt += 1

						#DT Data
						list = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent, count, stk_list[0], chuban, dt_st, dt_price]
						stcsItem.lst_large_dt.append(list)
					else:
						stcsItem.s_dt += 1
						status |= STK_DT
						if open==dt_price:
							dt_st = 'DT'
						if stk_list[0]<CX_DAYS:
							stcsItem.s_cxdt += 1

						#DT Data
						list = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent, count, stk_list[0], chuban, dt_st, dt_price]
						stcsItem.lst_dt.append(list)
				else:
					#DTFT Data
					if bGetDays==1 or count==-1:
						count = get_zf_days(code, 2, trade_date, 0, stk_list)
					else:
						verify_one_year_cx(market_date, pre300_date, 2, stk_list)
					if code[:3] in G_LARGE_FLUC:
						#print "DTFT ", code, name, change_percent, zt_price, price
						stcsItem.s_large_dtft += 1
						status |= STK_DTFT
						if open==dt_price:
							dt_st = 'K'

						list = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent, count, stk_list[0], chuban, openban, dt_st, dt_price]
						stcsItem.lst_large_dtft.append(list)
					else:
						stcsItem.s_dtft += 1
						status |= STK_DTFT
						if open==dt_price:
							dt_st = 'K'

						list = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent, count, stk_list[0], chuban, openban, dt_st, dt_price]
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
	if code[:3] in G_LARGE_FLUC:
		if zf_range>=25.0:
			if change_percent>=12.0:
				list = [code, name, change_percent, price, zf_range]
				stcsItem.lst_large_nb.append(list)
			elif change_percent<=-12.0:
				list = [code, name, change_percent, price, zf_range]
				stcsItem.lst_large_jc.append(list)
	else:
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
	#KCB CYB不限涨跌幅，所以是开板
	if code[:3] in G_LARGE_FLUC:
		return 1
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
				klist = get_kline_day_data(code, 60)
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
			#print code, name.encode('gbk'), item['sl']
			listing_date = item['listingdate'][:10]
			yzb_days = int(float(item['sl']))
			kb_date = calcu_back_date(yzb_days, listing_date)
			if kb_date!="" and kb_date==trade_date:
				#print "handle KB",code,name,item['kb'],item['sl'],yzb_days,kb_date
				preClose = float(props[9])
				price = float(props[3])
				chg_perc = round((price-preClose)*100/preClose,2)

				open_list = [code, name, chg_perc, price, yzb_days]
				today_open.append(open_list)
		break
	if bopen==0:
		#print "Not OpenBan", code, name
		stcsItem.s_cx_yzzt += 1

	return bopen

#检查是否当日上市新股
# -1: 有错误
#  0: 不是new stk
#  1: 是当天上的new stk
def check_new_market(new_stock_list, code, name, props, stcsItem, trade_day, today_open):
	itemLen = 26
	if len(props)!=itemLen:
		print("Stock item length not ", itemLen, code, name)
		return -1

	market_date = props[itemLen-1]
	if market_date!=trade_day:
		return 0
	if code[:3] in G_LARGE_FLUC:
		return 1

	#print(props)
	if code in new_stock_list:
		#检查第一天是否开板了
		ret = check_YZ_new_market(code, stcsItem)
		if ret==-1:
			#如果第一天就开板，加入当日开板的List中
			price = round(float(props[3]),2)
			pre_close = round(float(props[9]),2)
			chg_perc = round((price-pre_close)*100/pre_close,2)
			open_list = [code, name, chg_perc, price, 0]
			today_open.append(open_list)
	else:
		#如果上市日期是当前日期，但是并不是新股，这是重新复牌上市的票子
		#不进行分析首日重新上来
		if market_date==trade_date:
			print( "Check the item: %s %s"%(code, name) )
			return 0
	return 1

	
#获取New STK的相关信息
#new_list: 
#	当天上市的NewItem，包含个股多列数据
#new_code_list: 
#	当天上市的NewItem，仅仅包含个股代码
#non_kaiban_list：
#	30天以内的所有上市企业，不论是否KB都包含
def get_new_market_stock(trade_day, new_list, non_kaiban_list, new_code_list=None, src=''):
	sort_list = []
	if src=='' or src=='dc':
		get_new_stk_from_dfcf(sort_list)
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
			#获取前30以内上市的，不论是否KB，先加入list
			listing = item['listingdate'][:10]
			listingDt = datetime.datetime.strptime(listing, '%Y-%m-%d').date()
			pre30Dt = datetime.datetime.strptime(pre30_date, '%Y-%m-%d').date()
			if (listingDt-pre30Dt).days<=0:
				continue
			non_kaiban_list.append(item)
			#print "CXItem", item['securitycode'], item['securityshortname'],item['kb'],item['sl']
	return

def qry_loop(index, qryArgs, trade_date, qLock):
	#print desc
	#print stcsList
	for item in qryArgs:
		tmArr = ['','']
		code = item[1][0]
		desc = item[0]
		type = 0
		if desc=='zt  ':
			zdt_price = item[1][11]
		elif desc=='zthl':
			zdt_price = item[1][12]
		elif desc=='dt  ':
			zdt_price = item[1][11]
			type = 1
		elif desc=='dtft':
			zdt_price = item[1][12]
			type = 1
		else:
			print "Invalid type", desc
			break
		get_zdt_time(code, trade_date, zdt_price, type, tmArr)

		chuban = tmArr[0]
		openban = tmArr[1]
		item[1][9] = chuban
		if desc=='zthl' or desc=='dtft':
			item[1][10] = openban

		#qLock.acquire()
		#print index, item[0], item[1][0], item[1][1], chuban, openban
		#print item
		#qLock.release()
		#break
	#print("query_loop quit", index);
	return

def update_zdt_time(stcsItem, trade_date):
	thrdNum = 6
	threadIdx = 0
	threads = []
	qryThread = [[] for i in range(thrdNum)]
	lock = threading.Lock()
	#print qryThread

	for item in stcsItem.lst_non_yzcx_zt:
		#print item[0]
		lst = qryThread[threadIdx%thrdNum]
		lst.append(['zt  ', item])
		threadIdx += 1
	for item in stcsItem.lst_non_yzcx_zthl:
		#print item[0]
		lst = qryThread[threadIdx%thrdNum]
		lst.append(['zthl', item])
		threadIdx += 1
	for item in stcsItem.lst_dt:
		#print item[0]
		lst = qryThread[threadIdx%thrdNum]
		lst.append(['dt  ', item])
		threadIdx += 1
	for item in stcsItem.lst_dtft:
		#print item[0]
		lst = qryThread[threadIdx%thrdNum]
		lst.append(['dtft', item])
		threadIdx += 1

	for item in stcsItem.lst_large_non_yzcx_zt:
		#print item[0]
		lst = qryThread[threadIdx%thrdNum]
		lst.append(['zt  ', item])
		threadIdx += 1
	for item in stcsItem.lst_large_non_yzcx_zthl:
		#print item[0]
		lst = qryThread[threadIdx%thrdNum]
		lst.append(['zthl', item])
		threadIdx += 1
	for item in stcsItem.lst_large_dt:
		#print item[0]
		lst = qryThread[threadIdx%thrdNum]
		lst.append(['dt  ', item])
		threadIdx += 1
	for item in stcsItem.lst_large_dtft:
		#print item[0]
		lst = qryThread[threadIdx%thrdNum]
		lst.append(['dtft', item])
		threadIdx += 1

	#print "lll=", len(qryThread[0]),len(qryThread[1])
	threadIdx = 0
	for threadIdx in range(len(qryThread)):
		qryArgs = qryThread[threadIdx]
		t = threading.Thread(target=qry_loop, args=(threadIdx, qryArgs, trade_date, lock))
		threads.append(t)

	'''
	'''
	for item in threads:
		item.start()
	for item in threads:
		item.join()

	for item in stcsItem.lst_non_yzcx_zt:
		#print("upZdt %s %s '%s'"%(item[0], item[1], item[9])).encode('gbk')
		chuban = item[9]
		zt_time_analyze(item[0], chuban, stcsItem)
	for item in stcsItem.lst_large_non_yzcx_zt:
		#print("CZL_upZdt %s %s '%s'"%(item[0], item[1], item[9])).encode('gbk')
		chuban = item[9]
		zt_time_analyze(item[0], chuban, stcsItem)
	
	return

#分析所有STK的信息
def collect_all_stock_data(st_dict, today_open, stcsItem, preStat, trade_date, debug=0):
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
	pre300_date = get_preday(CX_DAYS, trade_date)
	pre5_date = get_preday(PRE_FIVE_DAYS, trade_date)
	#print ("collect_all_stock1_data:", pre30_date, pre5_date)
	
	status = 0
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
		#if code[:3] in G_LARGE_FLUC:
		#	continue
		#排除退市的个股
		if name[:2]==u'退市' or name[-1:]==u'退':
			st_dict['tui_stk'].append(item)
			continue

		#if code[:3] not in G_LARGE_FLUC:
		#如果是当天上市，不再继续检查
		ret=check_new_market(new_st_list, code, name, item, stcsItem, trade_date, today_open)
		if ret!=0:
			continue

		#检查是否今日KB
		ret = check_CX_open_ban(non_kb_list, code, name, item, stcsItem, trade_date, pre30_date, today_open)
		if ret==-1:
			status = ret
			break
		elif ret==0:
			yzcx_flag=1
		elif ret==1:
			yzcx_flag=0

		analyze_status(st_dict, code, name, item, stcsItem, preStat, yzcx_flag, trade_date, pre300_date, pre5_date)
		#ret, code = parseCode1(item[:6])
		#if ret==-1:
		#	print ("Invalid code", item[:6])
		#cur_list.append(code)
		#print(item[0], item[1], item[2])
		#print cur_list

	update_zdt_time(stcsItem, trade_date)
	return status

