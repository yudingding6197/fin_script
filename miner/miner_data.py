#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import datetime
import pandas as pd
import getopt
sys.path.append(".")
sys.path.append("..")
from internal.ts_common import *

#数据挖掘，选择符合的数据

def get_baseline(volume):
	if volume<50:
		return 0
	if volume<100:
		return 50
	v = ((volume+20)/100) * 100
	return v

def handle_res(code, coindf, coinList):
	clm_vol = 'volume'
	amount = coindf.iloc[:,0].size
	if amount==0:
		return
	average = coindf[clm_vol].mean()
	#print amount, average
	#print coindf.head(2)
	fdf = coindf[coindf[clm_vol]>=10]
	amount10 = fdf.iloc[:,0].size
	#成交活跃度和量太低
	if amount10==0:
		return
	avg10 = int(fdf[clm_vol].mean())
	#print amount10, avg10
	if avg10<50:
		return

	volumeList = []
	lastAvg = 0
	matchCt = 0
	#print code
	while 1:
		avg_sec = get_baseline(avg10)
		if lastAvg==avg_sec:
			avg_sec=avg_sec*2
		elif lastAvg>0 and (lastAvg*2+200) < avg_sec:
			matchCt += 1
			if matchCt>1:
				print code, lastAvg, avg_sec, volumeList
				#if matchCt==2:
				#	coinStr = "%s,%8d %8d %s"%(code,lastAvg,avg_sec, ',')
				#	coinList.append(coinStr)
			pass
		#print lastAvg, avg_sec
		volumeList.append(avg_sec)
		nextdf = coindf[coindf[clm_vol]>=avg_sec]
		lastAvg = avg_sec
		#print avg_sec, '=====>', nextdf.iloc[:,0].size
		rowSz = nextdf.iloc[:,0].size
		if rowSz<30:
			#print rowSz
			break
		avg10 = int(nextdf[clm_vol].mean())

	if matchCt>1:
		coinList.append(code +','+ str(volumeList))
	#print volumeList
	return

# Main
param_config = {
	"Date":'',	#
	"LogTP":0	#写日志
}
if __name__=="__main__":
	
	td = ''
	nowToday = datetime.date.today()
	optlist, args = getopt.getopt(sys.argv[1:], '?ld:')
	for option, value in optlist:
		if option in ["-d","--date"]:
			ret,stdate = parseDate(value, nowToday)
			if ret==-1:
				exit()
			param_config['Date'] = stdate
			td = stdate
		elif option in ["-l","--log"]:
			param_config['LogTP'] = 1
		elif option in ["-?","--??"]:
			print "Usage:", os.path.basename(sys.argv[0]), " [-d MMDD/YYYYMMDD]"
			exit()

	if td=='':
		days = 5
		tradeList = []
		get_pre_trade_date(tradeList, days)
		if len(tradeList)!=days:
			print "Fail to get trade date"
			exit()
		td = str(tradeList[0])

	#filterfl = '../data/entry/filter/filter_latest.txt'
	filterfl = '../data/entry/market/latest_stock.txt'

	file = open(filterfl, 'r')
	codeList = []
	line = file.readline()
	while line:
		item = line[0:6]
		codeList.append(item)
		line = file.readline()
	file.close()

	coinList = []
	tpList = []
	folder = '../data/entry/resp/'
	for item in codeList:
		cfolder = folder + item + '/'
		if not os.path.exists(cfolder):
			print cfolder, "Folder Not exist"
			continue
		fname = "%s%s_%s.csv" %(cfolder, item, td)
		if not os.path.exists(fname):
			#print fname, "File Not exist"
			tpList.append(item)
			continue
		coindf = pd.read_csv(fname)
		handle_res(item, coindf, coinList)

	if param_config['LogTP']==1:
		fpath = '../data/entry/filter/no_td_' +td+ '.log'
		file = open(fpath, 'w')
		for item in tpList:
			file.write(item+'\n')
		file.close()

	print "Mine " +td+ " ============\n"
	fpath = '../data/entry/filter/mine_coin_' + td + '.log'
	file = open(fpath, 'w')
	for item in coinList:
		#print item
		file.write(item+'\n')
	file.close()
	print 'FIN MINER'
