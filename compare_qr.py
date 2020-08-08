#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import time
import string
import datetime
import platform
import shutil
import getopt
#import tushare as ts
#import internal.common
#from internal.ts_common import *
#from internal.dfcf_inf import *
from internal.trade_date import *
from internal.update_tday_db import *
from internal.analyze_realtime import *
from internal.compare_realtime import *
from internal.format_parse import *


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
	
	sysstr = platform.system()
	cur_day = trade_day
	for i in range(0, count):
		pre_day = get_preday(1,cur_day)
		if pre_day=='':
			print("Error: get preday fail", i, cur_day)
			break
		#filename = get_path_by_tdate(pre_day)
		#print("%s \n"%(filename))
	
		stoday = statisticsItem()
		ret = parse_realtime_his_file(cur_day, stoday)
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
		print(cur_day)
		if len(q_dict)>0:
			print("QQQ =========")
			for k in q_dict.keys(): print k, q_dict[k][0], q_dict[k][2]
		if len(r_dict)>0:
			print("RRR =========")
			r_flag = 1
			for k in r_dict.keys(): print k, r_dict[k][0], r_dict[k][2]
		for k in stoday.lst_kbcx:
			if not (k[2]=='DT' or k[2]=='YZDT'):
				continue

			if r_flag==0:
				print("RRR =========")
				r_flag = 1
			for item in stoday.lst_yzdt:
				if item[1]==k[0]:
					print item[0], item[1], k[1], 'YZDT'
			for item in stoday.lst_dt:
				if item[1]==k[0]:
					print item[0], item[1], k[1], 'DT'
			
		#print(q_dict)
		#print(r_dict)
		cur_day = pre_day
	

	exit()
	
	
