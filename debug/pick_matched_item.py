#!/usr/bin/env python
# -*- coding:gbk -*-

import sys
import re
import os
import datetime
sys.path.append(".")
sys.path.append("..")
from internal.ts_common import *
import tushare as ts

#选出符合条件的item
if __name__=='__main__':
	days = 5
	tradeList = []
	get_pre_trade_date(tradeList, 5)
	if len(tradeList)!=days:
		print "Fail to get trade date"
	print tradeList
	
