#!/usr/bin/env python
# -*- coding:gbk -*-

import sys
import re
import os
import datetime
import platform
import shutil
import getopt
import threading

sys.path.append('.')
from internal.format_parse import *
from internal.url_juchao.tips_res import *

JUCHAO_PRE_FD = "../data/entry/juchao/"

def fetch_jc_trade_tips(sdate, edate, lock=None):
	startDt = datetime.datetime.strptime(sdate, '%Y-%m-%d').date()
	endDt = datetime.datetime.strptime(edate, '%Y-%m-%d').date()

	if lock is None:
		date_str = startDt.strftime('%Y-%m-%d')
		year_start = date_str[:4]
		date_str = endDt.strftime('%Y-%m-%d')
		year_end = date_str[:4]
		fd = JUCHAO_PRE_FD + year_start
		if not os.path.exists(fd):
			print "Creat folder", fd
			os.makedirs(fd)
		if year_end!=year_start:
			fd = JUCHAO_PRE_FD + year_end
			if not os.path.exists(fd):
				print "Creat folder", fd
				os.makedirs(fd)
	while startDt<=endDt:
		date_str = startDt.strftime('%Y-%m-%d')
		#print(date_str)
		startDt += datetime.timedelta(days=1)
		year = date_str[:4]
		fn = JUCHAO_PRE_FD + year + "/jc" + date_str + ".txt"
		
		if os.path.exists(fn):
			continue

		content = get_trade_tips(date_str)
		#print 'daily_td', date_str, content
		if content is None:
			continue
		file = open(fn, "w")
		dict = json.loads(content)
		str = json.dumps(dict['clusterSRTbTrade0112']['srTbTrade0112s'], ensure_ascii=False, indent=4)
		str = str.encode('utf8')
		file.write(str)
		#file.write(json.dumps(dict['clusterSRTbTrade0112']['srTbTrade0112s'], ensure_ascii=False).encode('utf8'))
		#json.dump(dict['clusterSRTbTrade0112']['srTbTrade0112s'], file, ensure_ascii=False)
		file.close()
	return

def handle_tips_action(sdate, edate, single=0):
	thrdNum = 5
	threadIdx = 0
	threads = []
	
	startDt = datetime.datetime.strptime(sdate, '%Y-%m-%d').date()
	endDt = datetime.datetime.strptime(edate, '%Y-%m-%d').date()
	delta = endDt-startDt
	allDays = delta.days
	
	#单线程处理
	if single==1 or allDays<30:
		#print "Use single thread"
		fetch_jc_trade_tips(sdate, edate)
		return

	#print "Start multiple thread"
	startL = []
	endL = []
	fmt = "%4d-%02d-%02d"
	thdStartDt = startDt
	step = allDays/thrdNum
	delta = datetime.timedelta(days=step)
	#print "delta", allDays, step
	for i in range(thrdNum):
		thdEndDt = thdStartDt + delta
		sDt = fmt % (thdStartDt.year, thdStartDt.month, thdStartDt.day)
		eDt = fmt % (thdEndDt.year, thdEndDt.month, thdEndDt.day)
		startL.append(sDt)
		endL.append(eDt)
		#print sDt, eDt
		thdStartDt = thdEndDt + datetime.timedelta(days=1)

	#可能最后结束日期比实际结束日期多几天，替换最后日期
	if (thdEndDt-endDt).days>0:
		eDt = fmt % (endDt.year, endDt.month, endDt.day)
		endL[thrdNum-1] = eDt
		#print endL[thrdNum-1]

	lock = threading.Lock()

	for i in range(thrdNum):
		t = threading.Thread(target=fetch_jc_trade_tips, args=(startL[i], endL[i], lock))
		threads.append(t)

	for item in threads:
		item.start()
	for item in threads:
		item.join()
	return

#Main Start:
if __name__=='__main__':
	sdate = '2020-08-03'
	edate = sdate
	handle_tips_action(sdate, edate)
	