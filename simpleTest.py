#!/usr/bin/env python
# -*- coding:gbk -*-

import sys
import re
import os
import datetime
import tushare as ts
from internal.common import *
from internal.ts_common import *

def fun1():
	print "we are in %s"%__name__ 

if __name__ == '__main__':
	src = ['sn', 'tt', 'nt']
	for ds in src:
		print ds
		df = ts.get_tick_data('300291', '2018-01-05', src=ds)
		if ds!='sn' and df.empty:
			continue
		if ds=='sn':
			tm = df.ix[0][0]
			tmObj = re.match('(\d+):(\d+):(\d+)', tm)
			print tmObj
			if tmObj is None:
				continue
		print "____________"
		df.to_csv("aa_" +ds+".csv", encoding="gbk")
		#break

	#get_latest_market(new_st_list)
	
	#print len(new_st_list)


