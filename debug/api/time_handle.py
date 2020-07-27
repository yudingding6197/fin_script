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
	#当前日期和时间
	st = datetime.datetime.now()
	#当前日期
	dt = datetime.date.today()

	delta1=datetime.timedelta(days=5)
	print delta1
	
	cur=datetime.datetime.now()
	fctime = 'TTT### %d-%d-%d %02d:%02d:%02d' %(cur.year, cur.month, cur.day, cur.hour, cur.minute, cur.second)
	print cur, fctime
	
	ttm = time.strptime('15:23:56', "%H:%M:%S")
	print("TIME:==", ttm, type(ttm))
	t1 = time.strptime('2020-05-28 15:23:56', "%Y-%m-%d %H:%M:%S")
	t2 = time.strptime('2020-05-28 15:25:56', "%Y-%m-%d %H:%M:%S")

	#当前日期
	today = datetime.date.today()
	
	#将时间格式转为字符串格式
	qdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)
	
	#将字符串格式转为时间格式，类型为 datetime.datetime
	curdate = '2017-3-5'
	idx_date = datetime.datetime.strptime(curdate, '%Y-%m-%d').date()
	print("data fmt===", type(idx_date), idx_date)

	enddate = '2017-3-11'
	end_date = datetime.datetime.strptime(enddate, '%Y-%m-%d').date()
	#计算起始日期相差多少天
	delta = end_date-idx_date
	print("day interval1=", delta.days)
	
	dt_str = '2017-3-5 12:23:56'
	tm1 = datetime.datetime.strptime(dt_str, '%Y-%m-%d  %H:%M:%S')
	print("tm1 fmt===", type(tm1), tm1)
	dt_str = '2017-3-15 12:27:56'
	tm2 = datetime.datetime.strptime(dt_str, '%Y-%m-%d  %H:%M:%S')
	print("tm2 fmt===", type(tm2), tm2)
	print((tm2-tm1).seconds, (tm2-tm1).total_seconds() )
	
	#将字符串格式转为日期格式，类型为 datetime.date，包含2中方案
	fmt = '%Y-%m-%d'
	time_tuple = time.strptime(curdate, fmt)
	year, month, day = time_tuple[:3]
	a_date = datetime.date(year, month, day)
	print(a_date, type(a_date))

	a_date = datetime.date(*map(int, curdate.split('-')))
	print(a_date, type(a_date))

	#2个日期间隔天数的计算
	obj = today - idx_date
	print "obj='%s', Delta days=%d"%(obj, obj.days)

	#'某一天'之前几天的日期
	edate = today - delta1
	print edate
	
	#'某一天'加一天
	delta1=datetime.timedelta(days=1)
	edate = today + delta1
	print edate
	
	
	#'某一天'加一小时
	#'某一天'加一分钟


	time.sleep(0.65)

	end = time.clock()
	ed = datetime.datetime.now()
	print "Time used:", end-start
	print ("Time Run:%s" %(ed-st))
