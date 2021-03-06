#!/usr/bin/env python
# -*- coding:gbk -*-

#将期望搜索的文件改名为 _dailydb_new.txt
#From _dailydb_new.txt读取所有个股
#生成 _rt_trade_year.txt文件
#保存为[code, name, 上市日期]格式
import sys
import re
import os
import time
import string
import datetime
#import platform
import getopt

sys.path.append('.')
from internal.handle_realtime import *
from internal.global_var import *

def handle_argument():
	optlist, args = getopt.getopt(sys.argv[1:], 'd:')
	for option, value in optlist:
		if option in ["-d","--date"]:
			param_config["Date"] = value
		elif option in ["-t","--sbtime"]:
			param_config["SortByTime"] = 1
		elif option in ["-a","--all"]:
			param_config["NotAllInfo"] = 1
		elif option in ["-c","--dfcf"]:
			param_config["DFCF"] = 1
	#print param_config

param_config = {
	"Date":'',
	"NoDetail":0,
	"SortByTime":0,
	"NotAllInfo":0,
	"DFCF":0,
}
REAL_DAILY_PRE_FD = "../data/daily/"

#Main Start:
if __name__=='__main__':
	beginTm = datetime.datetime.now()
	
	handle_argument()
	if param_config["Date"]=='':
		print "Error:Must add option -d(YYYY-MM-DD)"
		exit(0)
	ret, def_dt = parseDate2(param_config["Date"])
	if ret==-1:
		exit(0)
	
	flname = REAL_DAILY_PRE_FD + "_dailydb_new.txt"
	tradefl = REAL_DAILY_PRE_FD + def_dt[:4] + '/' + "_rt_trade_" + def_dt + ".txt"
	
	defDt = datetime.datetime.strptime(def_dt, '%Y-%m-%d').date()
	pre30_date = get_preday(PRE_DAYS, def_dt)
	pre300_date = get_preday(CX_DAYS, def_dt)
	print "dt, pre30, pre200", def_dt, pre30_date, pre300_date
	#print pre30_date, pre300_date
	print "Info:Read file", flname, "Is right???"

	fmt = "%s,%s,%s\n"
	tdFile = open(tradefl, "w")
	file = open(flname, "r")
	line = file.readline()
	while line:
		if len(line)<20:
			line = file.readline()
			continue

		obj = line.split(',')		
		mark_dt = obj[len(obj)-1].strip()
		markDt = datetime.datetime.strptime(mark_dt, '%Y-%m-%d').date()
		#print defDt, markDt
		if (defDt-markDt).days<0:
			line = file.readline()
			continue

		line = file.readline()
		
		tdLine = fmt % (obj[1], obj[2], mark_dt)
		tdFile.write(tdLine)
		#print line
	file.close()
	
	#TODO: 增加退市的个股
	tdFile.close()
