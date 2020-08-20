#!/usr/bin/env python
# -*- coding:gbk -*-

#解析个股添加或者取消ST处理消息
import sys
import re
import os
import datetime
import platform
import shutil
import getopt

sys.path.append('.')
from internal.format_parse import *
from internal.parse_jc_tips import *

def handle_argument():
	optlist, args = getopt.getopt(sys.argv[1:], 'hd:s:e:')
	for option, value in optlist:
		if option in ["-h","--help"]:
			param_config["Help"] = 1
		elif option in ["-d","--date"]:
			param_config["Date"] = value
		elif option in ["-e","--end"]:
			param_config["End"] = value
	#print param_config

param_config = {
	"Help":0,
	"Date":'',
	"End":'',
	"DFCF":0,
}

#Main Start:
if __name__=='__main__':
	handle_argument()
	if param_config["Help"]==1:
		print("%s -s([.][YYYY]MMDD) -e([.][([YYYY]MMDD)])"%(os.path.basename(__file__)))
		exit(0)

	fmt = '%04d-%02d-%02d'
	beginTm = datetime.datetime.now()
	cdate = fmt %(beginTm.year, beginTm.month, beginTm.day)
	endDt = datetime.datetime.strptime(cdate, '%Y-%m-%d').date()

	hisDate = param_config["Date"]
	ret, dt = parseDate2(hisDate)

	stk_list = []
	stk_dict = {}
	stepDt = datetime.datetime.strptime(dt, '%Y-%m-%d').date()
	while (endDt-stepDt).days>=0:
		base_date = fmt %(stepDt.year, stepDt.month, stepDt.day)
		read_st_in_daily_tips(base_date, stk_list, stk_dict)
		stepDt += datetime.timedelta(days=1)

	#print stk_list
	for key,value in stk_dict.items():
		print key, json.dumps(value, ensure_ascii=False).encode('gbk')
	endTm = datetime.datetime.now()
	print "END ", (endTm-beginTm)
