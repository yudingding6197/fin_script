#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import datetime
import pandas as pd
#数据挖掘，选择符合的数据

def get_baseline(volume):
	if volume<50:
		return 0
	if volume<100:
		return 50
	v = ((volume+20)/100) * 100
	return v

def handle_res(code, coindf, coinList):
	volumeList = []
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

	volumeList.append(code)
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
				print lastAvg, avg_sec, volumeList
				if matchCt==2:
					coinList.append(code)
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

	#print volumeList
	return

# Main
if __name__=="__main__":
	filterfl = '../data/entry/filter/filter_latest.txt'
	#filterfl = '../data/entry/market/latest_stock.txt'

	file = open(filterfl, 'r')
	codeList = []
	line = file.readline()
	while line:
		item = line[0:6]
		codeList.append(item)
		line = file.readline()

	coinList = []
	folder = '../data/entry/resp/'
	for item in codeList:
		cfolder = folder + item + '/'
		if not os.path.exists(cfolder):
			print cfolder, "Folder Not exist"
			continue
		fname = cfolder + item + '_2018-01-03' + '.csv'
		if not os.path.exists(fname):
			#print fname, "File Not exist"
			continue
		coindf = pd.read_csv(fname)
		handle_res(item, coindf, coinList)

	print "============\n"
	for item in coinList:
		print item
	print 'FIN MINER'
