#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import json
import zlib
import random
import getopt

sys.path.append('.')
from internal.global_var import *
from internal.math_common import *
from internal.trade_date import *
#import pandas as pd
#import numpy as np
#from bs4 import BeautifulSoup

if __name__=="__main__":
	#获取ZT
	preArr = [ 
	20.11,
	0.13,
	127.58,
	]
	ratioUp = [ 1.05, 1.1, 1.2 ]
	ratioDw = [ 0.95, 0.9, 0.8 ]
	fmt = "%8.2f  %8.2f  %8.2f"
	for index in range(len(preArr)):
		pre_close = preArr[index]
		zt_price1 = pre_close * ratioUp[index]
		dt_price1 = pre_close * ratioDw[index]

		zt_price = spc_round2(zt_price1,2)
		dt_price = spc_round2(dt_price1,2)
		
		str = fmt % (pre_close, zt_price, dt_price)
		print str

	trade_date = get_lastday()
	pre30_date = get_preday(PRE_DAYS, trade_date)
	pre300_date = get_preday(CX_DAYS, trade_date)
	
	print trade_date
	init_trade_list(trade_date)
	p1 = calcu_pre_date(2, trade_date)
	p2 = calcu_pre_date(CX_DAYS, trade_date)
	print pre30_date, pre300_date
	print p1, p2
	
	
