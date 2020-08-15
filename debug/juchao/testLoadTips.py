#!/usr/bin/env python
# -*- coding:gbk -*-

#保存每日的交易信息
import sys
import re
import os
import datetime
import platform
import shutil
import getopt

sys.path.append('.')
from internal.format_parse import *
from internal.url_juchao.tips_res import *

def handle_argument():
	optlist, args = getopt.getopt(sys.argv[1:], 'hd:s:e:')
	for option, value in optlist:
		if option in ["-h","--help"]:
			param_config["Help"] = 1
		elif option in ["-s","--start"]:
			param_config["Start"] = value
		elif option in ["-e","--end"]:
			param_config["End"] = value
		elif option in ["-d","--Date"]:
			param_config["DFCF"] = 1
	#print param_config

param_config = {
	"Help":0,
	"Start":'',
	"End":'',
	"DFCF":0,
}
JUCHAO_PRE_FD = "../data/entry/juchao/"

#Main Start:
if __name__=='__main__':
	handle_argument()
	if param_config["Help"]==1:
		print("%s -s([.][YYYY]MMDD) -e([.][([YYYY]MMDD)])"%(os.path.basename(__file__)))
		exit(0)

	dt = '2019-06-20'
	#dt = '2020-08-03'
	year = dt[:4]
	fn = JUCHAO_PRE_FD + year + "/jc" + dt + ".txt"
	file = open(fn, 'r')
	dobj = json.load(file)
	if isinstance(dobj, list) is False:
		print ("Error, not expected list object")
		exit(0)
	for item in dobj:
		#print item['tradingTipsName']
		if item['tradingTipsName']==u'复牌日':
			print item['tradingTipsName']
			for dict in item['tbTrade0112s']:
				print dict['obSeccode0110'], dict['obSecname0110']
			print ""
		elif item['tradingTipsName']==u'分红转增除权除息日':
			print item['tradingTipsName']
			for dict in item['tbTrade0112s']:
				print dict['obSeccode0110'], dict['obSecname0110']				
			print ""
		elif item['tradingTipsName']==u'分红转增红利发放日':
			print item['tradingTipsName']
			for dict in item['tbTrade0112s']:
				print dict['obSeccode0110'], dict['obSecname0110']								
			print ""
