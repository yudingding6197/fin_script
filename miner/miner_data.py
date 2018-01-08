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
			#if matchCt>1:
			#	print code, lastAvg, avg_sec, volumeList
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

	sellStr='卖盘'
	buyStr='买盘'
	
	if matchCt>1:
		coinList.append(code +','+ str(volumeList))

	if param_config['Code']!='' or param_config['File']==1:
		print code, str(volumeList)
		filterDf = coindf[coindf[clm_vol]>=0]
		i = 0
		for vol in volumeList:
			filterDf = filterDf[filterDf[clm_vol]>=vol]
			sellDf = filterDf[filterDf['type']==sellStr]
			sellSz = sellDf.iloc[:,0].size
			buyDf = filterDf[filterDf['type']==buyStr]
			buySz = buyDf.iloc[:,0].size
			
			if vol!=volumeList[-1]:
				vol1 = volumeList[i+1]
				filterDf1 = filterDf[filterDf[clm_vol]<=vol1]
				sellDf = filterDf1[filterDf1['type']==sellStr]
				sellSz1 = sellDf.iloc[:,0].size
				buyDf = filterDf1[filterDf1['type']==buyStr]
				buySz1 = buyDf.iloc[:,0].size
				msg = "%6s (%7d) %7d %7d -- %7d %7d" % (vol, (buySz+sellSz), buySz, sellSz, buySz1, sellSz1)
			else:
				msg = "%6s (%7d) %7d %7d" % (vol, (buySz+sellSz), buySz, sellSz)
			print msg
			i += 1
		return

	arrLen = len(volumeList)
	if arrLen<=2:
		return

	vol1 = volumeList[-1]
	vol = volumeList[-1]
	filterDf = coindf[coindf[clm_vol]>=vol]
	#print code, vol, len(filterDf)
	sellDf = filterDf[filterDf['type']==sellStr]
	sellSz = sellDf.iloc[:,0].size
	buyDf = filterDf[filterDf['type']==buyStr]
	buySz = buyDf.iloc[:,0].size

	if sellSz*3>buySz:
		return
	msg1 = code, len(filterDf), buySz, sellSz, str(volumeList)
	
	vol2 = volumeList[-2]
	vol = volumeList[-2]
	filterDf = coindf[coindf[clm_vol]>=vol]
	#print code, vol, len(filterDf)
	sellStr='卖盘'
	buyStr='买盘'
	sellDf = filterDf[filterDf['type']==sellStr]
	sellSz = sellDf.iloc[:,0].size
	buyDf = filterDf[filterDf['type']==buyStr]
	buySz = buyDf.iloc[:,0].size
	if sellSz*3>buySz:
		return

	vol3=volumeList[-3]
	msg2 = '      ', len(filterDf), buySz, sellSz

	if vol2*2<=vol1 and vol3*2<=vol2:
		print msg1
		print msg2
	#print code, len(filterDf), sellSz, buySz

	#print filterDf
	#exit()
	#print volumeList
	return

# Main
param_config = {
	"Date":'',	#
	"Code":'',	#
	"File":0,	#
	"LogTP":0	#写日志
}
if __name__=="__main__":
	if 0:
		lst=[1]
		print lst[-2]
		exit()

	td = ''
	nowToday = datetime.date.today()
	optlist, args = getopt.getopt(sys.argv[1:], '?lfd:c:')
	for option, value in optlist:
		if option in ["-d","--date"]:
			ret,stdate = parseDate(value, nowToday)
			if ret==-1:
				exit()
			param_config['Date'] = stdate
			td = stdate
		elif option in ["-l","--log"]:
			param_config['LogTP'] = 1
		elif option in ["-c","--code"]:
			param_config['Code'] = value
		elif option in ["-f","--file"]:
			param_config['File'] = 1
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

	codeList = []
	code = param_config['Code']
	if code!='':
		codeList.append(code)
	elif param_config['File']==1:
		filterfl = '../data/entry/miner/filter.txt'
		file = open(filterfl, 'r')
		line = file.readline()
		while line:
			if len(line)>=6:
				item = line[0:6]
				codeList.append(item)
			line = file.readline()
		file.close()
	else:
		file = open(filterfl, 'r')
		line = file.readline()
		while line:
			if len(line)>=6:
				item = line[0:6]
				codeList.append(item)
			line = file.readline()
		file.close()

	print "Mine " +td+ " start ......\n"
	coinList = []
	tpList = []
	folder = '../data/entry/resp/'
	for item in codeList:
		#print item
		if len(item)<6:
			continue
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
