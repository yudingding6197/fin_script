#!/usr/bin/env python
# -*- coding:gbk -*-

#根据code获取对应指定年的日K
#保存为kday_...文件，或者通过 json格式存储
import sys
import re
import os
import json
import getopt

sys.path.append('.')
from internal.handle_realtime import *
from internal.url_163.kline_163 import *

def handle_kline(dayInfo, kFile):
	dict = json.loads(dayInfo)
	for item in dict['data']:
		nlist = map(lambda x:str(x), item)
		value = ','.join(nlist)
		kFile.write(value + "\n")
	return

def handle_argument():
	optlist, args = getopt.getopt(sys.argv[1:], 'y:f:')
	for option, value in optlist:
		if option in ["-y","--year"]:
			param_config["Year"] = value
		elif option in ["-f","--format"]:
			param_config["Format"] = value
	#print param_config

param_config = {
	"Year":'',
	"Format":'json',
}
REAL_DAILY_PRE_FD = "../data/daily/"

#Main Start:
if __name__=='__main__':
	handle_argument()
	if param_config["Year"]=='':
		print "Error:Must add arg -yYYYY"
		exit(0)
	beginTm = datetime.datetime.now()
	year = param_config["Year"]
	#get_all_stk_info() 进行日期处理，获取最新交易日期
	tradeFl = REAL_DAILY_PRE_FD + year + '/' + "_trade_" + year + ".txt"

	file = open(tradeFl, "r")
	line = file.readline()
	flag = 1
	while line:
		#print line
		if len(line)<10:
			line = file.readline()
			continue
		elif line[0]=="#":
			line = file.readline()
			continue

		obj = line.split(',')
		#if obj[0] == '600145':
		#	flag = 1
		if flag == 0:
			line = file.readline()
			continue
	
		bExist = 0
		if param_config["Format"]=='':
			kFl = REAL_DAILY_PRE_FD + year + '/' + 'kday_' + obj[0] + ".txt"
			if os.path.exists(kFl):
				bExist = 1
		elif param_config["Format"]=='json':
			kFl = REAL_DAILY_PRE_FD + year + '/json/' + 'j' + obj[0] + ".txt"
			#print kFl
			if os.path.exists(kFl):
				bExist = 1
		else:
			print "Error: unsupport format", param_config["Format"]
			break

		if bExist==1:
			line = file.readline()
			continue

		#print "obj", obj[0]
		dayLine = get_kday_163(obj[0], year)
		if dayLine is None:
			print ("Get %s fail, tingpai???" % (obj[0]))
			line = file.readline()
			continue

		kFile = open(kFl, "w")
		if param_config["Format"]=='':
			handle_kline(dayLine, kFile)
		elif param_config["Format"]=='json':
			obj = json.loads(dayLine)
			json.dump(obj['data'], kFile)
		kFile.close()

		line = file.readline()
	file.close()
