#!/usr/bin/env python
# -*- coding:gbk -*-

import sys
import re
import os
import datetime
import pandas as pd
import tushare as ts
from internal.common import *
from internal.ts_common import *

def fun1():
	print "we are in %s"%__name__ 

if __name__ == '__main__':
	src = ['sn', 'tt', 'nt']
	for ds in src:
		try:
			df = ts.get_tick_data('603987', '2018-01-05', src=ds)
		#except IOError as e:
		except Exception as e:
			print Exception
			print e
			continue
		else:
			pass
		if df is None:
			continue
		print "____________"
		df = df.iloc[::-1]

		#df.to_csv("aa_" +ds+".csv", encoding="gbk", index=False)
		#break
	print 'ddddddd', ds
	#print df.iloc[::-1]
	#get_latest_market(new_st_list)
	coindf = pd.read_csv("aa_tt.csv")
	print coindf
	
	#print len(new_st_list)


