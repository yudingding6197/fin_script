#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import re
import os
import time
import datetime
import urllib2
#中文字符
#通过 time.clock() 和 datetime.datetime.now() 两种方式计算程序执行时间

# Main
if __name__ == '__main__':
	start = time.clock()
	st = datetime.datetime.now()

	delta1=datetime.timedelta(days=5)
	print delta1
	
	cur=datetime.datetime.now()
	fctime = 'TTT### %d-%d-%d %02d:%02d:%02d' %(cur.year, cur.month, cur.day, cur.hour, cur.minute, cur.second)
	print cur, fctime

	today = datetime.date.today()
	qdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)
	
	curdate = '2017-3-5'
	idx_date = datetime.datetime.strptime(curdate, '%Y-%m-%d').date()

	#2个日期间隔天数的计算
	obj = today - idx_date
	print "obj='%s', Delta days=%d"%(obj, obj.days)

	#'某一天'之前几天的日期
	edate = today - delta1
	print edate

	time.sleep(0.65)

	end = time.clock()
	ed = datetime.datetime.now()
	print "Time used:", end-start
	print ("Time Run:%s" %(ed-st))
