#!/usr/bin/env python
# -*- coding:utf8 -*-
import os
import urllib2,time
from internal.realtime_obj import *
from internal.trade_date import *

def parse_summary_info(f):
	stcsItem = statisticsItem()
	line = f.readline()
	while line:
		objs = re.match(".*ST\((\d+) ZT (\d+) DT\)(.*)", line)
		#print(line, objs)
		if objs is not None:
			break
		
		#判断访问超时导致的错误信息
		if line[:2]=="['":
			pass
		elif line[:4]=="<url":
			pass
		elif line[:6]=="timed ":
			pass
		else:
			print("Error: Get ZT DT fail", line)
			return -1
		line = f.readline()
	stcsItem.s_st_yzzt = int(objs.group(1))
	stcsItem.s_st_yzdt = int(objs.group(2))
	
	com_str = objs.group(3)
	objs = com_str.split(',')
	#print(len(objs), objs[0])
	for i in range(0, len(objs)):
		items = re.match('[\t ]+(\d+)[\t ]+(.*)', objs[i])
		#print(i, objs[i], items.groups())
		value = int(items.group(1))
		tname = items.group(2)
		if tname=='DTKP':
			stcsItem.s_open_dt = value
		elif tname=='YZDT':
			stcsItem.s_yzdt = value
		elif tname=='DTDK':
			stcsItem.s_open_dt_dk = value
		elif tname=='DaoT ':
			stcsItem.s_dt_daoT = value
		else:
			print("Warning: ======== unknown", items.groups());
	
	#line = f.readline()
	return 0

def parse_realtime(filename, pre_day):
	pFlag = 0
	hour = 0
	minute = 0
	hour1 = 0
	minute1 = 0
	
	f = open(filename, 'r')
	print(filename)

	line = f.readline()
	while line:
		objs = re.match("TIME: (.*) (\d+):(\d+)", line)
		if pFlag==0:
			if objs is None:
				line = f.readline()
				continue
			else:
				hour = int(objs.group(2))
				minute = int(objs.group(3))
				if hour>=15:
					#print("Find Line", line)
					pFlag = 1
				line = f.readline()
				continue
		#end if pFlag
		if objs is not None:
			#print("Next Line", line)
			hour1 = int(objs.group(2))
			minute1 = int(objs.group(3))
			break
		
		objs = re.match("(\d+)-(\d+)-(\d+)", line)
		if objs is not None:
			#print("Read summary")
			ret = parse_summary_info(f)
			if ret==-1:
				return
		
		line = f.readline()
	f.close()
	
	if hour<15:
		print("Warning: check file", filename, hour, minute)
	if hour1<15:
		print("Warning: 1 check file", filename, hour1, minute1)
	

#Main
if __name__=='__main__':
	pass
