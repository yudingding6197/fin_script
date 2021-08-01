#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import json
import getopt

sys.path.append('.')
from internal.format_parse import *
from internal.trade_date import *
from internal.url_exchange.daily_stats import *

def handle_argument():
	optlist, args = getopt.getopt(sys.argv[1:], 'hd:s:e:')
	for option, value in optlist:
		if option in ["-h","--help"]:
			param_config["Help"] = 1
		elif option in ["-s","--start"]:
			param_config["Start"] = value
		elif option in ["-e","--end"]:
			param_config["End"] = value
	#print param_config
	
param_config = {
	"Help":0,
	"Start":'',
	"End":'',
}


if __name__=="__main__":
	handle_argument()
	trade_date = get_lastday()
	pre_date = get_preday(1, trade_date)
	pre_date = get_preday(1, trade_date,2)
	#db下的json 和 csv 文件都会更新
