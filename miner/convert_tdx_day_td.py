#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import getopt
import datetime
sys.path.append(".")
sys.path.append("..")
from internal.ts_common import *

#读取通过TDX选股得到的某天所有交易数据，判断获得没有交易的item
#解析原始文件 '../data/entry/tdx_history/沪深Ａ股_日期.txt'(通过TDX 34功能生成此文件)
#保存到	'../data/entry/market/stock_日期.txt'
#TODO:如果不加日期，希望能只能判断

if __name__=='__main__':
	td=''
	nowToday = datetime.date.today()
	optlist, args = getopt.getopt(sys.argv[1:], '?d:')
	for option, value in optlist:
		if option in ["-d","--date"]:
			ret,stdate = parseDate(value, nowToday)
			if ret==-1:
				exit()
			td = stdate
		elif option in ["-?","--??"]:
			print "Usage:", os.path.basename(sys.argv[0]), "-d MMDD/YYYYMMDD"
			exit()

	if td=='':
		print "Usage:", os.path.basename(sys.argv[0]), "-d MMDD/YYYYMMDD"
		exit()
	sarry = td.split('-')
	ntd=''.join(sarry)
	folder='../data/entry/tdx_history/'
	preFname='沪深Ａ股'
	fname = preFname + ntd + '.txt'
	fpath = folder+fname.decode('utf8')
	if not os.path.isfile(fpath):
		print "Error: ", fpath, "not exist"
		exit()
	tpList = []
	file = open(fpath, 'r')
	line = file.readline()
	while line:
		if len(line)<6:
			line = file.readline()
			continue
		item = line[0:6]
		if not item.isdigit():
			line = file.readline()
			continue
		props = line.split('\t')
		if len(props)<6:
			print "Invalid line:", line
			line = file.readline()
			continue
		if props[3]=='' or props[4]=='0':
			#print "%s,'%s'" % (item, props[3])
			tpList.append(item)
		line = file.readline()
	file.close()

	folder='../data/entry/market/'
	fpath = folder+'stock_' + td + '.txt'
	if os.path.isfile(fpath):
		print fpath, "already exist, quit"
		exit()
	tpFile = open(fpath, 'w')
	for item in tpList:
		tpFile.write(item + '\n')
	tpFile.close()
