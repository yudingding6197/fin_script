#!/usr/bin/env python
# -*- coding:gbk -*-

#提取juchao每日交易tips
#分析ST变更的时间节点，溯源得到当时交易日的真正名称
#才能处理ST,退市,和对应涨幅

import sys
import re
import os
import datetime
import platform
import shutil
import getopt

sys.path.append('.')
from internal.format_parse import *
from internal.parse_juchao import *

def handle_his_name(his_list, st_name_list, st_name_dict):
	for item in his_list:
		if item[0] not in st_name_list:
			continue
		key = item[0]
		d_stk = st_name_dict[key]
		#print type(d_stk)
		#v2 = sorted(d_stk)
		#print key, json.dumps(d_stk, ensure_ascii=False).encode('gbk')
		skey = d_stk.keys()[0]
		data = d_stk[skey]
		#print item[1]
		#print key, json.dumps(data, ensure_ascii=False).encode('gbk')
		if data[0]=="Add":
			if data[1]==1:
				#TODO: 002220
				#print key, json.dumps(d_stk, ensure_ascii=False).encode('gbk')
				#print 111, item[1], data[2]
				#正常情况下原来是带有ST的
				if item[1].find("ST")==-1:
					if data[2].find("ST")>=0:
						item[1] = data[2]
					else:
						print key, json.dumps(d_stk, ensure_ascii=False).encode('gbk')
						print "Check: Add why not ST", item[0], item[1].encode('gbk')
			elif data[1]==2:
				#print key, json.dumps(d_stk, ensure_ascii=False).encode('gbk')
				#print 111-22222, item[1], data[2]
				if item[1].find("ST")>=0:
					if data[2].find("ST")==-1:
						item[1] = data[2]
					else:
						item[1] = data[2][2:]
						#print 111-22222, item[1], data[2]
				if item[1].find("ST")>=0:
					print "Check: Add why not ST", item[0], item[1].encode('gbk')
			elif data[1]==3:
				if item[1].find("ST")>=0:
					if data[2].find("ST")==-1:
						#print item[1], data[2]
						item[1] = data[2]
					else:
						if item[1][:3]=="*ST":
							item[1] = item[1][3:]
						elif item[1][:2]=="ST":
							item[1] = item[1][2:]
						else:
							print key, json.dumps(d_stk, ensure_ascii=False).encode('gbk')
							print "Add 31", item[1], data[2]
				else:
					#可能包含TuiShi名字
					name = item[1]
					if name[:2]==u'退市':
						item[1] = name[2:]
					elif name[-1:]==u'退':
						item[1] = name[:-1]
					else:
						print key, json.dumps(d_stk, ensure_ascii=False).encode('gbk')
						print "Add 32", item[1], data[2]
						item[1] = data[2]
		else:
			#print key, json.dumps(data, ensure_ascii=False).encode('gbk')
			#检查名字是否包含ST，最终名字需要带ST
			if item[1].find("ST")==-1:
				if data[2].find("ST")>=0:
					item[1] = data[2]
				else:
					item[1] = "ST" + data[2][:2]
				#print type(item[1]), type(data[2])
			if item[1].find("ST")==-1:
				print ("Error: not ST", item[0], item[1].encode('gbk'))

	#for key,value in st_name_dict.items():
	#	print key, json.dumps(value, ensure_ascii=False).encode('gbk')

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
REAL_DAILY_PRE_FD = "../data/entry/juchao/"

#Main Start:
if __name__=='__main__':
	handle_argument()
	if param_config["Help"]==1:
		print("%s -d([.][YYYY]MMDD))"%(os.path.basename(__file__)))
		exit(0)

	fmt = '%04d-%02d-%02d'
	beginTm = datetime.datetime.now()
	trade_date = get_lastday()
	pre_date = get_preday(1, trade_date)
	endDt = datetime.datetime.strptime(pre_date, '%Y-%m-%d').date()

	hisDate = param_config["Date"]
	ret, dt = parseDate2(hisDate)

	st_name_list = []
	st_name_dict = {}
	stepDt = datetime.datetime.strptime(dt, '%Y-%m-%d').date()
	while (endDt-stepDt).days>=0:
		base_date = fmt %(stepDt.year, stepDt.month, stepDt.day)
		parse_daily_tips(REAL_DAILY_PRE_FD, base_date, st_name_list, st_name_dict)
		stepDt += datetime.timedelta(days=1)

	flname = '../data/daily/' + dt +"/"+ dt + "xd.txt"
	hisFile = open(flname, "r")
	his_list = json.load(hisFile, encoding='gbk')
	hisFile.close()

	handle_his_name(his_list, st_name_list, st_name_dict)
	#for key,value in stk_dict.items():
	#	print key, json.dumps(value, ensure_ascii=False).encode('gbk')

	endTm = datetime.datetime.now()
	print "END ", (endTm-beginTm)
