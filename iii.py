#!/usr/bin/env python
# -*- coding: gbk -*-
import sys
import os
from internal.tingfupai import * 
from internal.url_juchao.tips_res import *


#Main Start:
if __name__=='__main__':
	#重出江湖STK
	fp_list = []
	fp_code_list = []
	trade_date = '2021-07-28'
	res_data = get_tingfupai_res(trade_date)
	s = json.loads(res_data)
	resumpObj = s["szshSRTbTrade0111"]["resumptionTbTrades"]
	if resumpObj is None:
		print "None"
		exit(0)
	for item in resumpObj:
		#print "pickup_tfp", item
		pass

	
	