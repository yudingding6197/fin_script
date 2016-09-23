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

COND_COUNT = 0
slpTime=1

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
	urllink = url + code
	buy = []
	buyVol = []
	sell = []
	sellVol = []
	try:
		req = urllib2.Request(urllink)
		stockData = urllib2.urlopen(req, timeout=2).read()
	except:
		loginfo(1)
		print "URL timeout"
	else:
		stockObj = stockData.split(',')
		stockLen = len(stockObj)
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

		#最高涨幅百分比期望超过最低涨幅百分比 0.5%(转为整数位50)
		if (highIntP-curIntP)<15 and (highPercent-lowPercent)>50:
			#可能涨停了
			if (buyVol[1]==0 and buyVol[2]==0 and buyVol[3]==0):
				pass
			#可能一字跌停
			elif (sellVol[1]==0 and sellVol[2]==0 and sellVol[3]==0):
				pass
			else:
				print highIntP, curIntP
				os.system('msg "*" "High! Have a rest"')
				if COND_COUNT<=0:
					COND_COUNT = 60
				else:
					COND_COUNT -= sleepTime

pindex = len(sys.argv)
if pindex<2:
	sys.stderr.write("Usage: " +os.path.basename(sys.argv[0])+ " 代码 [最大最小值之差 触发消息门限值]\n")
	exit(1);

code = sys.argv[1]
if (len(code) != 6):
	sys.stderr.write("Len should be 6\n")
	exit(1);

head3 = code[0:3]
result = (cmp(head3, "000")==0) or (cmp(head3, "002")==0) or (cmp(head3, "300")==0)
if result is True:
	code = "sz" + code
else:
	result = (cmp(head3, "600")==0) or (cmp(head3, "601")==0) or (cmp(head3, "603")==0)
	if result is True:
		code = "sh" + code
	else:
		print "非法代码:" +code+ "\n"
		exit(1);

deltaV = 0
deltaTg = 0
if pindex==4:
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
while True:
	print "---------------------"
	currentIndexData(url, "s_sh000001")
	if idxCount>=2:
		currentIndexData(url, "s_sz399001")
		currentIndexData(url, "s_sz399005")
		idxCount = 0
	else:
		idxCount += slpTime
	currentIndexData(url, "s_sz399006")
	currentSinaData(url, code, slpTime)

	if exgCount==0:
		print ""
		internal.common.analyze_data(exUrl, code, deltaV, deltaTg, sarr)
		exgCount += slpTime
	elif exgCount>40:
		exgCount = 0
	print "~~~~~~~~~~~~~~~~~~~~~\n"

	now = datetime.datetime.now()
	hour = now.hour
	minute = now.minute
	if (hour<9 or hour>=15):
		break
	elif (hour==9 and minute<15):
		break
	time.sleep(slpTime)
