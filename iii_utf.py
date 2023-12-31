#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import datetime
import json
import getopt
import codecs

from internal.trade_date import *

#test case
DB_PATH = 'internal/db'

#Main Start:
if __name__=='__main__':
	print sys.getdefaultencoding()
	print sys.stdout.encoding
	#reload(sys)
	#sys.setdefaultencoding('gbk')
	
	location = DB_PATH + '/' + 'sh000001_json2.txt'
	file = open(location, 'r')
	jFile = json.load(file)
	jStr = jFile.decode('unicode_escape').encode('utf-8')
	jDict = json.loads(jStr)
	file.close()

	lst = []
	for item in jDict["times"]:
		ret,curdate = parseDate2(item)
		if ret==-1:
			print("Parse fail", item)
			continue
		lst.append(curdate)
	lst.reverse()
	
	file = open('_stock_trd_date.txt','w')
	json.dump(lst,file)
	file.close()
	