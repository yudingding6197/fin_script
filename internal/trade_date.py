#!/usr/bin/env python
# -*- coding:utf8 -*-
import os
import sys
import datetime

sys.path.append(".")
from internal.url_sina.fetch_sina import *
from internal.url_163.service_163 import *
from internal.format_parse import *
import internal.update_tday_db as upday

DB_PATH = 'internal/db'
filenm = 'sh000001'
g_trade_list = []
g_trade_flag = 0

def read_preday_csv(days, cur_day):
	pre_day = ''
	bFlag = 0
	location = DB_PATH + '/' + filenm + '.csv'
	fl = open(location, 'r')
	#排除第一行
	line = fl.readline()
	line = fl.readline()
	curDt = datetime.datetime.strptime(cur_day, '%Y-%m-%d').date()
	if line=='':
		print ("No data")
		bFlag = 1
	else:
		fileDt = datetime.datetime.strptime(line[:10], '%Y-%m-%d').date()
		if (curDt-fileDt).days > 0:
			bFlag = 1

	flag = 0
	#数据库不是最新的，需要更新
	if bFlag==1:
		#print("Update trade day DB");
		fl.close()
		if upday.update_latest_trade(cur_day)==-1:
			return ''
		#如果在交易时段，交易当天日期没有写入文件中，文件最新日期和当天交易日期不匹配
		fl = open(location, 'r')
		
		line = fl.readline()
		line = fl.readline()
		filedate2 = datetime.datetime.strptime(line[:10], '%Y-%m-%d').date()
		#当天还在交易时段，日期没有写入文件中
		if (curDt-filedate2).days > 0:
			flag=1

	#print 'cur date', curDt
	count = 0
	while line:
		file_day = line.split(',')[0]
		if flag==0:
			if file_day==cur_day:
				flag = 1
			else:
				#因为日期可能为非交易日，在数据库中查询不到，定位到该非交易日最近一天的交易日
				fileDt = datetime.datetime.strptime(file_day, '%Y-%m-%d').date()
				if (fileDt-curDt).days<=0:
					flag = 1
		else:
			if count+1==days:
				pre_day = file_day	
				break
			count += 1
		line = fl.readline()
	return pre_day

#解析json文件，指定日期存在就不在更新，指定日期不存在就更新
def read_preday_json(days, cur_day):
	pre_day = ''
	bFlag = 0
	location = DB_PATH + '/' + filenm + '_json.txt'
	if os.path.exists(location) is False:
		get_index_history_byNetease_js(location, filenm)
	# internal/db/sh000001_json.txt
	fl = open(location, 'r')
	try:
		data = json.load(fl)
	except:
		#处理异常：有文件，内容非json格式
		fl.close()
		print "Error: fail to load trade json object"
		get_index_history_byNetease_js(location, filenm)
		fl = open(location, 'r')
		data = json.load(fl)
	fl.close()

	#数据没法通过json.load()直接转为dict对象。通过json.load()二次转化
	info = json.loads(data)
	ret, js_date = parseDate2(info['times'][-1])
	curDt = datetime.datetime.strptime(cur_day, '%Y-%m-%d').date()
	jsDt = datetime.datetime.strptime(js_date, '%Y-%m-%d').date()
	#print "trde_dt taildt=%s jsdt=%s c_d=%s"%(info['times'][-1], js_date, cur_day)

	start_date = cur_day
	#如果json文件的最后一天比需要查询的还早，说明需要更新json
	if (curDt-jsDt).days>0:
		get_index_history_byNetease_js(location, filenm)
		fl = open(location, 'r')
		data = json.load(fl)
		fl.close()
		
		#数据没法通过json.load()直接转为dict对象。通过json.load()二次转化
		info = json.loads(data)
		ret, js_date = parseDate2(info['times'][-1])
		jsDt2 = datetime.datetime.strptime(js_date, '%Y-%m-%d').date()
		if (curDt-jsDt2).days>0:
			#print "Warning:Force append dt",cur_day,js_date
			info['times'].append(cur_day)
		else:
			start_date = js_date

	#先找到指定日期的index
	dayCount = len(info['times'])
	pos = dayCount-1
	while pos>= 0:
		ret, js_cur_date = parseDate2(info['times'][pos])
		#print "Find ",pos, js_cur_date
		if start_date==js_cur_date:
			break
		else:
			jsCurDt = datetime.datetime.strptime(js_cur_date, '%Y-%m-%d').date()
			if (curDt-jsCurDt).days>0:
				break
		pos -= 1

	#开始推算前N天的日期
	pos -= 1
	while days>0:
		ret, js_cur_date = parseDate2(info['times'][pos])
		#print "22",pos, js_cur_date
		pos -= 1
		days -= 1

	#print days, js_cur_date
	return js_cur_date

def get_preday(days=1, cur_day='', method=1):
	pre_day = ''
	if cur_day=='':
		cur_day = get_lastday()
	if days==0:
		return cur_day

	if method==1:
		pre_day = read_preday_json(days, cur_day)
	if method==2:
		pre_day = read_preday_csv(days, cur_day)
	return pre_day

def get_lastday(src='sina'):
	value = ''
	if src=='sina':
		#print "ge_last sn date", src
		value = get_sina_lastday()
	elif src=='163':
		value = get_163_lastday()
	elif src=='qq':
		value = get_qq_lastday()
	#print(value)
	return value

#从文件读取所有的交易日，提供查询判断的基准
#初始化之前，必须更新使用最新的数据
def init_trade_list(cur_day='', method=1):
	global g_trade_flag
	global g_trade_list
	if g_trade_flag==1:
		return

	if cur_day=='':
		cur_day = get_lastday()

	if method==1:
		location = DB_PATH + '/' + filenm + '_json.txt'
		fl = open(location, 'r')
		info = json.loads(json.load(fl))
		fl.close()

		dLists = info["times"]
		pos = len(dLists)-1
		while pos>=0:
			ret, cur_date = parseDate2(dLists[pos])
			g_trade_list.append(cur_date)
			pos -= 1
		g_trade_flag = 1

	elif method==2:
		location = DB_PATH + '/' + filenm + '.csv'
		fl = open(location, 'r')
		#排除第一行
		line = fl.readline()
		line = fl.readline()
		#print cur_day, line[:10]
		g_trade_list.append(cur_day)
		
		#存在，则赋值后再读一行
		if cur_day==line[:10]:
			line = fl.readline()	
		while line:
			if cur_day==line[:10]:
				print("Error: invalid date", cur_day)
				g_trade_flag = 0
				g_trade_list = []
				fl.close()
				return
			g_trade_list.append(line[:10])
			line = fl.readline()
		fl.close()
		g_trade_flag = 1

def release_trade_list():
	global g_trade_flag
	global g_trade_list
	g_trade_flag=0
	g_trade_list=[]

def calcu_back_date(days, base_date):
	if len(g_trade_list)==0:
		print "Not initial date DB"
		return ""

	index = 0
	flag = 0
	for index,item in enumerate(g_trade_list):
		if item==base_date:
			flag = 1
			break
	if flag==0:
		print ("Not find base date", base_date)
		return ""
	if index<days:
		print ("days exceed range", days, index)
		return ""

	item =  g_trade_list[:(index)][-days]
	#print "find_date",item
	return item

def calcu_pre_date(days, base_date):
	trdLen = len(g_trade_list)
	if trdLen==0:
		print "Not initial date DB"
		return ""

	index = 0
	flag = 0
	for index,item in enumerate(g_trade_list):
		if item==base_date:
			flag = 1
			break
	#print 'pre idx', index, base_date
	if flag==0:
		print ("Not find base date", base_date)
		return ""
	if (trdLen-index)<days:
		print ("days exceed range", days, index)
		return ""

	item = g_trade_list[index:][days]
	#print "find_date",item
	return item

def is_trade_date(verifyDate):
	if g_trade_flag==0:
		print("Error: initial global trade DB")
		return False

	if verifyDate in g_trade_list:
		return True
	return False

#Main
#for i in range(0,1000):
#	formatRand()
if __name__ == "__main__":
	init_trade_list()
	dt = '2020-06-24'
	print calcu_back_date(2, dt)
	dt = calcu_pre_date(3, dt)
	print dt

	pass