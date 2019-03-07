#!/usr/bin/env python
# -*- coding:gbk -*-
#以前生成数据的解析
import sys
import re
import os
import string
import datetime
import urllib2
import zlib
import pandas as pd

#reload(sys)
#sys.setdefaultencoding('gbk')

def parse_stk_data(file, key_title, index, dict):
	stockList = []
	#upStkList = []
	#if dict.has_key('QU'):
	#	upStkList = dict.has_key('QU')
	if index<3:
		if dict.has_key('Q'):
			stockList = dict['Q']
	else:
		if dict.has_key('R'):
			stockList = dict['R']

	line = file.readline()
	while line:
		if len(line)<=3:
			if index<3:
				dict['Q'] = stockList
				#dict['QU'] = upStkList
			else:
				dict['R'] = stockList
				#dict['RU'] = upStkList
			break
		obj = re.match(r' *([\d]+) ([\d]+).* ([-]?\d+\.[\d]+)[ \t]+(\d+) ', line)
		#print (obj.group(3), obj.group(4))
		#print (line)
		if obj is None:
			print("Parse fail in line:" + line)
		else:
			day = int(obj.group(4))
			code = obj.group(2)
			if day>2:
				if code not in stockList:
					stockList.append(code)
			#elif day==2:
			#	if code not in stockList:
			#	upStkList.append(obj.group(2))
		line = file.readline()
	#end while loop

def parse_realtime_data(rt_file, dict):
	p_flag = 0
	file = open(rt_file, 'r')
	if file is None:
		print("Error open file" + rt_file)
		return

	line = file.readline()
	key_title = ['YZZT ', 'ZT ', 'ZTHL ', 'YZDT ', 'DT ', 'DTFT ']
	while line:
		if len(line)<=6:
			line = file.readline()
			continue
		if p_flag == 1:
			for i in range(len(key_title)):
				if line[:3]==key_title[i][:3]:
					index = i
					#print(i, key_title[i])
					parse_stk_data(file, key_title, i, dict)
					break
			if line[:6] == "TIME: ":
				p_flag=0
				break
			#print line
			
			line = file.readline()
			continue

		if line[:6] == "TIME: ":
			obj = re.match(r'TIME: (.*) (\d+):(\d+)', line)
			hour = int(obj.group(2))
			minute = int(obj.group(3))
			if hour>=15 and minute>0:
				#print (line)
				p_flag = 1
		line = file.readline()
	#end while loop

	'''
	for item in key_title:
		if dict.has_key(item):
			#print dict[item]
			sn_code = []
			for cd in dict[item]:
				ncode = sina_code(cd)
				sn_code.append(ncode)

			rt_list = []
			realtime_price(sn_code, rt_list)
			df = pd.DataFrame(rt_list, columns=column)
			rt_quotes(df, item, qt_stage)
	'''	

	