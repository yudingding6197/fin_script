#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import os
import datetime
import json
import getopt
import codecs

from internal.trade_date import *
from internal.url_dfcf.dc_hq_push import *

def cmp_gn_bk(cmpList, bk_id):
	cmpLen = len(cmpList)
	for idx in range(0, cmpLen):
		if cmpList[idx]['f12']!=bk_id:
			continue
		#print idx, cmpList[idx]
		cmpList.pop(idx)
		break
	#print len(cmpList)
	return

def check_quit_bk(trade_date):
	cmp_date='2021-08-05'
	cmp_fp='../data/entry/gainian/' + cmp_date[0:4] + '/gnbk_' + cmp_date + '.txt'
	file = open(cmp_fp, 'r')
	cmpObj = json.load(file)
	file.close()
	
	cur_fp='../data/entry/gainian/' + trade_date[0:4] + '/gnbk_' + trade_date + '.txt'
	file = open(cur_fp, 'r')
	curObj = json.load(file)
	file.close()
	
	cmpList = cmpObj['data']['diff']
	for idx in range(0, len(curObj['data']['diff'])):
		#print idx, curObj['data']['diff'][idx]['f12']
		cmp_gn_bk(cmpList, curObj['data']['diff'][idx]['f12'])
	
	print "Left data", len(cmpList)
	for i in range(0, len(cmpList)):
		print cmpList[i]['f12'], cmpList[i]['f14']
	
#Quit 从概念板块中退出的BK
def handle_argument():
	optlist, args = getopt.getopt(sys.argv[1:], 's:e:i:q')
	for option, value in optlist:
		if option in ["-s","--startdate"]:
			param_config["StartDate"] = value
		elif option in ["-e","--enddate"]:
			param_config["EndDate"] = value
		elif option in ["-i","--interval"]:
			param_config["Interval"] = int(value)
		elif option in ["-q","--quit"]:
			param_config["Quit"] = 1
	#print param_config

#Quit 从概念板块中退出的BK
param_config = {
	"StartDate":"",
	"Interval":0,
	"Quit":0,
}

#Main Start:
if __name__=='__main__':
	handle_argument()
	trade_date = get_lastday()
	
	if param_config['Quit']==1:
		check_quit_bk(trade_date)
		exit(0)

	init_trade_list(trade_date)
	
	pre_day = 15
	if param_config["StartDate"]=='' or param_config["StartDate"]=='.':
		if param_config["Interval"]!=0:
			pre_day = param_config["Interval"]
		cmp_date=calcu_pre_date(pre_day, trade_date)
		if cmp_date=='':
			release_trade_list()
			exit(-1)
		#print("Compare base date", cmp_date)
		param_config["StartDate"] = cmp_date
	else:
		ret, sdate = parseDate2(param_config["StartDate"])
		if ret==-1:
			release_trade_list()
			exit(-1)
		cmp_date = sdate

	klObj = None
	cur_kline='../data/entry/gainian/' + trade_date[0:4] + '/gn_kline_' + trade_date + '.txt'
	if not os.path.exists(cur_kline):
		print("File not exist, get via debug/gainian_bk.py")
		release_trade_list()
		exit(-1)
	release_trade_list()

	file = open(cur_kline, 'r')
	klObj = json.load(file)
	klLen = len(klObj)
	file.close()

	cmpDt = datetime.datetime.strptime(cmp_date, '%Y-%m-%d').date()
	for idx in range(0, klLen):
		kl_sdate = klObj[idx]['klines'][0][:10]
		startDt = datetime.datetime.strptime(kl_sdate, '%Y-%m-%d').date()
		
		if (startDt-cmpDt).days<0:
			continue
		print klObj[idx]['klines'][0][:11], klObj[idx]['code'],klObj[idx]['name']
		#print klObj[idx]['klines'][-1][:11]
		#bkList.append(klObj[idx])


	
