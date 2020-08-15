#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import urllib
import urllib2
import datetime
import json
import copy

from internal.url_juchao.tips_res import *
from global_var import g_shcd
from global_var import g_szcd

'''
{u'obModtime0111': 1595424980000L, 
u'obIsvalid0111': u'1', 
u'obRectime0111': 1595424980000L, 
u'f010v0111': u'Delisting Risk Warning Removal Announcement/Delisting Risk Warning Removal/Risk Warning', 
u'obSeqId': 6115954884L, 
u'lastMtime': 1595424984000L, 
u'obSeccode0111': u'000611', 
u'f004v0111': u'\u505c\u724c1\u5929', 
u'f001d0111': 1595467800000L, 
u'f006v0111': u'A\u80a1', 
u'f002d0111': 1595554200000L, 
u'tradeType': None, 
u'f005v0111': u'\u64a4\u9500\u9000\u5e02\u98ce\u9669\u8b66\u793a\u516c\u544a', 
u'f009v0111': u'Trading Suspension for 1 Day', u'obMemo0111': None, 
u'obSecname0111': u'*ST\u5929\u9996', 
u'f007v0111': u'001001', 
u'obObjectId': 1001126068
}
{
"date":"2020-07-24",
"error":null,
"szshSRTbTrade0111":
	{
	"suspensionTbTrades":[
		{"f001d0111":1595554200000,"obSeccode0111":"002473","obSecname0111":"圣莱达","f002d0111":1595813400000,"f004v0111":"停牌1天","f005v0111":"实行其他风险警示","obMemo0111":null,"obRectime0111":1595513775000,"obModtime0111":1595513775000,"obIsvalid0111":"1","obObjectId":1002380879,"f006v0111":"A股","f007v0111":"001001","obSeqId":6123826506,"f009v0111":"Trading Suspension for 1 Day","f010v0111":"Risk Warning","lastMtime":1595513778000,"tradeType":null},
		{"f001d0111":1595554201000,"obSeccode0111":"300853","obSecname0111":"N申昊","f002d0111":1595556002000,"f004v0111":null,"f005v0111":"盘中临时停牌","obMemo0111":null,"obRectime0111":1595555057000,"obModtime0111":1595555057000,"obIsvalid0111":"1","obObjectId":1002792209,"f006v0111":"A股","f007v0111":"001001","obSeqId":6127218036,"f009v0111":null,"f010v0111":null,"lastMtime":1595555062000,"tradeType":null},
	"resumptionTbTrades":[
		{
		"f001d0111":1595467800000,
		"obSeccode0111":"000611",
		"obSecname0111":"*ST天首",
		"f002d0111":1595554200000,
		"f004v0111":"停牌1天",
		"f005v0111":"撤销退市风险警示公告",
		"obMemo0111":null,
		"obRectime0111":1595424980000,
		"obModtime0111":1595424980000,
		"obIsvalid0111":"1",
		"obObjectId":1001126068,
		"f006v0111":"A股",
		"f007v0111":"001001",
		"obSeqId":6115954884,
		"f009v0111":"Trading Suspension for 1 Day",
		"f010v0111":"Delisting Risk Warning Removal Announcement/Delisting Risk Warning Removal/Risk Warning",
		"lastMtime":1595424984000,
		"tradeType":null
		}
		],
	"keepSuspensionTbTrades":null
	},
'''
def get_all_fupai_data(res_data, fl, detail, curdate, stockCode, stockName):
	totalline = 0
	flag = 0
	count = 0
	ignore = 0
	line = res_data.readline()
	checkStr = '复牌日'
	stockIdx = -1
	while line:
		#print line
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
				if head3 in g_szcd:
					stockCode.append(code)
					stockIdx += 1
					fl.write(code + ' ')
				else:
					if head3 in g_shcd:
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
		print "%-8s	%8s(%8s,%8s,%8s)	%8s(%8s,%8s)	%8s" %(stname, change, change_o, change_h, change_l, price, high, low, st)
	return

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
		st = get_zdt_st(stname, float(p_change), float(change_l), float(change_h), float(change_o))
		print "%-8s	%8s(%8s,%8s,%8s)	%8s(%8s,%8s)	%8s" %(stname, change, change_o, change_h, change_l, price, high, low, st)
	return

def pickup_tingpai_item(curdate, tp_list):
	res_data = get_tingfupai_res(curdate)
	if res_data is None:
		return None

	s = json.loads(res_data)
	print ("WIP ...")
	item = s["szshSRTbTrade0111"]["suspensionTbTrades"]
	for i in item:
		tp_list.append(copy.deepcopy(i))

def pickup_fupai_item(curdate, fp_list, fp_code_list=None):
	res_data = get_tingfupai_res(curdate)
	if res_data is None:
		return

	s = json.loads(res_data)
	resumpObj = s["szshSRTbTrade0111"]["resumptionTbTrades"]
	if resumpObj is None:
		return
	for item in resumpObj:
		#print "pickup_tfp", item
		fp_list.append(copy.deepcopy(item))
		#print item['obSeccode0111']
		if fp_code_list is not None:
			fp_code_list.append(item['obSeccode0111'])
	return