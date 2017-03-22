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

def getSinaData(url, code, sleepTime, inst_info):
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
	#print stockObj[0]
	obj = re.match(r'.*\"(.*)',stockObj[0])
	str = obj.group(1)
	name = str.decode("gbk")
	#print name

	curPrice = stockObj[3]
	highPrice = stockObj[4]
	lowPrice = stockObj[5]
	lastPrice = stockObj[2]
	jingmaijia = stockObj[6]
	#variation = stockObj[43]
	zhangdiejia = 0.0
	if float(curPrice)==0:
		zhangdiejia = float(jingmaijia) - float(lastPrice)
	else:
		zhangdiejia = float(curPrice) - float(lastPrice)
	zhangdiefu = zhangdiejia*100/float(lastPrice)
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

	inst_info.append(code)
	inst_info.append(sellVol[0])
	inst_info.append(buyVol[0])
	inst_info.append(curPrice)
	inst_info.append(volume)
	inst_info.append(name)
	
	#还没有打开
	if sellVol[0]==0:
		return 0

	#已经打开
	return 1
	
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

# Main
data_path = "..\\Data\\entry\\_self_define.txt"
stockCode = []

today = datetime.date.today()
curdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)
#print curdate

if os.path.isfile(data_path) is False:
	print "No file:",data_path
	exit(0)

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

if len(stockCode)==0:
	print "No CX Data"
	exit(0)
#stockCode = stockCode[0:1]
#stockCode = ['sz002850']

slpTime = 2
idxCount=0
exgCount=0
sarr = ''
url = "http://hq.sinajs.cn/list="
exUrl = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php"
#exUrl = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php"
c_list = ['code', 'sell1', 'buy1', 'price', 'vol', 'name']
while True:
	now = datetime.datetime.now()
	hour = now.hour
	minute = now.minute

	print "---------------------[%02d:%02d:%02d]"%(hour, minute,now.second)

	opened_df = pd.DataFrame()
	fengbd_df = pd.DataFrame()
	for code in stockCode:
		inst_info = []
		state = getSinaData(url, code, slpTime, inst_info)
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
		print opened_df
	print ''

	if len(fengbd_df)==0:
		print "No FengBan Item"
	else:
		df = fengbd_df.sort_values(['buy1'], 0, True)
		df = df[df.buy1<50000]
		print df
	

	#currentSinaData(url, code, slpTime)

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
