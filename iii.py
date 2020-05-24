#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import time
import string
import datetime
import platform
import shutil
import getopt
#import tushare as ts
#import internal.common
#from internal.ts_common import *
#from internal.dfcf_inf import *
from internal.trade_date import *
from internal.update_tday_db import *
from internal.analyze_realtime import *


param_config = {
	"NoLog":0,
	"NoDetail":0,
	"SortByTime":0,
	"AllInfo":0,
	"DFCF":0,
}
REAL_PRE_FD = "../data/"

#Main Start:
if __name__=='__main__':
	trade_day = get_lastday()
	#update_latest_trade(trade_day)
	pre_day = get_preday(6,trade_day)
	#print(trade_day, pre_day)
	
	beginTm = datetime.datetime.now()
	sysstr = platform.system()

	for i in range(1, 57):
		pre_day = get_preday(i,trade_day)
		filename = REAL_PRE_FD + 'entry/realtime/' + 'rt_' + pre_day + '.txt'
		parse_realtime(filename, pre_day)
	
	