# -*- coding:gbk -*-
import sys
import os
import re
import string
import datetime
import urllib2
import pandas as pd
import time
import ctypes
from internal.ts_common import *

ALERT_HIGH = 0
COND_COUNT = 0
slpTime=1
ZT_BUY_VOL = 0
DT_SELL_VOL = 0

def currentIndexData(url, code):
	urllink = url + code
	try:
		req = urllib2.Request(urllink)
		stockData = urllib2.urlopen(req, timeout=2).read()
	except:
		print "URL timeout"
	else:
		stockObj = stockData.split(',')
		if len(stockObj)<3:
			return
		idxVal = "%.02f"%(float(stockObj[1]))
		print "%10s	%s%%(%s)" % (idxVal, stockObj[3], stockObj[2])

def handle_code(code):
	head3 = code[0:3]
	result = (cmp(head3, "000")==0) or (cmp(head3, "002")==0) or (cmp(head3, "300")==0) or (cmp(head3, "131")==0)
	if result is True:
		code = "sz" + code
		return code

	result = (cmp(head3, "600")==0) or (cmp(head3, "601")==0) or (cmp(head3, "603")==0) or (cmp(head3, "204")==0)
	if result is True:
		code = "sh" + code
		return code

	print "非法代码:" +code+ "\n"
	return None

def getSinaData(url, code, sleepTime, inst_info, phase):
	global COND_COUNT
	global ALERT_HIGH
	global ZT_BUY_VOL
	global DT_SELL_VOL

	urllink = url + code
	buy = []
	buyVol = []
	sell = []
	sellVol = []
	try:
		#print urllink
		req = urllib2.Request(urllink)
		stockData = urllib2.urlopen(req, timeout=2).read()
	except:
		print "URL timeout"
		return -1

	#print stockData
	stockObj = stockData.split(',')
	stockLen = len(stockObj)
	if stockLen<10:
		return -1

	#for i in range(0, stockLen):
	#	print "%02d:	%s" % (i, stockObj[i])

	obj = re.match(r'.*\"(.*)',stockObj[0])
	str = obj.group(1)
	name = str.decode("gbk")
	#print name

	curPrice = stockObj[3]
	highPrice = stockObj[4]
	lowPrice = stockObj[5]
	pre_close = float(stockObj[2])
	jingmaijia = stockObj[6]
	#variation = stockObj[43]
	zhangdiejia = 0.0
	if float(curPrice)==0:
		zhangdiejia = float(jingmaijia) - pre_close
	else:
		zhangdiejia = float(curPrice) - pre_close
	zhangdiefu = zhangdiejia*100/pre_close

	zt_price1 = pre_close * 1.1
	dt_price1 = pre_close * 0.9
	zt_price = spc_round(zt_price1,2)
	dt_price = spc_round(dt_price1,2)

	#成交量 和 成交额
	volume = stockObj[8]
	amount = stockObj[9]

	index = 11
	for i in range(0, 5):
		buy.append(stockObj[index+i*2])
	index = 10
	for i in range(0, 5):
		buyVol.append(int(stockObj[index+i*2])/100)
	index = 21
	for i in range(0, 5):
		sell.append(stockObj[index+i*2])
	index = 20
	for i in range(0, 5):
		sellVol.append(int(stockObj[index+i*2])/100)

	#print code, name, "===BUY_PRICE", buy[0], buy[1], buy[2]

	if (code[0:2]=='sh' or code[0:2]=='sz'):
		inst_info.append(code[2:])
	else:
		inst_info.append(code)
	inst_info.append(sellVol[0])
	inst_info.append(buyVol[0])
	inst_info.append(buyVol[1])
	inst_info.append(curPrice)
	inst_info.append(volume)
	inst_info.append(name)

	if highPrice!=lowPrice:
		return 1

	status = 0
	if phase==1:
		if buy[0]!=zt_price:
			status = 1
	else:
		if sellVol[0]!=0:
			status = 1
	return status

def get_stk_by_file(stockCode):
	data_path = "..\\Data\\entry\\_self_define.txt"
	if os.path.isfile(data_path) is False:
		print "No file:",data_path
		return

	file = open(data_path, 'r')
	while 1:
		lines = file.readlines(100000)
		if not lines:
			break
		for line in lines:
			code = line.strip()
			if len(code)!=6:
				continue
			if code.isdigit() is False:
				continue
			code = handle_code(code)
			if code is None:
				continue
			#print code
			stockCode.append(code)
	file.close()


# Main
pindex = len(sys.argv)
if pindex==2:
	slpTime = int(sys.argv[1])

today = datetime.date.today()
curdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)
#print curdate
stockCode = []

get_stk_by_file(stockCode)
if len(stockCode)==0:
	print "No CX Data"
	exit(0)
#stockCode = stockCode[0:1]
#stockCode = ['sz300625']

idxCount=0
exgCount=0
sarr = ''
url = "http://hq.sinajs.cn/list="
c_list = ['code', 'sell1', 'buy1', 'buy2', 'price', 'vol', 'name']
while True:
	now = datetime.datetime.now()
	hour = now.hour
	minute = now.minute

	print "---------------------[%02d:%02d:%02d]"%(hour, minute,now.second)
	#处理竞价阶段
	phase = 0
	filter_vol = 200000
	if (hour==9 and minute>=14 and minute<=25):
		phase = 1
		filter_vol = 200000
	elif (hour<10):
		phase = 2
		filter_vol = 150000
	else:
		phase = 3
		filter_vol = 40000

	opened_df = pd.DataFrame()
	fengbd_df = pd.DataFrame()
	for code in stockCode:
		inst_info = []
		state = getSinaData(url, code, slpTime, inst_info, phase)
		#print inst_info
		if state<0:
			continue

		if state==0:
			df1 = pd.DataFrame([inst_info], columns=c_list)
			fengbd_df = fengbd_df.append(df1)
		elif state==1:
			df1 = pd.DataFrame([inst_info], columns=c_list)
			opened_df = opened_df.append(df1)

	#所有数据获取完成，准备显示
	if len(opened_df)==0:
		print "No KaiBan Item"
	else:
		if phase==1:
			df = opened_df.sort_values(['buy2'], 0, True)
		else:
			df = opened_df.sort_values(['buy1'], 0, True)
		print df
	print ''
	str = "#########################################"
	if len(fengbd_df)==0:
		print str
		print "No FengBan Item"
	else:
		if phase==1:
			df = fengbd_df.sort_values(['buy2'], 0, True)
			df = df[df.buy2<filter_vol]
		else:
			df = fengbd_df.sort_values(['buy1'], 0, True)
			df = df[df.buy1<filter_vol]
		print "T:%d   S:%d %s"%(len(fengbd_df), len(df), str)
		print df
	print "===================================="
	print "\n\n"
	time.sleep(slpTime)

	'''	
	if (hour<9 or hour>15 or hour==12):
		break
	elif (hour==9 and minute<14):
		break
	elif (hour==15 and minute>1):
		break
	elif (hour==11 and minute>31):
		break
	'''
