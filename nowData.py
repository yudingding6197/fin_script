# -*- coding:gbk -*-
import sys
import re
import os
import string
import datetime
import urllib
import urllib2
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook
import internal.common
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

def currentSinaData(url, code, sleepTime):
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
		print urllink
		req = urllib2.Request(urllink)
		stockData = urllib2.urlopen(req, timeout=2).read()
	except:
		print "URL timeout"
	else:
		stockObj = stockData.split(',')
		stockLen = len(stockObj)
		if stockLen<10:
			return
		#for i in range(0, stockLen):
		#	print "%02d:	%s" % (i, stockObj[i])

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
		print "---------------------"
		print "[%s]	[%s	%s]" % (curPrice, highPrice, lowPrice)
		index = 4
		for i in range(0, 5):
			print "%s	%8s" %(sell[index], sellVol[index])
			index -= 1
		print "===%s (%.02f%%)" %(curPrice,zhangdiefu)
		index = 0
		for i in range(0, 5):
			print "%s	%8s" %(buy[index], buyVol[index])
			index += 1

		highIntP = int(float(highPrice)*1000)
		lowIntP = int(float(lowPrice)*1000)
		curIntP = int(float(curPrice)*1000)
		lastIntP = int(float(lastPrice)*1000)
		highPercent = (highIntP-lastIntP)*10000/lastIntP
		lowPercent = (lowIntP-lastIntP)*10000/lastIntP

		#可能ZT
		if (sellVol[0]==0 and sellVol[1]==0 and sellVol[2]==0 and sellVol[3]==0):
			dltVol = ZT_BUY_VOL - buyVol[0]
			if dltVol<0:
				ZT_BUY_VOL = buyVol[0]
			elif dltVol>=100000:
				msgstr = u'ZZ Quickly Change %d,%d'%(ZT_BUY_VOL, buyVol[0])
				ZT_BUY_VOL = buyVol[0]
				ctypes.windll.user32.MessageBoxW(0, msgstr, '', 0)
		#可能DT
		elif (buyVol[0]==0 and buyVol[1]==0 and buyVol[2]==0 and buyVol[3]==0):
			dltVol = DT_SELL_VOL - sellVol[0]
			if dltVol<0:
				DT_SELL_VOL = sellVol[0]
			elif dltVol>=100000:
				msgstr = u'DD Quickly Change %d,%d'%(DT_SELL_VOL, sellVol[0])
				DT_SELL_VOL = sellVol[0]
				ctypes.windll.user32.MessageBoxW(0, msgstr, '', 0)

		#最高涨幅百分比期望超过最低涨幅百分比 0.5%(转为整数位50)
		if (highIntP-curIntP)<15 and (highPercent-lowPercent)>50:
			#可能DT
			if (buyVol[0]==0 and buyVol[1]==0 and buyVol[2]==0 and buyVol[3]==0):
				pass
			#可能ZT
			elif (sellVol[0]==0 and sellVol[1]==0 and sellVol[2]==0 and sellVol[3]==0):
				pass
			else:
				print highIntP, curIntP
				if ALERT_HIGH<curIntP:
					ALERT_HIGH = curIntP
					ctypes.windll.user32.MessageBoxW(0, u'High! Have a rest', '', 0)
				if COND_COUNT<=0:
					COND_COUNT = 60
				else:
					COND_COUNT -= sleepTime

def handle_price(priceList):
	#循环得到数据后，判断条件是否满足
	maxValue = priceList[3]
	minValue = priceList[2]
	curValue = priceList[1]
	curValue0 = priceList[0]
	if ((maxValue-minValue) >= deltaV):
		#print maxValue-int(curValue*100)
		#print int(curValue*100)-minValue
		bMatched = 0
		if (maxValue-curValue)<=deltaTg:
			print "Increase: %.02f (%d	%d)"%(curValue0, maxValue, minValue)
			for j in range(0, len(alertPrice)):
				if curValue==alertPrice[j]:
					bMatched = 1
					break
			if bMatched==0:
				alertPrice.append(curValue)
				ctypes.windll.user32.MessageBoxW(0, u'High value', '', 0)
		elif (curValue-minValue)<=deltaTg:
			print "Decrease: %.02f (%d	%d)"%(curValue0, maxValue, minValue)
			for j in range(0, len(alertPrice)):
				if curValue==alertPrice[j]:
					bMatched = 1
					break
			if bMatched==0:
				alertPrice.append(curValue)
				ctypes.windll.user32.MessageBoxW(0, u'Low value', '', 0)

pindex = len(sys.argv)
if pindex<2:
	sys.stderr.write("Usage: " +os.path.basename(sys.argv[0])+ " 代码 [睡眠时间] [最大最小值之差 触发消息门限值]\n")
	exit(1);

code = sys.argv[1]
if (len(code) != 6):
	sys.stderr.write("Len should be 6\n")
	exit(1);

head3 = code[0:3]
result = (cmp(head3, "000")==0) or (cmp(head3, "002")==0) or (cmp(head3, "300")==0) or (cmp(head3, "131")==0)
if result is True:
	code = "sz" + code
else:
	result = (cmp(head3, "600")==0) or (cmp(head3, "601")==0) or (cmp(head3, "603")==0) or (cmp(head3, "204")==0)
	if result is True:
		code = "sh" + code
	else:
		print "非法代码:" +code+ "\n"
		exit(1);

deltaV = 0
deltaTg = 0
if pindex==3:
	slpTime = int(sys.argv[2])

if pindex==5:
	deltaV = int(sys.argv[2])
	deltaTg = int(sys.argv[3])
else:
	deltaV = 6
	deltaTg = 2

idxCount=0
exgCount=0
sarr = ''
url = "http://hq.sinajs.cn/list="
exUrl = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php"
#exUrl = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php"

priceList = [0, 0, 0, 0]
#当价格快速上拉的时候提醒
alertPrice = []
#当连续大单出现时报警
contPrice = []

#临时处理方案，对国债逆回购
head5 = code[0:5]
bBigChange = (cmp(head5, "sz131")==0) or (cmp(head5, "sh204")==0)

while True:
	now = datetime.datetime.now()
	hour = now.hour
	minute = now.minute

	print "---------------------[%02d:%02d:%02d]"%(hour, minute,now.second)
	currentIndexData(url, "s_sh000001")
	if idxCount>=2:
		currentIndexData(url, "s_sz399001")
		currentIndexData(url, "s_sz399005")
		idxCount = 0
	else:
		idxCount += slpTime
	currentIndexData(url, "s_sz399006")
	currentSinaData(url, code, slpTime)

	bAnalyze = 0
	if ((hour==9 and minute>=30) or hour==10 or (hour==11 and minute<=30)):
		bAnalyze = 1
	elif (hour==13 or hour==14):
		bAnalyze = 1

	if bAnalyze==1:
		if exgCount==0:
			if not bBigChange:
				internal.common.analyze_data(exUrl, code, sarr, priceList, contPrice)
				handle_price(priceList)
			exgCount += slpTime
		elif exgCount>=30:
			exgCount = 0
		else:
			exgCount += slpTime
	print "~~~~~~~~~~~~~~~~~~~~~\n"

	if (hour<9 or hour>=15 or hour==12):
		break
	elif (hour==9 and minute<15):
		break
	elif (hour==11 and minute>30):
		break

	time.sleep(slpTime)
