#!/usr/bin/env python
# -*- coding:gbk -*-
#比较通用、公共的函数实现
import sys
import re
import os
import string
import datetime
import urllib2
import zlib
import pandas as pd
from internal.sina_inf import *

#reload(sys)
#sys.setdefaultencoding('gbk')

c_shcd = ['600', '601', '603', '688']
c_szcd = ['000','001','002','003','300']

url_sn = "http://hq.sinajs.cn/list="
split_ct = 10

def create_column(column):
	c0 = ['code', 'name']
	c1 = ['open', 'p_close', 'price', 'high', 'low']
	c2 = ['bidb','bids','volume','amount']
	c3 = ['b1_v','b1','b2_v','b2','b3_v','b3','b4_v','b4','b5_v','b5']
	c4 = ['s1_v','s1','s2_v','s2','s3_v','s3','s4_v','s4','s5_v','s5']
	c5 = ['date','time','state','']
	column.extend(c0)
	column.extend(c1)
	column.extend(c2)
	column.extend(c3)
	column.extend(c4)
	column.extend(c5)

#字符串转二进制
def char2bin(s):
    return ' '.join([bin(ord(c)).replace('0x', '') for c in s])

#二进制转字符串
def bin2char(s):
    return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])

def quotation_st():
	now = datetime.datetime.now()
	hour = now.hour
	minute = now.minute
	if (hour<9 or hour>15 or hour==12):
		return 0
	elif (hour==9 and minute<15):
		return 0
	elif (hour==15):
		return 0
	elif (hour==9 and (minute>=15 and minute<30)):
		return 1
	else:
		return 2

def timeShow(starttime, line=0):
	endtime = datetime.datetime.now()
	print( "%d: Run Time: %s"%(line, endtime-starttime) )

def sina_code(code):
	ncode = code
	head3 = code[0:3]
	if head3 in c_szcd:
		ncode = 'sz' + code
	elif head3 in c_shcd:
		ncode = 'sh' + code
	else:
		print("Error: Not match code=" + code)
	return ncode

def list_index_info(df, show_idx):
	if df is None:
		return
	for index,row in df.iterrows():
		if row[0] not in show_idx:
			continue

		open = float(row['open'])
		close = float(row['close'])
		preclose = float(row['preclose'])
		print("%8.2f(%6s)"%(close, row[2]))

def list_extra_index(codeArray):
	df = ts.get_realtime_quotes(codeArray)
	for index,row in df.iterrows():
		pre_close = row['pre_close']
		price = row['price']
		f_pclose = float(pre_close)
		f_price = float(price)
		value =  (f_price-f_pclose)*100/f_pclose
		print("%8.2f( %3.2f)"%(f_price, round(value,2)))

#https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks		
#一行代码切片数组，n自定义长度, python2推荐xragne, python3使用range就可以
#new_l = [list[i:i + n] for i in xrange(0, len(list), n)]
#print (new_l)
def list_slice(init_list, children_list_len):
	list_of_groups = zip(*(iter(init_list),) *children_list_len)
	end_list = [list(i) for i in list_of_groups]
	count = len(init_list) % children_list_len
	end_list.append(init_list[-count:]) if count !=0 else end_list
	return end_list

def handle_hq_data(stockData, rt_list):
	#print ("===" + stockData + "===")
	#print ("\n\n")
	stkObjs = stockData.split(';')
	for item in stkObjs:
		if len(item)<10:
			#print("Invalid line=" + item)
			continue
		#print (item)
		#print(encode1(item))

		stkList = []
		obj = re.match(r'\n?var hq_str_(.*)="(.*)"', item)
		if obj is None:
			print("Invalid line=" + item)
			continue
		elif obj.group(2)=="":
			print("No data line=" + item)
			stkList.append(obj.group(1)[2:])
			continue

		#print(obj,obj.group(1),obj.group(2))
		stkList.append(obj.group(1)[2:])
		quotation = obj.group(2)
		dataObj = quotation.split(',')
		for data in dataObj:
			stkList.append(data)
		#特殊处理，沪市深市数据不一致，沪市多了一个','
		if len(stkList)==34:
			stkList.append('')
		rt_list.append(stkList)
		#for END

#沪市的结果最后是 '00,'
#深市的结果最后是 '00'
def req_data(req_url, rt_list):
	retry = 0
	while retry<3:
		try:
			#print(req_url)
			req = urllib2.Request(req_url)
			stockData = urllib2.urlopen(req, timeout=2).read()
		except:
			if retry==2:
				print "URL timeout"
			retry += 1
			continue
		else:
			handle_hq_data(stockData, rt_list)
			break

			'''
			for i in range(0, stockLen):
				sobj = stockObj[i].decode('gbk')
				print u"%02d:	%s" % (i, sobj)
			'''

def realtime_price(stockCode, rt_list, source=0):
	grp_code = list_slice(stockCode, split_ct)
	for item in grp_code:
		req_url = url_sn + ",".join(item)
		req_data(req_url, rt_list)

#对比 get_pre_trade_date(), 从SINA获取的速度更快
def get_his_trade_days(tradeList, len=10, src='sn'):
	if src=='sn':
		code='sh000001'
		scale=240
		ma='no'
		content = get_history_trade_info_bysn(len, code, scale, ma)
		if content is None:
			print("Error: Get for SN fail\n")
			return

		#print(content)
		left = content[1:-1]
		while (1):
			obj = re.match(r'{(.*?)},?(.*)', left)
			if obj is None:
				break
			left = obj.group(2)
			dayObj = re.match(r'day:"(.*?)"', obj.group(1))
			if dayObj is None:
				continue
			tradeList.insert(0, dayObj.group(1))
		return

def get_guben_change(code, src='sn'):
	content = None
	if src=='':
		src='sn'

	if src=='sn':
		content = get_guben_change_bysn(code)
	else:
		print("Not support source", src)

	return content
##	