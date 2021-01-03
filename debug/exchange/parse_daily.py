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

CHECK_ARR = [HU_A, HU_TOTAL, HU_KCB,u"股票",u"主板A股",u"中小板",u"创业板",u"创业板A股"]
SHOW_ARR = [HU_A, HU_KCB, u"主板A股",u"中小板",u"创业板"]

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

def parse_jys_data(base_date, daily_dict, exchange='sz'):
	fileFmt = "%s/%s/%s_%s.txt"

	filename = fileFmt % (MARKET_DAILY_FD,base_date[:4], base_date, exchange)
	if not os.path.exists(filename):
		return -1

	tpstr = 'string'

	file = open(filename, 'r')
	contObj = json.load(file,encoding='utf-8')
	file.close()
	
	#print filename
	#print contObj
	arr = [u"基金",u"债券",u"期权"]
	if exchange=='sz':
		#print json.dumps(contObj[0]['data'], ensure_ascii=False)
		if base_date in daily_dict.iterkeys():
			cur_dict = daily_dict[base_date]
		else:
			cur_dict = {}

		contData = contObj[0]['data']
		for item in contData:
			name = item['lbmc'].strip().replace('&nbsp;','')
			if name not in CHECK_ARR:
				continue
			
			val1 = float(item["cjje"].replace(',',''))
			val2 = float(item["ltsz"].replace(',',''))
			ratio = round(val1 * 100 / val2, 4)
			list = [val1, val2, ratio]
			if name==u"创业板A股":
				name = u"创业板"
			cur_dict[name] = list
			#print item['lbmc'].replace('&nbsp;',''), float(item["cjje"].replace(',','')),item["ltsz"]
		#print "\n\n"
		if base_date not in daily_dict.iterkeys():
			daily_dict[base_date] = cur_dict
		
	elif exchange=='sh':
		#print contObj["result"]
		ll = len(contObj["result"])
		#if not (ll==3 or ll==6):
		#	print base_date, len(contObj["result"])
		if base_date in daily_dict.iterkeys():
			cur_dict = daily_dict[base_date]
		else:
			cur_dict = {}

		if not (ll==3 or ll==5 or ll==6):
			print "Warning: SH invalid length", base_date, ll
			#daily_dict[base_date] = {}
			return 0
		for index in range(len(contObj["result"])):
			obj = contObj["result"][index]
			list = []
			bFlag = 0
			if index==0:
				bFlag = 1
				name = HU_A
			elif index==1:
				bFlag = 1
				name = HU_TOTAL
			elif index==5:
				bFlag = 1
				name = HU_KCB

			if bFlag==1:
				val1 = float(obj["TX_AMOUNT"])
				val2 = float(obj["NEGOTIABLE_VALUE"])
				ratio = float(obj["EXCHANGE_RATE"])
				list = [val1, val2, ratio]
				cur_dict[name] = list
		if base_date not in daily_dict.iterkeys():
			daily_dict[base_date] = cur_dict
		pass
	return 0
	'''
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
	'''

def generate_csv(dailyDict,start,end):
	fileFmt = "%s/%s_%s.csv"
	if not os.path.exists(MARKET_DAILY_RESULT):
		os.makedirs(MARKET_DAILY_RESULT)
	filename = fileFmt % (MARKET_DAILY_RESULT,start, end)

	keys = dailyDict.keys()
	keys.sort(reverse=False)
	
	t_fmt = "%s,%s,%s,"
	fmt = "%s,%s,%s,%s,%s,%s"
	data = "%.2f,%.2f,%.2f"
	data_not = "-,-,-"
	file = open(filename, "w")
	t_value = " ,"
	for title in SHOW_ARR:
		str = t_fmt % ('','',title)
		t_value += str
	file.write(t_value.encode('gbk')+"\n")

	for item in keys:
		#print dailyDict[item]
		dictObj = dailyDict[item]
		str = item
		for obj in SHOW_ARR:
			#print "CHECK",obj
			if obj in dictObj.iterkeys():
				#print obj, "IN"
				#print obj, dictObj[obj]
				if obj==HU_TOTAL:
					continue
				elif obj==u"股票":
					continue
				value = data % (dictObj[obj][0],dictObj[obj][1],dictObj[obj][2])
				str = str + "," + value
			else:
				#print obj, "NOT"
				str = str + "," + data_not
		file.write(str+"\n")
			
	file.close()
	
param_config = {
	"Help":0,
	"Start":'',
	"End":'',
}


if __name__=="__main__":
	handle_argument()
	trade_date = get_lastday()
	if param_config["Start"]=='':
		param_config["Start"] = '20080101'
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
	dailyDict = {}
	while (endDt-stepDt).days>=0:
		base_date = fmt %(stepDt.year, stepDt.month, stepDt.day)
		if is_trade_date(base_date):
			if parse_jys_data(base_date, dailyDict, 'sz')==-1:
				break
			elif parse_jys_data(base_date, dailyDict, 'sh')==-1:
				break
		stepDt += datetime.timedelta(days=1)
	release_trade_list()
	
	#print json.dumps(dailyDict,ensure_ascii=False)
	generate_csv(dailyDict, sdate, edate)
