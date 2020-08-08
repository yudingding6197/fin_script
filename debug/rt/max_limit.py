#!/usr/bin/env python
# -*- coding:utf-8 -*-

#涨停分析
import sys
import getopt

sys.path.append(".")
from internal.trade_date import *
from internal.analyze_realtime import *

def handle_argument():
	optlist, args = getopt.getopt(sys.argv[1:], 'g:l:e:d:n:')
	for option, value in optlist:
		if option in ["-g","--greate"]:
			param_config["Greate"] = int(value)
			param_config["Flag"] = 1
			param_config["Days"] = param_config["Greate"]
		elif option in ["-l","--less"]:
			param_config["Less"] = value
			if param_config["Flag"] != 0:
				print("-g -l -e 选项3选一") 
				return -1
			param_config["Flag"] = 2
			param_config["Days"] = param_config["Less"]
		elif option in ["-e","--equal"]:
			param_config["Equal"] = value
			if param_config["Flag"] != 0:
				print("-g -l -e 选项3选一") 
				return -1
			param_config["Flag"] = 3
			param_config["Days"] = param_config["Equal"]
		elif option in ["-d","--date"]:
			param_config["Date"] = value
		elif option in ["-n","--number"]:
			param_config["Number"] = int(value)
	#print param_config
	#默认设置为greate
	if param_config["Flag"]==0:
		param_config["Flag"] = 1
		param_config["Days"] = param_config["Greate"]
	
	return 0

def showContinueZT(curStat, cur_date):
	cDays = param_config["Days"]
	list = []
	for item in curStat.lst_non_yzcx_yzzt:
		value = item[7]
		if param_config["Flag"]==1:
			if value>=cDays:
				list.append(item)
		elif param_config["Flag"]==2:
			if value<=cDays:
				list.append(item)
		elif param_config["Flag"]==3:
			if value==cDays:
				list.append(item)
	for item in curStat.lst_non_yzcx_zt:
		value = item[7]
		if param_config["Flag"]==1:
			if value>=cDays:
				list.append(item)
		elif param_config["Flag"]==2:
			if value<=cDays:
				list.append(item)
		elif param_config["Flag"]==3:
			if value==cDays:
				list.append(item)
	if len(list)>0:
		print ("%s%s"%('\n', cur_date))
		for i in range(len(list)):
			item = list[i]
			print item[0], item[1], item[7]
	
	
param_config = {
	"Greate":8,
	"Less":0,
	"Equal":0,
	"Flag":0,
	"Days":0,
	"Date":'',
	"Number":300,
}

#Main Start:
if __name__=='__main__':
	ret = handle_argument()
	if ret==-1:
		exit(0)
	if param_config['Date']=='':
		cur_day = get_lastday()
	else:
		#必须转为 YYYY-MM-DD格式
		cur_day = param_config['Date']
		if len(cur_day)==8:
			cur_day = cur_day[:4] + '-' + cur_day[4:6] + '-' + cur_day[6:8]
		
		#print cur_day

	number = param_config["Number"]
	count = 0
	for i in range(number):
		#print i, cur_day
		if cur_day=='':
			break
		curStat = statisticsItem()
		ret = parse_realtime_his_file(cur_day, curStat)
		if ret == -1:
			cur_day = get_preday(1, cur_day)
			count += 1
			if count>3:
				break
			continue
		count = 0
		showContinueZT(curStat, cur_day)
		cur_day = get_preday(1, cur_day)
		