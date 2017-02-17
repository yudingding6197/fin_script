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
from common import *
import ctypes
import tushare as ts

#reload(sys)
#sys.setdefaultencoding('gbk')

def ts_handle_data(addcsv, prepath, bhist, url, code, qdate, sarr):
	todayUrl = "http://hq.sinajs.cn/list=" + code
	#if Handle_Mid==0:
	#	print "Message: Ignore 中性盘"

	if not os.path.isdir(prepath):
		os.makedirs(prepath)

	dataObj = []
	if cmp(sarr, '')==0:
		sarr = dftsarr
	volObj = sarr.split(',')
	arrlen = len(volObj)
	for i in range(0,arrlen):
		obj = fitItem(int(volObj[i]))
		dataObj.append(obj)

	wb = Workbook()
	# grab the active worksheet
	ws = wb.active

	totalline = 0
	filename = code+ '_' + qdate
	fctime = ''
	todayData = []
	todayDataLen = 0
	bGetToday = 0
	last_close = 0

	cur=datetime.datetime.now()
	if bhist==0:
		fctime = '%02d:%02d' %(cur.hour, cur.minute)
		filename = '%s_%02d-%02d' %(filename, cur.hour, cur.minute)
		bGetToday = 1
	if (bhist==2 and cur.hour>=15 and cur.minute>0):
		bGetToday = 1
	if (bGetToday==1):
		try:
			req = urllib2.Request(todayUrl)
			stockData = urllib2.urlopen(req, timeout=5).read()
		except:
			loginfo(1)
			print "URL timeout"
		else:
			stockObj = stockData.split(',')
			if len(stockObj)<10:
				print code, ": No trade data"
				return -1
			
			closePrice = float(stockObj[3])
			lastClsPrice = float(stockObj[2])
			last_close = lastClsPrice
			openPrice = float(stockObj[1])
			highPrice = float(stockObj[4])
			lowPrice = float(stockObj[5])
			exVolume = int(stockObj[8])/100
			exAmount = float(stockObj[9])
			f1 = '%02.02f'%( ((closePrice-lastClsPrice)/lastClsPrice)*100 )
			exFluc = float(f1)
			
			todayData.append(closePrice)
			todayData.append(exFluc)
			todayData.append(lastClsPrice)
			todayData.append(openPrice)
			todayData.append(highPrice)
			todayData.append(lowPrice)
			todayData.append(exVolume)
			todayData.append(exAmount)
			todayDataLen = len(todayData)

	if addcsv==1:
		filecsv = prepath + filename + '.csv'
		fcsv = open(filecsv, 'w')
		strline = '成交时间,成交价,涨跌幅,价格变动,成交量,成交额,性质'
		fcsv.write(strline)
		fcsv.write("\n")

	strline = u'成交时间,成交价,涨跌幅,价格变动,成交量,成交额,性质,收盘价,涨跌幅,前收价,开盘价,最高价,最低价,成交量,成交额'
	strObj = strline.split(u',')
	ws.append(strObj)

	stockInfo = []
	#每一页的数据，如果找到匹配数据则设置为1；解决有时候页面有数据但是收不到，
	#count为0，重新加载尝试再次获取；如果解析到数据的页面，如果count为0就不再继续解析数据
	matchDataFlag = 0
	excecount = 0
	savedTrasData = []
	savedTrasData2 = []
	largeTrasData = []
	i = 1

	curcode = code
	if len(code)==8:
		curcode = code[2:8]

	#历史当天行情数据通过此方法获得
	if bhist==1:
		df = ts.get_hist_data(curcode, start=qdate, end=qdate)
		if df is None or df.empty or len(df)!=1:
			print qdate, ": No data"
			return -1
		#print qdate, df
		for index,row in df.iterrows():
			last_close = float(row['close'])-float(row['price_change'])
			stockInfo.append(row['close'])
			stockInfo.append(row['p_change'])
			stockInfo.append(last_close)
			stockInfo.append(row['open'])
			stockInfo.append(row['high'])
			stockInfo.append(row['low'])
			stockInfo.append(row['volume'])
			stockInfo.append(row['turnover'])

	while excecount<=3:
		if bhist==0:
			df = ts.get_today_ticks(curcode)
		else:
			df = ts.get_tick_data(curcode, qdate)
		#print df
		if df is None:
			excecount += 1
			continue;
		if df.size==18:
			excecount += 1
			continue;
		else:
			break;
		
	#尝试3次，检查结果
	if df is None:
		print qdate, ": None Object"
		return -1
	if df.size==18:
		print qdate, ": Fail to get data"
		return -1

	for index,row in df.iterrows():
		curtime = row['time']
		curprice = row['price']
		range_per = ''
		if last_close!=0:
			range_val = ((float(curprice)-last_close) * 100) / last_close
			range_per = round(range_val, 2)
		fluctuate = row['change']
		curvol = int(row['volume'])
		volume = curvol
		amount = row['amount']
		if bhist==0:
			state = row['type']
		else:
			state = row['type'].decode('utf-8')
		#print state.decode('utf8')

		ret,hour,minute,second = parseTime(curtime)
		if (ret==-1):
			continue
		if (int(amount)==0 and not (hour==15 and minute==0)):
			continue

		bAddVolumn = 1
		if (hour==9 and minute==25) or (hour==15 and minute==0):
			bAddVolumn = 0

		stateStr = state
		st_buy = '买盘'.decode('gbk')
		st_sell = '卖盘'.decode('gbk')
		st_mid = '中性盘'.decode('gbk')
		if cmp(state, st_sell)==0:
			if bAddVolumn==1:
				handle_volumn(volume, dataObj, 2)
			stateStr = 'SELL卖盘'.decode('gbk')
		elif cmp(state, st_buy)==0:
			if bAddVolumn==1:
				handle_volumn(volume, dataObj, 1)
		#目前中性盘没有处理
		elif cmp(state, st_mid)==0:
			if bAddVolumn==1:
				ret = handle_middle_volumn(volume, dataObj, curtime, fluctuate, 0)
			else:
				ret = 0
			if ret==1:
				stateStr = st_buy
			elif ret==2:
				stateStr = st_sell

		if addcsv==1:
			strline = curtime +","+ curprice +","+ range_per +","+ fluctuate +","+ curvol +","+ amount +","+ stateStr + "\n"
			fcsv.write(strline)

		totalline += 1
		row = totalline+1
		price = float(curprice)
		cell = 'A' + str(row)
		ws[cell] = curtime
		cell = 'B' + str(row)
		ws[cell] = price
		cell = 'C' + str(row)
		ws[cell] = range_per
		cell = 'D' + str(row)
		ftfluct = fluctuate
		if (fluctuate=='--'):
			ws[cell] = fluctuate
		else:
			ftfluct = float(fluctuate)
			ws[cell] = ftfluct
		cell = 'E' + str(row)
		ws[cell] = curvol
		cell = 'F' + str(row)
		ws[cell] = int(amount)
		cell = 'G' + str(row)
		s1 = stateStr
		ws[cell] = s1

		#将当天的数据在Sheet页面更新
		if (row==2 and (bhist==0 or bhist==1 or (bhist==2 and cur.hour>=15)) and todayDataLen>0):
			ascid = 72
			for k in range(0, todayDataLen):
				cell = chr(ascid+k) + str(row)
				ws[cell] = todayData[k]

		#将开始和最后成交数据保存
		bSaveFlag = 0
		if (totalline==1 or (totalline<4 and curvol>100)):
			bSaveFlag = 1
		elif (hour==9 and minute==30 and curvol>300) or (hour==9 and minute<30):
			bSaveFlag = 2
		if bSaveFlag==1 or bSaveFlag==2:
			rowData = []
			rowData.append(curtime)
			rowData.append(price)
			rowData.append(range_per)
			rowData.append(ftfluct)
			rowData.append(curvol)
			rowData.append(int(amount))
			rowData.append(s1)
		if bSaveFlag==1:
			savedTrasData.append(rowData)
		elif bSaveFlag==2:
			savedTrasData2.append(rowData)

		#增加大单成交记录
		if (curvol>=Large_Volume):
			rowData = []
			rowData.append(curtime)
			rowData.append(price)
			rowData.append(range_per)
			rowData.append(ftfluct)
			rowData.append(curvol)
			rowData.append(int(amount))
			rowData.append(s1)
			largeTrasData.append(rowData)

		if (row==2 and bhist==1):
			ascid = 72
			number = len(stockInfo)
			for k in range(0,number):
				cell = chr(ascid+k) + str(row)
				ws[cell] = stockInfo[k]

	ws.auto_filter.ref = "A1:G1"

	if addcsv==1:
		fcsv.close()
		if (totalline==0):
			os.remove(filecsv)

	if totalline>0:
		startIdx = 0
		savedTrasLen = len(savedTrasData2)
		if savedTrasLen>0:
			if savedTrasLen>Tras_Count:
				startIdx = savedTrasLen-Tras_Count
			for j in range(startIdx, savedTrasLen):
				savedTrasData.append(savedTrasData2[j])
		ws = wb.create_sheet()
		write_statics(ws, fctime, dataObj, qdate, savedTrasData, largeTrasData)

	filexlsx = prepath +filename+ '.xlsx'
	if (os.path.exists(filexlsx) and bhist==0):
		j = 1
		while True:
			filexlsx = prepath + filename + '_' + str(j) + '.xlsx'
			j += 1
			if not os.path.exists(filexlsx):
				break;

	wb.save(filexlsx)
	return 0

def ts_analyze_data(url, code, sarr, priceList, contPrice):
	url = url +"?symbol="+ code
	dataObj = []
	if cmp(sarr, '')==0:
		sarr = dftsarr
	volObj = sarr.split(',')
	arrlen = len(volObj)
	for i in range(0,arrlen):
		obj = fitItem(int(volObj[i]))
		dataObj.append(obj)
	dataObjLen = len(dataObj)

	totalline = 0
	#可能数据在不同的页面，同时存在，这是重复数据需要过滤重复结果
	#还可能相同时间，产生多个成交量，需要都保留
	lasttime = ''
	lastvol = 0
	pageFtime = ''
	bFtime = 0
	hisUrl = ''
	fctime = ''
	todayData = []
	todayDataLen = 0
	bGetToday = 0

	cur=datetime.datetime.now()

	strline = u'成交时间,成交价,涨跌幅,价格变动,成交量,成交额,性质,收盘价,涨跌幅,前收价,开盘价,最高价,最低价,成交量,成交额'
	strObj = strline.split(u',')
	#dtlRe = re.compile(r'\D+(\d{2}:\d{2}:\d{2})\D+(\d+.\d{1,2})</td><td>(\+?-?\d+.\d+%)\D+(--|\+\d+.\d+|-\d+.\d+)\D+(\d+)</td><td>([\d,]+)</td><th><h\d+>(卖盘|买盘|中性盘)\D')
	dtlRe = re.compile(r'\D+(\d{2}:\d{2}:\d{2})\D+(\d+.\d{1,2})</td><td>(\+?-?\d+.\d+%)\D+(--|\+\d+.\d+|-\d+.\d+)\D+(\d+)</td><td>([\d,]+)</td><th>(.*)\D')
	frameRe = re.compile(r'.*name=\"list_frame\" src=\"(.*)\" frameborder')
	keyw = '收盘价|涨跌幅|前收价|开盘价|最高价|最低价|成交量|成交额'
	infoRe = re.compile(r'\D+('+keyw+').*>(\+?-?\d+\.\d+)')
	excecount = 0
	stockInfo = []
	reloadUrl = 0
	noDataFlag = 0
	noDataKey = "该股票没有交易数据"
	notTrasFlag = 0
	notTrasKey = "输入的日期为非交易日期"
	#每一页的数据，如果找到匹配数据则设置为1；解决有时候页面有数据但是收不到，
	#count为0，重新加载尝试再次获取；如果解析到数据的页面，如果count为0就不再继续解析数据
	matchDataFlag = 0
	i = 1
	lineCount = 0
	firstHour = 0
	firstMinute = 0
	firstSecond = 0
	minValue = 0
	maxValue = 0
	curValue = 0
	tmpContPrice = []
	pageIdx = 1
	bAlert = 0
	bLastAlert = 0

	st_buy = '买盘'.decode('gbk')
	st_sell = '卖盘'.decode('gbk')
	st_mid = '中性盘'.decode('gbk')

	#临时处理方案，对国债逆回购
	head5 = code[0:5]
	bBigChange = (cmp(head5, "sz131")==0) or (cmp(head5, "sh204")==0)

	#获取当天所有分笔交易
	curcode=code
	if len(code)==8:
		curcode=code[2:8]
	while excecount<=3:
		df = ts.get_today_ticks(curcode)
		if df is None:
			excecount += 1
			continue
		excecount += 1
		if df.size>0:
			break

	print ""
	#尝试3次，检查结果
	if df is None:
		print curcode, ": None Object"
		return -1
	if df.size==0:
		print curcode, ": Fail to get today ticks"
		return -1

	for index,row in df.iterrows():
		curtime = row['time']
		curprice = row['price']
		range_per = ''
		#if last_close!=0:
		#	range_val = ((float(curprice)-last_close) * 100) / last_close
		#	range_per = round(range_val, 2)
		fluctuate = row['change']
		curvol = int(row['volume'])
		volume = curvol
		amount = row['amount']
		state = row['type']#.decode('utf8')
		lasttime = curtime
		lastvol = curvol
		volume = curvol
		#print curtime,curprice,row['pchange'],row['change'],curvol,amount,row['type'],state

		ret,hour,minute,second = parseTime(curtime)
		if (ret==-1):
			continue
		if (curprice=="0.00") or (fluctuate=="-100.00%"):
			print "page(%d) Price(%s) or range(%s) is invalid value"%(i, key.group(2), key.group(3))
			continue
		if (hour==9 and minute<=20) or (hour==15 and minute>1):
			count += 1
			continue

		if curvol>Large_Volume:
			#记录成交时间，判断防止数据重复
			bFind = 0
			for k in range(0, len(Large_Vol_Time)):
				if (curtime==Large_Vol_Time[k]):
					bFind=1
					break
			if bFind==0:
				Large_Vol_Time.append(curtime)
				sv = ''
				if state==st_sell:
					sv = 'S'
				elif state==st_buy:
					sv = 'B'
				elif state==st_mid:
					sv = 'M'

				#15分钟内的大单
				bMatch = time_range(firstHour, firstMinute, hour, minute, 15)
				if bMatch==1:
					if not bBigChange:
						msgstr = u'Hello Big_DT (%s	%s:%d)'%(curtime, sv, curvol)
						ctypes.windll.user32.MessageBoxW(0, msgstr, '', 0)

		if curvol>=300:
			if (len(tmpContPrice)==0):
				if (state==st_sell or state==st_buy):
					tmpContPrice.append(state)
					tmpContPrice.append(1)
					tmpContPrice.append(curvol)
			else:
				stateValue = tmpContPrice[0]
				allowAdd = tmpContPrice[1]
				if (allowAdd==1):
					if cmp(stateValue, state)==0:
						tmpContPrice.append(curvol)
					else:
						if state==st_sell:
							tmpContPrice[1] = 0
						elif state==st_buy:
							tmpContPrice[1] = 0
						elif state==st_mid:
							tmpContPrice.append(curvol)
			bAlert = handle_last_price(tmpContPrice, contPrice)
			if bLastAlert==1 and bAlert==0:
				print "Price=", contPrice
				totalVol = 0
				contPriceLen = len(contPrice)
				for k in range(0, contPriceLen):
					totalVol += contPrice[k]
				sv = 'BB'
				if tmpContPrice[0]==st_sell:
					sv = 'SS'
				if not bBigChange:
					msgstr = u'Continued(%s) %d: %d'%(sv, contPriceLen, totalVol/contPriceLen)
					ctypes.windll.user32.MessageBoxW(0, msgstr, '', 0)
				bLastAlert = bAlert
			elif bAlert==1 and bLastAlert==0:
				bLastAlert = bAlert

	priceList[0] = curValue
	priceList[1] = int(curValue*100)
	priceList[2] = minValue
	priceList[3] = maxValue

def list_stock_news(code, curdate, file):
	df = ts.get_notices(code, curdate)
	for index,row in df.iterrows():
		if index>1:
			break
		print row['date'],row['title']
	print ''

def list_stock_rt(codeArray, curdate, file):
	if len(codeArray)==0:
		return
	df = ts.get_realtime_quotes(codeArray)
	#c = df[['name','price','bid','ask','volume','amount','time']]
	print ''
	for index,row in df.iterrows():
		stname = row['name']
		open = row['open']
		pre_close = row['pre_close']
		price = row['price']
		high = row['high']
		low = row['low']

		price_f = float(price)
		pre_close_f = float(pre_close)
		change = '%02.02f'%( ((price_f-pre_close_f)/pre_close_f)*100 )
		change_l = '%02.02f'%( ((float(low)-pre_close_f)/pre_close_f)*100 )
		change_h = '%02.02f'%( ((float(high)-pre_close_f)/pre_close_f)*100 )
		change_o = '%02.02f'%( ((float(open)-pre_close_f)/pre_close_f)*100 )
		#print change
		#print "%10s	" %(stname, change)
		print "%5s	%6s(%6s,%6s,%6s)	%8s(%8s,%8s)" %(stname, change, change_l, change_h, change_o, price, low, high)