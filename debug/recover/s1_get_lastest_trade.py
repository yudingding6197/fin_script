#!/usr/bin/env python
# -*- coding:gbk -*-

#从DC获取最新一个交易日的信息，总共4000多Item
#保存到../data/daily/下，知道当时哪些Item正在交易，TuiS的就消失了
import sys
import re
import os
import time
import string
import datetime
import platform
import shutil
import getopt

sys.path.append('.')
from internal.trade_date import *
from internal.handle_realtime import *
from internal.update_tday_db import *

def handle_argument():
	optlist, args = getopt.getopt(sys.argv[1:], 'ldtac')
	for option, value in optlist:
		if option in ["-l","--nolog"]:
			param_config["NoLog"] = 1
		elif option in ["-d","--nodetail"]:
			param_config["NoDetail"] = 1
		elif option in ["-t","--sbtime"]:
			param_config["SortByTime"] = 1
		elif option in ["-a","--all"]:
			param_config["NotAllInfo"] = 1
		elif option in ["-c","--dfcf"]:
			param_config["DFCF"] = 1
	#print param_config

param_config = {
	"NoLog":0,
	"NoDetail":0,
	"SortByTime":0,
	"NotAllInfo":0,
	"DFCF":0,
}
REAL_DAILY_PRE_FD = "../data/daily/"

#Main Start:
if __name__=='__main__':
	beginTm = datetime.datetime.now()
	sysstr = platform.system()
	handle_argument()

	t_fmt = '%d-%02d-%02d %02d:%02d'
	t_fmt1 = '%d-%02d-%02d_%02d-%02d'
	cur_dt_fmt = '%d-%02d-%02d'
	fmt_time = t_fmt %(beginTm.year, beginTm.month, beginTm.day, beginTm.hour, beginTm.minute)
	fmt_time1 = t_fmt1 %(beginTm.year, beginTm.month, beginTm.day, beginTm.hour, beginTm.minute)
	today_date = cur_dt_fmt %(beginTm.year, beginTm.month, beginTm.day)
	
	#get_all_stk_info() 进行日期处理，获取最新交易日期
	trade_date = get_lastday()
	flname = REAL_DAILY_PRE_FD + "dailydb_" + fmt_time1 + ".txt"
	print "TIME:",today_date, trade_date, flname

	#通过条件查询所有STK, start from 000001
	st_list = []
	ret = get_stk_code_by_dfcf(st_list, 'A', 0)
	if ret==-1:
		exit(0)
	file = open(flname, "w")
	for item in st_list:
		test_str = ",".join(item)
		test_str += "\n"
		file.write(test_str.encode('gbk'))
	file.close()
	
	endTm = datetime.datetime.now()
	print "END ", (endTm-beginTm)
