#!/usr/bin/env python
# -*- coding:utf8 -*-
import os
import sys
import datetime
from shutil import copyfile

sys.path.append(".")
from internal.url_sina.fetch_sina import *
from internal.url_163.service_163 import *
from internal.url_163.fetch_163 import *
from internal.url_tecent.fetch_tecent import *
from internal.format_parse import *
import internal.update_tday_db as upday

DB_PATH = 'internal/db'
#g_filenm = 'sh000001'
g_filenm = 'sh000001_2'
g_trade_list = []
g_trade_flag = 0

g_filenm_qq = 'sh000001'

def read_preday_csv(days, cur_day):
	pre_day = ''
	bFlag = 0
	location = DB_PATH + '/' + g_filenm + '.csv'
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
#通常，通过sina获取最新的交易日期，再从wy解析json后得到最新日期，
#如果sina和wy的不匹配，说明需要获取最新的json文件
def read_preday_json(days, cur_day):
	pre_day = ''
	bFlag = 0
	location = DB_PATH + '/' + g_filenm + '_json.txt'
	if os.path.exists(location) is False:
		get_index_history_byNetease_js(location, g_filenm)
	# internal/db/sh000001_json.txt
	fl = open(location, 'r')
	try:
		data = json.load(fl)
	except:
		#处理异常：有文件，内容非json格式
		fl.close()
		print "Error: fail to load trade json object"
		get_index_history_byNetease_js(location, g_filenm)
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
		get_index_history_byNetease_js(location, g_filenm)
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

#先判断最新的json文件是否存在，不存在先下载
def read_preday_json2(days, cur_day):
	pre_day = ''
	bFlag = 0
	location = DB_PATH + '/' + g_filenm + '_json.txt'
	if os.path.exists(location) is False:
		get_index_history_byNetease_js2(location, g_filenm)
	# internal/db/sh000001_json.txt
	info = None
	fl = open(location, 'r')
	try:
		info = json.load(fl)
	except:
		#处理异常：有文件，内容非json格式
		fl.close()
		print "Error: fail to load trade json object"
		get_index_history_byNetease_js2(location, g_filenm)
		fl = open(location, 'r')
		info = json.load(fl)
	fl.close()
	if info is None:
		print("WY: Fail get file")
		return None
	elif len(info)==0:
		print("WY: data is Empty")
		#exit(0)
		return None

	#从json文件读出最新日期转为jsDt，和当前日期做对比
	js_date = info[0]
	curDt = datetime.datetime.strptime(cur_day, '%Y-%m-%d').date()
	jsDt = datetime.datetime.strptime(js_date, '%Y-%m-%d').date()
	#print "trde_dt taildt=%s jsdt=%s c_d=%s"%(info[0], js_date, cur_day)

	start_date = cur_day
	#如果json文件的最后一天比需要查询的还早，说明需要更新json
	if (curDt-jsDt).days>0:
		get_index_history_byNetease_js2(location, g_filenm)
		fl = open(location, 'r')
		data = json.load(fl)
		fl.close()
		
		info = data
		js_date = info[0]
		jsDt2 = datetime.datetime.strptime(js_date, '%Y-%m-%d').date()
		if (curDt-jsDt2).days>0:
			#print "Warning:Force append dt",cur_day,js_date
			info.insert(0, cur_day)
		else:
			start_date = js_date

	#先找到指定日期的index
	dayCount = len(info)
	pos = 0
	while pos<dayCount:
		js_cur_date = info[pos]
		#print "Find ---",pos, js_cur_date
		if start_date==js_cur_date:
			break
		else:
			jsCurDt = datetime.datetime.strptime(js_cur_date, '%Y-%m-%d').date()
			if (curDt-jsCurDt).days>0:
				break
		pos += 1

	#print "tradt read json1",days, pos, start_date, js_cur_date
	#开始推算前N天的日期
	pos += 1
	tDays = days
	while tDays>0:
		#print "tradt read json2",tDays, pos, js_cur_date
		js_cur_date = info[pos]
		pos += 1
		tDays -= 1

	#print("Read2", days, js_cur_date, cur_day)
	return js_cur_date

def get_preday(days=1, cur_day='', method=1):
	pre_day = ''
	if cur_day=='':
		cur_day = get_lastday()
	if days==0:
		return cur_day

	#print ("_____ Get lastDay ",days, cur_day, method)
	if method==1:
		pre_day = read_preday_json2(days, cur_day)
	if method==2:
		pre_day = read_preday_csv(days, cur_day)
	return pre_day

#仅仅从这几家网站获取最新的交易日期，如最新上证指数，没有其它的操作
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

'''
#从当前json或者csv文件中读取所有当前交易日
#初始化之前，必须确保更新使用最新的日期，否则最新日期可能不存在导致问题
#初始化之后，通过release_trade_list()释放
#method: 1.打开json格式的文件
         2.打开csv格式
'''
def init_trade_list(cur_day='', method=1):
	global g_trade_flag
	global g_trade_list
	if g_trade_flag==1:
		return

	if cur_day=='':
		cur_day = get_lastday()

	if method==1:
		location = DB_PATH + '/' + g_filenm + '_json.txt'
		fl = open(location, 'r')
		'''
		info = json.loads(json.load(fl))
		fl.close()

		dLists = info["times"]
		pos = len(dLists)-1
		while pos>=0:
			ret, cur_date = parseDate2(dLists[pos])
			g_trade_list.append(cur_date)
			pos -= 1
		'''
		info = json.load(fl)
		fl.close()
		
		#判断当天是否加上，交易时段不会有，需要加上
		ret, cur_date = parseDate2(cur_day)
		if cur_date!=info[0]:
			info.insert(0, cur_date)		

		g_trade_list = info
		g_trade_flag = 1

	elif method==2:
		location = DB_PATH + '/' + g_filenm + '.csv'
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
		print ("days1 exceed range", days, index)
		return ""

	if days==0:
		return base_date
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
		print ("days2 exceed range", days, index)
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

def read_preday_QQ_json(days, cur_day):
	pre_day = ''
	bFlag = 0
	location = DB_PATH + '/' + g_filenm_qq + '_qq.txt'
	if os.path.exists(location) is False:
		get_tecent_kline_day(location, g_filenm_qq)

	info = None
	fl = open(location, 'r')
	try:
		info = json.load(fl)
	except:
		#处理异常：有文件，内容非json格式
		fl.close()
		print "Error: fail to load trade json object"
		get_tecent_kline_day(location, g_filenm_qq)
		fl = open(location, 'r')
		info = json.load(fl)
	fl.close()
	if info is None:
		print("Fail get file")
		return None

	#从json文件读出最新日期转为jsDt，和当前日期做对比
	js_date = info[0]
	
	curDt = datetime.datetime.strptime(cur_day, '%Y-%m-%d').date()
	jsDt = datetime.datetime.strptime(js_date, '%Y-%m-%d').date()
	#print "trde_dt taildt=%s jsdt=%s c_d=%s"%(info[0], js_date, cur_day)

	start_date = cur_day
	#如果json文件的最后一天比需要查询的还早，说明需要更新json
	if (curDt-jsDt).days>0:
		get_tecent_kline_day(location, g_filenm_qq)
		fl = open(location, 'r')
		data = json.load(fl)
		fl.close()

		info = data
		js_date = info[0]
		jsDt2 = datetime.datetime.strptime(js_date, '%Y-%m-%d').date()
		if (curDt-jsDt2).days>0:
			#print "Warning:Force append dt",cur_day,js_date
			info.insert(0, cur_day)
		else:
			start_date = js_date

	#先找到指定日期的index
	dayCount = len(info)
	pos = 0
	while pos<dayCount:
		js_cur_date = info[pos]
		#print "Find ---",pos, js_cur_date
		if start_date==js_cur_date:
			break
		else:
			jsCurDt = datetime.datetime.strptime(js_cur_date, '%Y-%m-%d').date()
			if (curDt-jsCurDt).days>0:
				break
		pos += 1

	#开始推算前N天的日期
	pos += 1
	tDays = days
	while tDays>0:
		js_cur_date = info[pos]
		#print "calll",pos, js_cur_date
		pos += 1
		tDays -= 1

	#print("Read2", days, js_cur_date, cur_day)
	return js_cur_date

def get_QQ_preday(days=1, cur_day=''):
	#if cur_day=='':
	#	cur_day = get_lastday()
	if days==0:
		return cur_day

	#print ("_____ Get QQ lastDay ",days, cur_day, method)
	pre_QQ_day = read_preday_QQ_json(days, cur_day)
	return pre_QQ_day

def sync163FromQQ():
	src = DB_PATH + '/' + g_filenm_qq + '_qq.txt'
	dest = DB_PATH + '/' + g_filenm + '_json.txt'
	copyfile(src, dest)

#Main
#for i in range(0,1000):
#	formatRand()
if __name__ == "__main__":
	trade_date = get_lastday()
	print "trd_dt", trade_date
	#preDay = read_preday_QQ_json(1,trade_date)
	#print "PPPP", preDay
	#exit(0)
	init_trade_list()
	dt = '2020-06-24'
	print calcu_back_date(2, trade_date)
	#dt = calcu_pre_date(3, dt)
	print dt
	release_trade_list()

	pass