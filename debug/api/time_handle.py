#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import re
import os
import time
import datetime
import urllib2
#中文字符

# Main
if __name__ == '__main__':
	start = time.clock()

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

	end = time.clock()
	print "Time used:", end-start
