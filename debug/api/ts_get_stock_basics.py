#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import time
import datetime
import tushare as ts

LOOP_COUNT=0
while LOOP_COUNT<3:
	try:
		df = ts.get_stock_basics()
	except:
		LOOP_COUNT += 1
		time.sleep(0.5)
	else:
		break;
if df is None:
	print "Timeout to get stock basic info"
	exit(0)
df1 = df.sort_values(['timeToMarket'], 0, False)
#df1 = df1.head(20)
print df1
