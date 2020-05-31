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

#Main Start:
if __name__=='__main__':
	trade_day = get_lastday()
	#trade_day = '2019-03-22'
	#update_latest_trade(trade_day)
	pre_day = get_preday(6,trade_day)
	#print(trade_day, pre_day)

	type = 2
	if type==1:
		for i in range(1, 2):
			pre_day = get_preday(i,trade_day)
			if pre_day=='':
				print("Error: get preday fail", i, trade_day)
				break
			#filename = get_path_by_tdate(pre_day)
			#print("%s \n"%(filename))
			stcsItem = statisticsItem()
			ret = parse_realtime_fl(pre_day, stcsItem)
			if ret == -1:
				break
	elif type==2:
		#trade_day = '2020-05-19'
		for i in range(1, 312):
			q_dict = {}
			r_dict = {}
			pre_day = get_preday(1,trade_day)
			if pre_day=='':
				print("Error: get preday fail", i, trade_day)
				break
			#filename = get_path_by_tdate(pre_day)
			#print("%s \n"%(filename))
			tdItem = statisticsItem()
			ret = parse_realtime_fl(trade_day, tdItem)
			if ret == -1:
				trade_day = pre_day
				continue
			
			ysItem = statisticsItem()
			ret = parse_realtime_fl(pre_day, ysItem)
			if ret == -1:
				break

			compare_rt(tdItem, ysItem, q_dict, r_dict)
			trade_day = pre_day
	