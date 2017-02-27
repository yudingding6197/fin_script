# -*- coding:gbk -*-
import sys
import re
import os
import time
import datetime
import tushare as ts
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook
from internal.common import *

cmp_string = "20150201"
base_date = datetime.datetime.strptime(cmp_string, '%Y%m%d').date()

prepath = "..\\Data\\"
df = ts.get_stock_basics()
#df.to_csv("aa.csv")
df1 = df.sort_values(['timeToMarket'], 0, False)
#print df1

index = -1

wb = Workbook()
# grab the active worksheet
ws = wb.active
strline = u'代码,名称,是否开板,封板天数,封板价格,上市日期,流通股本,流通市值,总股本,总市值'
strObj = strline.split(u',')
ws.append(strObj)
excel_row = 2
for code,row in df1.iterrows():
	stockInfo = []
	index += 1
	name = row[0].decode('utf8')
	trade_item = row['timeToMarket']
	ltgb = row['outstanding']
	zgb = row['totals']
	#print type(trade_item) 竟然是 long 类型
	trade_string = str(trade_item)
	trade_date = datetime.datetime.strptime(trade_string, '%Y%m%d').date()
	delta = trade_date - base_date
	#print (index+1),code,delta.days,trade_date,base_date
	#print (index+1),code,name,trade_date	
	if delta.days<0:
		break

	#获得每只个股每天交易数据
	tddf = ts.get_k_data(code)
	#print tddf

	b_open = 0
	yzzt_day = 0
	last_close = 0.0
	td_total = len(tddf)
	for tdidx,tdrow in tddf.iterrows():
		open = tdrow[1]
		close = tdrow[2]
		high = tdrow['high']
		low = tdrow['low']
		if high!=low:
			if yzzt_day!=0:
				b_open = 1
				break
		else:
			yzzt_day += 1
		last_close = close

	#追加数据
	ltsz = ltgb*last_close
	zsz = zgb*last_close
	stockInfo.append(code)
	stockInfo.append(name)
	stockInfo.append(b_open)
	stockInfo.append(yzzt_day)
	stockInfo.append(last_close)
	stockInfo.append(trade_item)
	stockInfo.append(ltgb)
	stockInfo.append(round(ltsz,2))
	stockInfo.append(zgb)
	stockInfo.append(round(zsz,2))
	#print stockInfo

	k = 0
	ascid = 65
	number = len(stockInfo)
	for k in range(0,number):
		cell = chr(ascid+k) + str(excel_row)
		ws[cell] = stockInfo[k]
	excel_row += 1

filexlsx = prepath + "cixin_analyze.xlsx"
wb.save(filexlsx)