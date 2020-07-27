#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import datetime
sys.path.append(".")
from internal.url_sina.fetch_sina import *
import internal.update_tday_db as upday

DB_PATH = 'internal/db'
filenm = 'sh000001'
g_trade_list = []
g_trade_flag = 0

def get_preday(days=1, cur_day=''):
	pre_day = ''
	if cur_day=='':
		cur_day = get_lastday()

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
		print("Update trade day DB");
		fl.close()
		upday.update_latest_trade(cur_day)
		#如果在交易时段，交易当天日期没有写入文件中，文件最新日期和当天交易日期不匹配
		fl = open(location, 'r')
		
		line = fl.readline()
		line = fl.readline()
		filedate2 = datetime.datetime.strptime(line[:10], '%Y-%m-%d').date()
		#当天还在交易时段，日期没有写入文件中
		if (curDt-filedate2).days > 0:
			flag=1

	count = 0
	while line:
		file_day = line.split(',')[0]
		if flag==0:
			if file_day==cur_day:
				flag = 1
		else:
			if count+1==days:
				pre_day = file_day	
				break
			count += 1
		line = fl.readline()
	return pre_day

def get_lastday(src='sina'):
	value = ''
	if src=='sina':
		value = get_sina_lastday()
	elif src=='163':
		value = get_163_lastday()
	elif src=='qq':
		value = get_qq_lastday()
	#print(value)
	return value

def init_trade_list(cur_day=''):
	global g_trade_flag
	global g_trade_list
	if g_trade_flag==1:
		return

	if cur_day=='':
		cur_day = get_lastday()

	location = DB_PATH + '/' + filenm + '.csv'
	fl = open(location, 'r')
	#排除第一行
	line = fl.readline()
	line = fl.readline()
	print cur_day, line[:10]
	g_trade_list.append(cur_day)
	
	#存在，则赋值后再读一行
	if cur_day==line[:10]:
		line = fl.readline()	
	while line:
		if cur_day==line[:10]:
			print("Error: invalid date", cur_day)
			g_trade_flag = 0
			g_trade_list = []
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

def calcu_back_date(base_date, days):
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
		print ("days too long", days, index)
		return ""

	item =  g_trade_list[:(index)][-days]
	#print "find_date",item
	return item

#Main
#for i in range(0,1000):
#	formatRand()
if __name__ == "__main__":
	init_trade_list()
	dt = '2020-06-24'
	calcu_back_date(dt, 2)

	pass