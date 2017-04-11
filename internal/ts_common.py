#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import string
import datetime
import urllib
import urllib2
import pandas as pd
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook
from common import *
from decimal import Decimal
import ctypes
import tushare as ts

#reload(sys)
#sys.setdefaultencoding('gbk')

STK_ZT = 1<<0
STK_DT = 1<<1
STK_ZTHL = 1<<2
STK_DTFT = 1<<3
STK_YZZT = 1<<4
STK_YZDT = 1<<5
STK_OPEN_ZT = 1<<6
STK_OPEN_DT = 1<<7
STK_ST_YZZT = 1<<8
STK_ST_YZDT = 1<<9

class statisticsItem:
	s_zt = 0
	s_dt = 0
	s_zthl = 0
	s_dtft = 0
	s_yzzt = 0
	s_yzdt = 0
	s_open_zt = 0		#涨停开盘
	s_close_zt = 0		#涨停开盘个股收盘仍涨停
	s_open_T_zt = 0		#涨停开盘个股收盘仍涨停，非一字
	s_zt_o_gt_c = 0		#触及涨停,开盘价高于收盘价
	s_dk_zt = 0			#开盘涨停，收盘打开涨停
	s_open_dt = 0		#跌停开盘
	s_st_yzzt = 0
	s_st_yzdt = 0
	s_open_sz = 0		#开盘上涨
	s_open_xd = 0		#开盘下跌
	s_open_pp = 0		#开盘平盘
	s_open_dz = 0		#开盘大涨
	s_open_dd = 0		#开盘大跌
	s_close_sz = 0		#收盘上涨
	s_close_xd = 0		#收盘下跌
	s_close_pp = 0		#收盘平盘
	s_close_dz = 0		#收盘大涨
	s_close_dd = 0		#收盘大跌
	s_high_zf = 0		#最高涨幅
	s_low_df = 0		#最低跌幅
	s_cx_yzzt = 0		#次新YZZT
	s_new = 0			#上市新股
	s_total = 0			#总计所有交易票
	s_sw_zt = 0			#上午ZT
	s_xw_zt = 0			#下午ZT
	lst_kd = []			#坑爹个股
	lst_nb = []			#NB，低位强拉高位
	lst_jc = []			#韭菜了，严重坑人
	lst_non_yzcx_zt = []		#非次新涨停
	lst_non_yzcx_yzzt = []		#非次新一字涨停
	lst_dt = []					#跌停
	lst_dtft = []				#跌停反弹
	def __init__(self):
		self.s_zt = 0
		self.s_dt = 0
		self.s_zthl = 0
		self.s_dtft = 0
		self.s_yzzt = 0
		self.s_yzdt = 0
		self.s_open_zt = 0
		self.s_close_zt = 0
		self.s_open_T_zt = 0
		self.s_zt_o_gt_c = 0
		self.s_dk_zt = 0
		self.s_open_dt = 0
		self.s_st_yzzt = 0
		self.s_st_yzdt = 0
		self.s_open_sz = 0
		self.s_open_xd = 0
		self.s_open_pp = 0
		self.s_open_dz = 0
		self.s_open_dd = 0
		self.s_close_sz = 0
		self.s_close_xd = 0
		self.s_close_pp = 0
		self.s_close_dz = 0
		self.s_close_dd = 0
		self.s_high_zf = 0
		self.s_low_df = 0
		self.s_cx_yzzt = 0
		self.s_new = 0
		self.s_total = 0
		self.s_sw_zt = 0
		self.s_xw_zt = 0
		self.lst_kd = []
		self.lst_nb = []
		self.lst_jc = []
		self.lst_non_yzcx_zt = []
		self.lst_non_yzcx_yzzt = []
		self.lst_dt = []
		self.lst_dtft = []

def spc_round(value,bit):
	b = int(value*1000)%10
	rd_val=float( '{:.2f}'.format(Decimal(str(value))) )
	if b==5:
		if int(value*100)%2==0:
			rd_val+=0.01
	return round(rd_val,2)

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
	df = None
	try:
		df = ts.get_notices(code, curdate)
	except:
		pass

	if df is None or df.empty:
		df = ts.get_notices(code)
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
		print "%-8s	%6s(%6s,%6s,%6s)	%8s(%8s,%8s)" %(stname, change, change_l, change_h, change_o, price, low, high)

def list_realtime_info(basic, codeArray):
	if len(codeArray)==0:
		return
	df = ts.get_realtime_quotes(codeArray)
	#print df
	#c = df[['name','price','bid','ask','volume','amount','time']]
	#name    open pre_close   price    high     low     bid     ask     volume 
	#amount   ...      a2_p  a3_v    a3_p  a4_v    a4_p  a5_v    a5_p  date      time    code
	print ''
	for index,row in df.iterrows():
		stname = row['name']
		open = row['open']
		pre_close = row['pre_close']
		price = row['price']
		high = row['high']
		low = row['low']
		volume = int(row['volume'])
		if basic is None:
			turnover_rt = 0
		else:
			total_vol = float(basic.ix[codeArray[index]]['outstanding'])
			turnover_rt = ((volume/10000) / (total_vol*100))
			
		price_f = float(price)
		pre_close_f = float(pre_close)
		change = '%02.02f'%( ((price_f-pre_close_f)/pre_close_f)*100 )
		change_l = '%02.02f'%( ((float(low)-pre_close_f)/pre_close_f)*100 )
		change_h = '%02.02f'%( ((float(high)-pre_close_f)/pre_close_f)*100 )
		change_o = '%02.02f'%( ((float(open)-pre_close_f)/pre_close_f)*100 )

		#print change
		print "%-5s	%-6s(%6s%%) (%5.02f%%)	%-6s(%6s) %-6s(%6s)" %(stname, price, change, turnover_rt, low, change_l, high, change_h)
		#print "%5s	%6s(%6s,%6s,%6s)	%8s(%8s,%8s)" %(stname, change, change_l, change_h, change_o, price, low, high)
		
def list_latest_news(codeArray, curdate):
	cur_dt = datetime.datetime.strptime(curdate, '%Y-%m-%d').date()
	for code in codeArray:
		bFlag = 0
		news_ct = 0
		df = ts.get_notices(code)
		for index,row in df.iterrows():
			news_dt = datetime.datetime.strptime(row['date'], '%Y-%m-%d').date()
			delta = cur_dt-news_dt
			if delta.days<=0:
				print "==================================="
				bFlag=1
			else:
				if bFlag==0:
					news_ct += 1
				else:
					break
				if news_ct>1:
					break
			print row['date'],row['title']
		print ''

def show_index_info(df, show_idx):
	if df is None:
		return
	for index,row in df.iterrows():
		if row[0] not in show_idx:
			continue

		open = float(row['open'])
		close = float(row['close'])
		preclose = float(row['preclose'])
		print "%8.2f(%6s)"%(close, row[2])

def check_cx(code):
	if len(code)!=6:
		return 0
	if code.isdigit() is False:
		return 0

	df = ts.get_hist_data(code)
	if df is None:
		return 0
	if len(df)>39:
		return 0

	b_match = 1
	for index,row in df.iterrows():
		open = float(row['open'])
		close = float(row['close'])
		high = float(row['open'])
		low = float(row['close'])
		p_change = float(row['p_change'])
		if p_change>12:
			continue
		if open==close and low==high and p_change>1:
			pass
		else:
			b_match = 0
			break
	return b_match

#通过分时得到ZT时间，上午or下午
def zt_time_point(code, zt_price, trade_date, stcsItem):
	excecount = 0
	df = None
	while excecount<=3:
		try:
			df = ts.get_k_data(code, ktype='60')
		except:
			excecount += 1
		else:
			break
	if df is None:
		return

	df_today = df.loc[df['date'].str.contains(str(trade_date))]
	if len(df_today)<=0:
		#print "Not find data"
		return
	j=1
	#读出的数据就是float类型
	#通过定义区间，记录ZT的时间段
	#1:[9:30-10:30],2:[10:30-11:30]...
	for index,row in df_today.iterrows():
		high = row['high']
		if high==zt_price:
			if j<3:
				stcsItem.s_sw_zt += 1
			else:
				stcsItem.s_xw_zt += 1
			break
		else:
			j += 1
	return

#分析此单的状态：ZT、DT、ZTHL、DTFT...，详见 statisticsItem 定义
def analyze_status(code, name, row, stcsItem, yzcx_flag, pd_list, trade_date):
	if len(code)!=6:
		return 0
	if code.isdigit() is False:
		return 0

	status = 0
	high = round(float(row['high']),2)
	low = round(float(row['low']),2)
	open = round(float(row['open']),2)
	price = round(float(row['price']),2)
	pre_close = round(float(row['pre_close']),2)
	volume = int(row['volume'])

	#排除当天没有交易
	if pre_close==0:
		print "PRE_CLOSE Not exist!!!", code, name
		return 0

	if high==0 or low==0:
		return 0

	b_ST = 0
	if name.find("ST")>=0 or name.find("st")>=0:
		b_ST = 1
		#print code,name

	o_percent = (open-pre_close)*100/pre_close
	c_percent = (price-pre_close)*100/pre_close
	h_percent = (high-pre_close)*100/pre_close
	l_percent = (low-pre_close)*100/pre_close
	open_percent = spc_round(o_percent,2)
	change_percent = spc_round(c_percent,2)
	high_zf_percent = spc_round(h_percent,2)
	low_df_percent = spc_round(l_percent,2)

	#获取ZT
	if b_ST==1:
		zt_price1 = pre_close * 1.05
		dt_price1 = pre_close * 0.95
	else:
		zt_price1 = pre_close * 1.1
		dt_price1 = pre_close * 0.9
	zt_price = spc_round(zt_price1,2)
	dt_price = spc_round(dt_price1,2)

	#YZ状态处理
	if high==low:
		if open>pre_close:
			if b_ST==1 and high==zt_price:
				stcsItem.s_st_yzzt += 1
				status |= STK_ST_YZZT
			elif b_ST==0 and high==zt_price:
				if high_zf_percent>15:
					pass
				else:
					stcsItem.s_yzzt += 1
					status |= STK_YZZT
					stcsItem.s_zt += 1
					status |= STK_ZT
					stcsItem.s_open_zt += 1
					status |= STK_OPEN_ZT
					stcsItem.s_close_zt += 1
					#list = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent]
					#pd_list.append(list)
					if yzcx_flag==0:
						list = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent]
						stcsItem.lst_non_yzcx_yzzt.append(list)
					#print stcsItem.s_zt,code,name,price,change_percent,open
		elif open<pre_close:
			if b_ST==1:
				stcsItem.s_st_yzdt += 1
				status |= STK_ST_YZDT
			else:
				stcsItem.s_yzdt += 1
				status |= STK_YZDT
				stcsItem.s_dt += 1
				status |= STK_DT
				stcsItem.s_open_dt += 1
				status |= STK_OPEN_DT

				list = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent]
				stcsItem.lst_dt.append(list)
		#print code,name,open,low,high,price,pre_close
	else:
		if high==zt_price:
			if b_ST==0:
				if price==zt_price:
					#仅仅计算最后还是ZT的item
					zt_time_point(code, zt_price, trade_date, stcsItem)
					stcsItem.s_zt += 1
					status |= STK_ZT
					if open==zt_price:
						stcsItem.s_open_zt += 1
						status |= STK_OPEN_ZT
						if price==open:
							stcsItem.s_close_zt += 1
							stcsItem.s_open_T_zt += 1
					#list = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent]
					#pd_list.append(list)
					if yzcx_flag==0:
						list = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent]
						stcsItem.lst_non_yzcx_zt.append(list)
				else:
					stcsItem.s_zthl += 1
					status |= STK_ZTHL
					if open==zt_price:
						stcsItem.s_open_zt += 1
						status |= STK_OPEN_ZT
						stcsItem.s_dk_zt += 1
						#print stcsItem.s_zthl,code,name,price,high,zt_price
				if change_percent<=3:
					stcsItem.lst_kd.append(name)
				if price<open:
					stcsItem.s_zt_o_gt_c += 1

		if low==dt_price:
			if b_ST==0:
				if price==dt_price:
					stcsItem.s_dt += 1
					status |= STK_DT
					if open==dt_price:
						stcsItem.s_open_dt += 1
						status |= STK_OPEN_DT

					#DT Data
					list = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent]
					stcsItem.lst_dt.append(list)
				else:
					stcsItem.s_dtft += 1
					status |= STK_DTFT

					#DTFT Data
					list = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent]
					stcsItem.lst_dtft.append(list)

	#统计开盘涨跌幅度
	if open_percent>0:
		stcsItem.s_open_sz += 1
		if open_percent>=4.0:
			stcsItem.s_open_dz += 1
	elif open_percent<0:
		stcsItem.s_open_xd += 1
		if open_percent<=-4.0:
			stcsItem.s_open_dd += 1
	else:
		stcsItem.s_open_pp += 1

	#统计开盘涨跌幅度
	if change_percent>0:
		stcsItem.s_close_sz += 1
		if change_percent>=4.0:
			stcsItem.s_close_dz += 1
	elif change_percent<0:
		stcsItem.s_close_xd += 1
		if change_percent<=-4.0:
			stcsItem.s_close_dd += 1
	else:
		stcsItem.s_close_pp += 1
	stcsItem.s_total += 1

	#统计最大涨跌幅度
	if high_zf_percent>=4.0:
		stcsItem.s_high_zf += 1
	if low_df_percent<=-4.0:
		stcsItem.s_low_df += 1

	#统计表现震撼个股 通过成交量排除新股
	zf_range = high_zf_percent-low_df_percent
	if zf_range>=15.0 and volume>100000:
		if change_percent>=6.0:
			list = [code, name, change_percent, price, zf_range]
			stcsItem.lst_nb.append(list)
		elif change_percent<=-6.0:
			list = [code, name, change_percent, price, zf_range]
			stcsItem.lst_jc.append(list)
	return status

#建议在之前调用debug\instant_data.py更新所有数据，在Data\entry\trade\trade_last.txt保存
def get_guben_line(url_str, code):
	url = url_str % (code)
	#print url
	guben_info = None
	excecount = 0
	while excecount<=3:
		try:
			req = urllib2.Request(url)
			guben_info = urllib2.urlopen(req, timeout=5).read()
		except:
			excecount += 1
		else:
			break
	if guben_info is None:
		print "Fail to get data"
		return None
	#找到匹配数据
	start = guben_info.find("<set name='")
	if start<0:
		return None
	end = guben_info[start:].find("</graph>")
	if end<0:
		return None
	return guben_info[start:start+end]

def parse_guben(gb_str, gb_list):
	while gb_str:
		rec = []
		obj = re.match(r'<set name=\'.*?\' value=\'(.*?)\' hoverText=\'(.*?)\'/>(.*)', gb_str)
		#print obj,obj.group(1),obj.group(2)
		rec.append(obj.group(2))
		if obj.group(1)=='':
			rec.append(0)
		else:
			rec.append(float(obj.group(1)))
		gb_list.append(rec)
		gb_str = obj.group(3)
	return