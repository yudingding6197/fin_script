#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import json
import getopt

sys.path.append('.')
from internal.format_parse import *
from internal.trade_date import *
from internal.url_exchange.daily_stats import *
from name_def import *

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

def fetch_jys_data(base_date, exchange='sz'):
	fileFmt = "%s/%s/%s_%s.txt"

	y_folder = MARKET_DAILY_FD + base_date[:4]
	if not os.path.exists(y_folder):
		os.makedirs(y_folder)

	filename = fileFmt % (MARKET_DAILY_FD,base_date[:4], base_date, exchange)
	if os.path.exists(filename):
		return

	tpstr = 'string'
	contObj = None
	if exchange=='sz':
		contObj = query_szse_daily_stats(base_date, tpstr)
	elif exchange=='sh':
		contObj = query_shse_daily_stats(base_date, tpstr)
		
	if contObj is None or contObj=='':
		print "Error: query data is None",base_date
		exit(-1)
	#print json.dumps(contObj[0]['data'][0], ensure_ascii=False)
	#print stepDt
	
	tf_fl = open(filename, 'w+')
	tf_fl.write(contObj)
	#json.dump(contObj, tf_fl)
	tf_fl.close()


param_config = {
	"Help":0,
	"Start":'',
	"End":'',
}

if __name__=="__main__":
	handle_argument()
	trade_date = get_lastday()
	ret, sdate = parseDate2(param_config["Start"])
	if ret==-1:
		exit(0)

	if param_config["End"]=='':
		param_config["End"] = trade_date
	ret, edate = parseDate2(param_config["End"])
	if ret==-1:
		exit(0)

	startDt = datetime.datetime.strptime(sdate, '%Y-%m-%d').date()
	endDt = datetime.datetime.strptime(edate, '%Y-%m-%d').date()
	stepDt = startDt

	fmt = '%04d-%02d-%02d'
	init_trade_list(trade_date)
	while (endDt-stepDt).days>=0:
		base_date = fmt %(stepDt.year, stepDt.month, stepDt.day)
		#read_st_in_daily_tips(base_date, stk_list, stk_dict)

		if is_trade_date(base_date):
			fetch_jys_data(base_date, 'sh')
			fetch_jys_data(base_date, 'sz')
		stepDt += datetime.timedelta(days=1)
	release_trade_list()
	
	''''
	#r1 = random.random()
	dt = '2020-09-15'
	urlall = urlfmt %(dt, r1) 
	print urlall

	list = json.loads(content,object_pairs_hook=OrderedDict)
	#list = json.loads(content)
	print json.dumps(list[0]['data'], ensure_ascii=False)
	'''
