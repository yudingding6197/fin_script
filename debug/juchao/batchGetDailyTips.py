#!/usr/bin/env python
# -*- coding:gbk -*-

#保存每日的交易信息
import sys
import re
import os
import datetime
import platform
import shutil
import getopt

sys.path.append('.')
from internal.format_parse import *
from internal.url_juchao.trade_info import *

def handle_argument():
	optlist, args = getopt.getopt(sys.argv[1:], 'hd:s:e:')
	for option, value in optlist:
		if option in ["-h","--help"]:
			param_config["Help"] = 1
		elif option in ["-s","--start"]:
			param_config["Start"] = value
		elif option in ["-e","--end"]:
			param_config["End"] = value
		elif option in ["-c","--dfcf"]:
			param_config["DFCF"] = 1
	#print param_config

param_config = {
	"Help":0,
	"Start":'',
	"End":'',
	"DFCF":0,
}
REAL_PRE_FD = "../data/entry/juchao/"

#Main Start:
if __name__=='__main__':
	handle_argument()
	if param_config["Help"]==1:
		print("%s -s([.][YYYY]MMDD) -e([.][([YYYY]MMDD)])"%(os.path.basename(__file__)))
		exit(0)

	cur=datetime.datetime.now()
	cdate = '%04d-%02d-%02d' %(cur.year, cur.month, cur.day)
	#print cdate
	if param_config["Start"]=='.':
		param_config["Start"] = cdate
		param_config["End"] = param_config["Start"]
	else:
		if param_config["End"]=='':
			param_config["End"] = cdate
		elif param_config["End"]=='.':
			param_config["End"] = param_config["Start"]

	ret, sdate = parseDate2(param_config["Start"])
	if ret==-1:
		exit(0)
	ret, edate = parseDate2(param_config["End"])
	if ret==-1:
		exit(0)
	
	startDt = datetime.datetime.strptime(sdate, '%Y-%m-%d').date()
	endDt = datetime.datetime.strptime(edate, '%Y-%m-%d').date()
	while startDt<=endDt:
		date_str = startDt.strftime('%Y-%m-%d')
		#print(date_str)
		startDt += datetime.timedelta(days=1)
		year = date_str[:4]
		fn = REAL_PRE_FD + year + "/jc" + date_str + ".txt"
		
		if os.path.exists(fn):
			continue

		file = open(fn, "w")
		get_trade_tips(date_str, file)
		file.close()
	print("END")