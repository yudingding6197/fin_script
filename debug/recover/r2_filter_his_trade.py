#!/usr/bin/env python
# -*- coding:gbk -*-

#保存每日的交易信息
import sys
import re
import os
import time
import string
import datetime
import platform
import getopt

sys.path.append('.')
from internal.handle_realtime import *

PRE_DAYS = 33
CX_DAYS = 200

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
REAL_PRE_FD = "../data/daily/"

#Main Start:
if __name__=='__main__':
	beginTm = datetime.datetime.now()
	
	handle_argument()
	if param_config["Date"]=='':
		print "Error:Must add arg -dYYYY-MM-DD option"
		exit(0)
	ret, def_dt = parseDate2(param_config["Date"])
	if ret==-1:
		exit(0)
	
	#get_all_stk_info() 进行日期处理，获取最新交易日期
	#trade_date = get_lastday()
	flname = REAL_PRE_FD + "dailydb_19base.txt"
	tradefl = REAL_PRE_FD + def_dt[:4] + '/' + "trade_" + def_dt + ".txt"
	
	defDt = datetime.datetime.strptime(def_dt, '%Y-%m-%d').date()
	pre30_date = get_preday(PRE_DAYS, def_dt)
	pre300_date = get_preday(CX_DAYS, def_dt)
	print "dt, pre30, pre300", defDt, pre30_date, pre300_date

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
