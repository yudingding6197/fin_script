#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import re
import os
import time
import string
import datetime
import platform
import shutil
import getopt
import urllib2,time
import datetime
import threading

from internal.url_dfcf.dc_hangqing import *
from internal.url_dfcf.dc_hq_push import *
from internal.url_163.service_163 import *
from internal.global_var import *
from internal.trade_date import *

TS_FLAG = 1

#通过不同的链接获取信息
URL_TYPE = 2

#分析时间得到ZT时间，上午or下午
# TODO:
def zt_time_analyze(code, chuban, stcsItem):
	timeObj = re.match(r'(\d{2}):(\d{2})', chuban)
	hour = int(timeObj.group(1))
	minute = int(timeObj.group(2))
	#print code, chuban
	if code[:3] in G_LARGE_FLUC:
		if hour<=11:
			stcsItem.s_large_sw_zt += 1
		else:
			stcsItem.s_large_xw_zt += 1
	else:
		if hour<=11:
			stcsItem.s_sw_zt += 1
		else:
			stcsItem.s_xw_zt += 1

def get_price_list(code, price_dict, src='163'):
	if src=='' or src=='163':
		get_price_list_163(code, price_dict)
	elif src=='sina':
		sn_code = sina_code(code)
		#get_price_list(sn_code, price_dict)
	else:
		print("WIP", src)
	return

#如果是YZZT，确定是不是还没有开板的CX
def check_YZ_not_kb(non_kaiban_list, code):
	for item in non_kaiban_list:
		if code==item['securitycode']:
			print "TODO:Need check"
			#print item['securitycode'],item['securityshortname']
			return 1
	return 0

# 判断新股第一天是否YZZT
def check_YZ_new_market(code, stcsItem):
	price_dict = {}
	get_price_list(code, price_dict)
	p_len = len(price_dict)
	if p_len==0:
		#print ("Error: no price", code)
		return 0
	elif p_len>3:
		return -1
	#print(price_dict)
	stcsItem.s_cx_yzzt += 1
	return 1

def searchInList(code, src_list, desc):
	bPreZt = 0
	count = 0
	for item in src_list:
		if item[0]==code:
			#print "Find ", desc, code, item[7], item[8]
			bPreZt = 1
			count = int(item[7])
			break
	return bPreZt, count
	
#type:
# 0: ZT
# 1: DT
def getPreZDtDays(code, type, preStat):
	bPreZt = 0
	if type==0:
		if code[:3] in G_LARGE_FLUC:
			bPreZt, count = searchInList(code, preStat.lst_large_non_yzcx_yzzt, "yzzt1")
			if bPreZt==0:
				bPreZt, count = searchInList(code, preStat.lst_large_non_yzcx_zt, "zt1")
		else:
			bPreZt, count = searchInList(code, preStat.lst_non_yzcx_yzzt, "yzzt1")
			if bPreZt==0:
				bPreZt, count = searchInList(code, preStat.lst_non_yzcx_zt, "zt1")
	elif type==1:
		if code[:3] in G_LARGE_FLUC:
			bPreZt, count = searchInList(code, preStat.lst_large_yzdt, "yzdt1")
			if bPreZt==0:
				bPreZt, count = searchInList(code, preStat.lst_large_dt, "dt1")
		else:
			bPreZt, count = searchInList(code, preStat.lst_yzdt, "yzdt1")
			if bPreZt==0:
				bPreZt, count = searchInList(code, preStat.lst_dt, "dt1")
	else:
		print ("Invalid type", type, code)
		return -1

	if bPreZt==0:
		count = 0
	return count

#上市日期和交易日大约1年前的时间对比
def verify_one_year_cx(market_date, pre300_date, type, stk_list):
	#propLen = len(props)
	#market_date = props[propLen-1]
	mkDt = datetime.datetime.strptime(market_date, '%Y-%m-%d').date()
	pre300Dt = datetime.datetime.strptime(pre300_date, '%Y-%m-%d').date()
	if (pre300Dt-mkDt).days<=0:
		stk_list[0] = CX_DAYS-50
	else:
		stk_list[0] = CX_DAYS+50
	return

#type:
# 0: ZT
# 1: DT
#判断是不是复牌STK，或者退市STK
def checkZDTInfo(code, name, fpFlag, type, preStat):
	if fpFlag==1:
		#print "FuPai YZZT", code, name.encode('gbk')
		bGetDays = 1
		return bGetDays, -1
	elif TS_FLAG==1:
		if name[:2]==u'退市':
			#print code, name.encode('gbk'), "ZT"
			count = -1
		elif name[-1:]==u'退':
			#print code, name.encode('gbk'), "ZT"
			count = -1
		else:
			count = getPreZDtDays(code, type, preStat)
	else:
		count = getPreZDtDays(code, type, preStat)
	return 0,count

def query_stk(index, qryArgs, pageNum, qLock, st, sr, ps):
	pageStr = index*pageNum + 1
	pageEnd = pageStr + pageNum - 1
	
	debug = 0
	if debug==1:
		qLock.acquire()
		print index, pageNum, pageStr, pageEnd
		qLock.release()

	curpage = pageStr
	for curpage in range(pageStr, pageEnd+1):
		if URL_TYPE==1:
			bnext = get_each_page_data1(qryArgs, curpage, st, sr, ps)
		elif URL_TYPE==2:
			bnext = get_each_page_push_data1(qryArgs, curpage, st, sr, ps)
		else:
			break
		if bnext==0:
			break
	#print("query_stk quit", index);
	return
	
#sort mode：
#'A' stock code
#'B' 股价
#'C' 涨幅
def get_stk_code_by_dfcf(new_st_list, st='C', sr=-1, ps=80):
	curpage = 1
	#items_list = []
	totalpage = -1
	if URL_TYPE==1:
		totalpage = get_stk_max_page(0, st, sr, ps)
	elif URL_TYPE==2:
		totalpage = get_stk_push_max_page(0, st, sr, ps)

	if totalpage==-1:
		return totalpage
	#print("Max Page", totalpage)
	
	thrdNum = 4
	pageNum = totalpage/4 + 1
	threadIdx = 0
	threads = []
	qryThread = [[] for i in range(thrdNum)]
	lock = threading.Lock()

	#print "lll=", len(qryThread[0]),len(qryThread[1])
	threadIdx = 0
	for threadIdx in range(len(qryThread)):
		qryArgs = qryThread[threadIdx]
		t = threading.Thread(target=query_stk, args=(threadIdx, qryArgs, pageNum, lock, st, sr, ps))
		threads.append(t)

	for item in threads:
		item.start()
	for item in threads:
		item.join()
	
	threadIdx = 0
	for threadIdx in range(len(qryThread)):
		if qryThread[threadIdx] == []:
			print ("Warning: Empty data")
			exit(0)
		new_st_list.extend(qryThread[threadIdx])
	'''
	while 1:
		bnext = get_each_page_data1(new_st_list, curpage, st, sr, ps)
		exit(0)
		if bnext==0:
			break
		elif bnext==-1:
			continue
		curpage += 1
	#for item in items_list:
	#	new_st_list.append(item[0:6])
	'''
	return 0

if __name__=="__main__":
	print "Realtime Common Interface"
	
