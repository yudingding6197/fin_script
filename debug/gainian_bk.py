#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import os
import datetime
import json
import codecs

sys.path.append(".")
from internal.trade_date import *
from internal.url_dfcf.dc_hq_push import *

def handle_argument():
	optlist, args = getopt.getopt(sys.argv[1:], 's:e:c:fdg')
	for option, value in optlist:
		if option in ["-s","--startdate"]:
			param_config["StartDate"] = value
		elif option in ["-e","--enddate"]:
			param_config["EndDate"] = value
		elif option in ["-c","--count"]:
			param_config["Count"] = int(value)
		elif option in ["-f","--full"]:
			param_config["Full"] = 0
		elif option in ["-d","--download"]:
			param_config["Download"] = 1
		elif option in ["-g","--debug"]:
			param_config["Debug"] = 1
	#print param_config

param_config = {
	"StartDate":"",
	"EndDate":"",
	"Count":0,
	"Full":1,
	"Download":0,
	"Debug":0,
}

#Main Start:
#通过当日的概念BK文件，获取每一个GNBK的K线
if __name__=='__main__':
	t_d = get_lastday()
	gn_fp = '../data/entry/gainian/' + t_d[0:4] + '/gnbk_' + t_d + '.txt'
	if not os.path.exists(gn_fp):
		print("File not exist", gn_fp)
		exit(-1)

	file = open(gn_fp, 'r')
	info = json.load(file)
	file.close()
	
	klObj = None
	cur_kline='../data/entry/gainian/' + t_d[0:4] + '/gn_kline_' + t_d + '.txt'
	if os.path.exists(cur_kline):
		file = open(cur_kline, 'r')
		klObj = json.load(file)
		klLen = len(klObj)
		file.close()
		print ("Open Exist Kline", klLen)
		
	bFlag = 0
	bkList = []
	p_jq = 'jQuery112409533203989812345_1628206827123'
	for idx in range(0, info['data']['total']):
		#print info['data']['diff'][idx]['f14']
		#print info['data']['diff'][idx]['f12']
		if klObj is not None:
			if idx<klLen:
				if klObj[idx]['code']==info['data']['diff'][idx]['f12']:
					#print idx, klObj[idx]['code'],klObj[idx]['name']," existed"
					#print klObj[idx]['klines'][0][:11]
					#print klObj[idx]['klines'][-1][:11]
					bkList.append(klObj[idx])
					continue
		content = fetch_gn_history_kline('90',info['data']['diff'][idx]['f12'])
		obj = json.loads(content)
		try:
			#print (obj['rc'])
			bk_id = obj['data']['code']
		except Exception as e:
			print info['data']['diff'][idx]['f12']
			print info['data']['diff'][idx]['f14']
			print e
			break
		else:
			bkList.append(obj['data'])
			bFlag=1
	if bFlag==0:
		print("No data")
		exit(0)

	gnbk_kline = '../data/entry/gainian/' + t_d[0:4] + '/gn_kline_' + t_d + '.txt'
	file = codecs.open(cur_kline, 'w+', 'utf-8')
	file.write(json.dumps(bkList,ensure_ascii=False,indent=2))
	file.close()

	
