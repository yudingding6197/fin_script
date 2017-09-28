#!/usr/bin/env python
# -*- coding:gbk -*-
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook
import sys
import re
import os
import time
import datetime
import ctypes
import sqlite3
from internal.common import *

def fun1():
	print "we are in %s"%__name__ 

if __name__ == '__main__':
	url = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._A&sty=FCOIATA&sortType=C&sortRule=-1&page=1&pageSize=20&js={rank:[(x)],pages:(pc)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c"
	LOOP_COUNT = 0
	while LOOP_COUNT<3:
		try:
			req = urllib2.Request(url)
			response = urllib2.urlopen(req, timeout=5)
		except:
			LOOP_COUNT += 1
			print "URL request timeout"
		else:
			break
	if response is None:
		print "NONE"
		exit(0)

	new_st_list = []
	print "LINE::::"
	line = response.read()
	print line[0:20]
	obj = re.match(r'{rank:\["(.*)"\].*', line)
	rank = obj.group(1)
	array = rank.split('","')
	print array[0]
	print array[1]
	print array[2]
	for i in range(0, len(array)):
		props = array[i].split(',')
		#print props
		code = props[1]
		val = props[5]
		if val[-1]=="%":
			val = val[:-1]
		print val
		print float(val)
		new_st_list.append(code)
	print new_st_list
