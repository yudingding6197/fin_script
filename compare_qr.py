#!/usr/bin/env python
# -*- coding:utf8 -*-
#强弱对比，包含复牌的item
#前一交易日ZT/DT,下一交易日DT/ZT
import sys
import re
import os
import time
import string
import datetime
import platform
import shutil
import getopt

from internal.trade_date import *
from internal.update_tday_db import *
from internal.analyze_realtime import *
from internal.compare_realtime import *
from internal.format_parse import *
from internal.inf_juchao.daily_trade_tips import *
from internal.inf_juchao.parse_jc_tips import *
from internal.price_limit import *

#针对复牌的个股，检查是否满足强弱势条件，满足则加入
def check_fupai_item(stoday, fp_list, cur_date, qs_dict, rs_dict):
	allLists = [stoday.lst_yzdt, stoday.lst_dt, 
		stoday.lst_non_yzcx_yzzt, stoday.lst_non_yzcx_zt]
	descList = ['YZDT','DT','YZZT','ZT']
	#print descList[:2]
	#print descList[2:]
	for code in fp_list:
		desc = ''
		recList = []
		#print code
		for i in range(len(allLists)):
			for iList in allLists[i] :
				item = iList[0]
				if item==code:
					desc = descList[i]
					recList.append(iList[1])
					recList.append(1)
					recList.append(descList[i])
					recList.append(' FP')
					break

		#如果当天ZDT，接着检查前一天是否ZDT
		#复牌当天是YZDT or DT
		if desc in descList[:2]:
			#print "dsc", code, cur_date, desc
			zdtDesc = check_pre_day_state(code, cur_date)
			if zdtDesc in descList[2:]:
				#print 'matched', code, zdtDesc, recList
				recList[2] = "%4s-%4s"%(zdtDesc,desc)
				rs_dict[code] = recList
		#复牌当天是YZZT or ZT
		elif desc in descList[2:]:
			zdtDesc = check_pre_day_state(code, cur_date)
			if zdtDesc in descList[:2]:
				#print 'matched', code, zdtDesc
				recList[2] = "%4s-%4s"%(zdtDesc,desc)
				qs_dict[code] = recList
		#end if-else
	return

def handle_argument():
	optlist, args = getopt.getopt(sys.argv[1:], 'c:d:')
	for option, value in optlist:
		if option in ["-c","--count"]:
			param_config["Count"] = int(value)
		elif option in ["-d","--date"]:
			param_config["Date"] = value
	#print param_config

param_config = {
	"Count":1,
	"Date":'',
}

#Main Start:
if __name__=='__main__':
	beginTm = datetime.datetime.now()
	t_fmt = '%d-%02d-%02d'
	fmt_time = t_fmt %(beginTm.year, beginTm.month, beginTm.day)

	handle_argument()
	count = param_config["Count"]
	trade_day = ''
	if param_config["Date"]=='':
		trade_day = get_lastday()
	else:
		ret, dt = parseDate2(param_config["Date"])
		if ret==-1:
			exit(-1)
		trade_day = dt
	#trade_day = '2019-03-22'
	#update_latest_trade(trade_day)
	#pre_day = get_preday(6,trade_day)
	#print(trade_day, pre_day)
	
	#print( (jc_dict['fupai']) )

	#sysstr = platform.system()
	cur_day = trade_day
	for i in range(0, count):
		pre_day = get_preday(1,cur_day)
		if pre_day=='':
			print("Error: get preday fail", i, cur_day)
			break
		#print("preD=%s"%(pre_day))

		stoday = statisticsItem()
		ret = parse_realtime_his_file(cur_day, stoday, fmt_time==cur_day)
		if ret == -1:
			break

		sysday = statisticsItem()
		ret = parse_realtime_his_file(pre_day, sysday)
		if ret == -1:
			break

		q_dict = {}
		r_dict = {}
		r_flag = 0
		compare_qiangruo(stoday, sysday, q_dict, r_dict)
		
		jc_dict = {}
		handle_tips_action(cur_day, cur_day)
		read_tfp_fh_in_tips(cur_day, jc_dict)
		if 'fupai' in jc_dict.iterkeys():
			#print jc_dict['fupai']
			check_fupai_item(stoday, jc_dict['fupai'], cur_day, q_dict, r_dict)
		
		print(cur_day)
		if len(q_dict)>0:
			print("QQQ =========")
			for k in q_dict.keys(): print k, q_dict[k][0], '',q_dict[k][1], q_dict[k][2], q_dict[k][3]
		if len(r_dict)>0:
			print("RRR =========")
			r_flag = 1
			#for k in r_dict.keys(): print k, r_dict[k][0], '',r_dict[k][1], r_dict[k][2], r_dict[k][3]
			for k in r_dict.keys():
				#print type(r_dict[k][0])
				print k, r_dict[k][0], '',r_dict[k][1], r_dict[k][2], r_dict[k][3]
		for k in stoday.lst_kbcx:
			if not (k[2]=='DT' or k[2]=='YZDT'):
				continue

			if r_flag==0:
				print("RRR =========")
				r_flag = 1
			for item in stoday.lst_yzdt:
				if item[1]==k[0]:
					print item[0], item[1], k[1], '','  YZDT   ','CXKB'
			for item in stoday.lst_dt:
				if item[1]==k[0]:
					print item[0], item[1], k[1], '','   DT    ','CXKB'
		print ('')
		#print(q_dict)
		#print(r_dict)
		cur_day = pre_day
	

	exit()
	
	
