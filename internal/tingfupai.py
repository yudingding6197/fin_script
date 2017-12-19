#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import urllib2
import datetime
from ts_common import *

def get_date_with_last():
	today = datetime.date.today()
	curdate = ''
	bLast = 0

	pindex = len(sys.argv)
	lastdt = get_last_trade_dt()
	if (pindex == 1):
		curdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)
		edate = datetime.datetime.strptime(curdate, '%Y-%m-%d').date()
		#如果是当日的数据通过history链接目前不能得到，所以暂时得到前一天的数据
		#今日数据通过getToday获取
		#edate = edate - delta1
		
		#目前通过周六日进行简单判断
		#ts.is_holiday()  or chk_holiday()
		today = datetime.datetime.strptime(curdate, '%Y-%m-%d')
		if today.isoweekday() in [6, 7]:
			curdate = lastdt
		bLast = 1
	else:
		curdate = sys.argv[1]
		if curdate=='.':
			curdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)
		else:
			ret,curdate = parseDate(sys.argv[1], today)
			if ret==-1:
				exit(1)
			if curdate==lastdt:
				bLast = 1
	return curdate, bLast

def get_tingfupai_res(curdate):
	url = "http://www.cninfo.com.cn/information/memo/jyts_more.jsp?datePara="
	urlall = url + curdate

	LOOP_COUNT = 0
	res_data=None
	while LOOP_COUNT<3:
		try:
			req = urllib2.Request(urlall)
			res_data = urllib2.urlopen(req)
		except:
			print "Error fupai urlopen"
			LOOP_COUNT = LOOP_COUNT+1
		else:
			break
	return res_data

def get_all_fupai_data(res_data, fl, detail, curdate, stockCode, stockName):
	totalline = 0
	flag = 0
	count = 0
	ignore = 0
	line = res_data.readline()
	checkStr = '复牌日'
	stockIdx = -1
	while line:
	#	print line
		if flag==0:
			index = line.find(checkStr)
			if (index>=0):
				flag = 1
			line = res_data.readline()
			continue

		key = re.match(r'.+fulltext.+\'(\d+)\',\'(\d+)\'', line)
		if key:
			#print key.groups()
			#读取每一行，首先得到ST代码
			code = key.group(1)
			if (len(code) == 6):
				head3 = code[0:3]
				result = (cmp(head3, "000")==0) or (cmp(head3, "002")==0) or (cmp(head3, "300")==0)
				if result is True:
					stockCode.append(code)
					stockIdx += 1
					fl.write(code + ' ')
				else:
					result = (cmp(head3, "600")==0) or (cmp(head3, "601")==0) or (cmp(head3, "603")==0)
					if result is True:
						stockCode.append(code)
						stockIdx += 1
						fl.write(code + ' ')
					else:
						ignore = 1
			else:
				print "Invalid code:" +code

			#解析完此行，继续下一行
			line = res_data.readline()
			continue
		key = re.match(r'(.+)(</a></td>)', line)
		if key:
			#print key.groups()
			#再读取代码对应的名字
			if ignore==0:
				codename = key.group(1)
				fl.write(codename)
				fl.write("\n")
				print "====",stockCode[stockIdx],codename.decode('gbk')
				stockName.append(codename.decode('gbk'))
				if detail==1:
					list_stock_news(stockCode[stockIdx], curdate, None)
				totalline += 1
			count = 0
			ignore = 0
			line = res_data.readline()
			continue
		count += 1
		if (count>2):
			break;
		line = res_data.readline()
	return totalline

def get_zdt_st(name, p_change, change_l, change_h, change_o):
	st=''
	bst=0
	if name.find("ST")>=0 or name.find("st")>=0:
		bst=1
	#print p_change, change_l, change_h, change_o
	if change_l==change_h:
		if bst==1 and p_change>4.9:
			st = 'YZZZZT'
		elif bst==0 and p_change>9.9:
			st = 'YZZZZT'
		elif bst==1 and p_change<-4.9:
			st = 'YZDDDT'
		elif bst==0 and p_change<-9.9:
			st = 'YZDDDT'
	elif p_change==change_h:
		if p_change>9.9:
			st = 'ZT'
	elif p_change==change_l:
		if p_change<-9.9:
			st = 'DT'
	return st

#将该票实时行情输出，不保存到文件
def list_stock_rt(codeArray, curdate, file=None):
	if len(codeArray)==0:
		return
	df = ts.get_realtime_quotes(codeArray)
	for index,row in df.iterrows():
		stname = row['name']
		open = row['open']
		pre_close = row['pre_close']
		price = row['price']
		high = row['high']
		low = row['low']

		price_f = float(price)
		pre_close_f = float(pre_close)
		if high=='0.000' and low=='0.000':
			change = '%02.02f'%(0)
			change_l = '%02.02f'%(0)
			change_h = '%02.02f'%(0)
			change_o = '%02.02f'%(0)
		else:
			change = '%02.02f'%( ((price_f-pre_close_f)/pre_close_f)*100 )
			change_l = '%02.02f'%( ((float(low)-pre_close_f)/pre_close_f)*100 )
			change_h = '%02.02f'%( ((float(high)-pre_close_f)/pre_close_f)*100 )
			change_o = '%02.02f'%( ((float(open)-pre_close_f)/pre_close_f)*100 )
		st = get_zdt_st(stname, float(change), float(change_l), float(change_h), float(change_o))
		print "%-8s	%8s(%8s,%8s,%8s)	%8s(%8s,%8s)	%8s" %(stname, change, change_l, change_h, change_o, price, low, high, st)

def list_fupai_trade(codeArray, nameArray, curdate, file=None):
	if len(codeArray)==0:
		return
	i = 0
	for code in codeArray:
		stname = nameArray[i]
		i += 1

		df = ts.get_hist_data(code)
		row=df.ix[[curdate]]
		open = row['open']
		price = row.ix[0,'close']
		high = row.ix[0,'high']
		low = row.ix[0,'low']
		p_change = row.ix[0,'p_change']
		turnover = row.ix[0,'turnover']
		pre_close_f = round(price/(1+p_change/100), 2)
		#print pre_close
		change_l = '%02.02f'%( ((float(low)-pre_close_f)/pre_close_f)*100 )
		change_h = '%02.02f'%( ((float(high)-pre_close_f)/pre_close_f)*100 )
		change_o = '%02.02f'%( ((float(open)-pre_close_f)/pre_close_f)*100 )
		change = p_change
		
		st = get_zdt_st(float(p_change), float(change_l), float(change_h), float(change_o))
		print "%-8s	%8s(%8s,%8s,%8s)	%8s(%8s,%8s)	%8s" %(stname, change, change_l, change_h, change_o, price, low, high, st)


