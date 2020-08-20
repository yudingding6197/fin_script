#!/usr/bin/env python
# -*- coding:gbk -*-

#提取juchao每日交易tips
#分析ST变更的时间节点，溯源得到当时交易日的真正名称
#才能处理ST,退市,和对应涨幅
#打开手工生成的'日期xd.txt'文件，通过tips更新有名称变化的个股，确定当时的名称
#另存为'日期up_nm.txt'文件

import sys
import re
import os
import datetime
#import platform
import json
import getopt

sys.path.append('.')
from internal.format_parse import *
from internal.trade_date import *
from internal.math_common import *
from internal.inf_juchao.parse_jc_tips import *

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
						#print key, json.dumps(d_stk, ensure_ascii=False).encode('gbk')
						#print "Add 32", item[1], data[2]
						item[1] = data[2]
		elif data[0]=="Rem":
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
		elif data[0]=="TuS":
			#print "Handle Tus", data[2]
			item[1] = data[2]

	#for key,value in st_name_dict.items():
	#	print key, json.dumps(value, ensure_ascii=False).encode('gbk')

def handle_argument():
	optlist, args = getopt.getopt(sys.argv[1:], 'hd:')
	for option, value in optlist:
		if option in ["-h","--help"]:
			param_config["Help"] = 1
		elif option in ["-d","--date"]:
			param_config["Date"] = value
	#print param_config

param_config = {
	"Help":0,
	"Date":'',
}

#Main Start:
if __name__=='__main__':
	beginTm = datetime.datetime.now()
	
	handle_argument()
	if param_config["Help"]==1 or param_config["Date"]=='':
		print("%s -d([.][YYYY]MMDD))"%(os.path.basename(__file__)))
		exit(0)

	fmt = '%04d-%02d-%02d'
	trade_date = get_lastday()
	pre_date = get_preday(1, trade_date)
	endDt = datetime.datetime.strptime(pre_date, '%Y-%m-%d').date()

	ret, his_date = parseDate2(param_config["Date"])
	if ret==-1:
		exit(0)

	st_name_list = []
	st_name_dict = {}
	stepDt = datetime.datetime.strptime(his_date, '%Y-%m-%d').date()
	#解析从指定日期起，到如今，所有的tips，提取每天ST变更公告，得到变化的个股
	while (endDt-stepDt).days>=0:
		base_date = fmt %(stepDt.year, stepDt.month, stepDt.day)
		read_st_in_daily_tips(base_date, st_name_list, st_name_dict)
		stepDt += datetime.timedelta(days=1)

	flname = '../data/daily/' + his_date +"/"+ his_date + "xd.txt"
	hisFile = open(flname, "r")
	his_list = json.load(hisFile, encoding='gbk')
	hisFile.close()

	#for key,value in st_name_dict.items():
	#	if key=='002509':
	#		print key, json.dumps(value, ensure_ascii=False).encode('gbk')
	#	print key, json.dumps(value, ensure_ascii=False).encode('gbk')
	handle_his_name(his_list, st_name_list, st_name_dict)

	updPath = '../data/daily/' + his_date +"/"+ his_date + "up_nm.txt"
	#更新文件名称
	updFile = open(updPath, "w")
	fmt=1
	if fmt==0:
		updFile.write(json.dumps(his_list, ensure_ascii=False, indent=4).encode('gbk'))
	else:
		updFile.write ("[")
		for i in range(len(his_list)):
			if i==len(his_list)-1:
				updFile.write(json.dumps(his_list[i], ensure_ascii=False).encode('gbk')+"\n")
			else:
				updFile.write(json.dumps(his_list[i], ensure_ascii=False).encode('gbk')+",\n")
		updFile.write ("]")
	updFile.close()

	#校验数据，ST涨幅5%以内，普通的10%
	updFile = open(updPath, "r")
	hisLists = json.load(updFile, encoding='gbk')
	updFile.close()
	for item in hisLists:
		#print item[0],item[1],item[3]
		mrk_date = item[2]
		preClose = item[3]
		open1 = item[4]
		close = item[5]
		high = item[6]
		low = item[7]
		if mrk_date == his_date:
			continue
		if isinstance(preClose, float) is False:
			print "Error data", item[0], item[1]
		elif preClose<=0:
			print "Error data preClose", item[0], item[1], preClose

		if item[1].find("ST")>=0:
			#print item[0],item[1]
			zt_price1 = preClose * 1.05
			dt_price1 = preClose * 0.95
		else:
			zt_price1 = preClose * 1.1
			dt_price1 = preClose * 0.9
		zt_price = spc_round2(zt_price1,2)
		dt_price = spc_round2(dt_price1,2)
		if high>zt_price:
			print "Error data, hig", item[0], item[1],high, zt_price
		if low<dt_price:
			print "Error data, low", item[0], item[1],low, dt_price
		if high<low or close>high or close<low or open1>high or open1<low:
			print "Error data, other", item[0], item[1], open1, close, high, low

	endTm = datetime.datetime.now()
	print "END ", (endTm-beginTm)
