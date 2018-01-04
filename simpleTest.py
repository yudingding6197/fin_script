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
	src = ['tt', 'sn', 'nt']
	for ds in src:
		print ds
		df = ts.get_tick_data('000520', '2018-01-02', src=ds)
		print df.head(5)
		print "____________"
		df.to_csv("aaa.csv", encoding="gbk")
		break

	#get_latest_market(new_st_list)
	
	#print len(new_st_list)


