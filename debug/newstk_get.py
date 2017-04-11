#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import string
import urllib
import urllib2
import datetime
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook
sys.path.append(".")
sys.path.append("..")
from internal.ts_common import *

#获取每天的所有的信息，将new stock选出
#放到 "../Data/entry/trade/ns_info.xlxs"

#'code,name,timeToMarket,outstanding,totals'

def handle_float(str):
	if str=='-':
		obj = None
	else:
		obj = float(str)
	return obj

def handle_int(str):
	if str=='-':
		obj = None
	else:
		obj = int(str)
	return obj

def check_new_stk(stk_item, stockInfo):
	str_arr = stk_item.split(',')
	name = str_arr[2]
	code = str_arr[1]
	if name[0:1]!='N':
		return 0

	url_liut = "http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockStructureHistory/stockid/%s/stocktype/LiuTongA.phtml"
	url_totl = "http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockStructureHistory/stockid/%s/stocktype/TotalStock.phtml"
	ltgb_list = []
	gb_str = get_guben_line(url_liut, code)
	parse_guben(gb_str, ltgb_list)

	zgb_list = []
	gb_str = get_guben_line(url_totl, code)
	parse_guben(gb_str, zgb_list)

	gb_len = len(ltgb_list)
	if gb_len != len(zgb_list):
		print code, name, "guben not match"
		return 0
	for i in range(0, gb_len):
		ltobj = ltgb_list[i]
		zobj = zgb_list[i]
		if ltobj[0] != zobj[0]:
			print code, "guben date not match", ltobj[0], zobj[0]
			return 0
		if ltobj[1]==0:
			continue
		sdate = ''.join(ltobj[0].split('-'))
		stockInfo.append(code)
		stockInfo.append(name)
		stockInfo.append(long(sdate))
		stockInfo.append(ltobj[1])
		stockInfo.append(zobj[1])
	return 1

# Main
fm_url = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._A&sty=FCOIATA&sortType=A&sortRule=-1&page=%d&pageSize=%d&token=7bc05d0d4c3c22ef9fca8c2a912d779c"
prepath1 = "../Data/entry/trade/"
name = "ns_info.xlsx"
PAGE_COUNT = 500

wb = Workbook()
# grab the active worksheet
ws = wb.active
strline = u'code,name,timeToMarket,outstanding,totals'
strObj = strline.split(u',')
ws.append(strObj)
#随着列数进行改变
ws.auto_filter.ref = "A1:P1"
excel_row = 2
repeat_flag = 0
first_code = ''

for i in range(1, 35):
	if repeat_flag==1:
		break

	url = fm_url%(i,PAGE_COUNT)
	#print url
	#response type is 'instance'
	response = None
	LOOP_COUNT = 0
	while LOOP_COUNT<3:
		try:
			req = urllib2.Request(url)
			response = urllib2.urlopen(req, timeout=5)
		except:
			LOOP_COUNT += 1
			print "URL request timeout"
		else:
			break
	if response is None:
		break

	line = response.readline()
	while line:
		line = line.decode('utf8')

		obj = re.match('.*\(\[(.*)\]\)',line)
		line = obj.group(1)
		#这个if可能判断多余，强行左右匹配引号里的内容""
		if line is None:
			pos = line.find('"')
			if pos == -1:
				line = response.readline()
				continue
			rpos = line.rfind('"')
			if rpos==-1:
				line = response.readline()
				continue
			if rpos<=pos:
				line = response.readline()
				continue
			line = line[pos:rpos+1]

		total_item = 0
		#记录每一页第一个代码，避免重复读取数据
		firstln = 1
		while 1:
			obj = re.match(r'"(.*?)",?(.*)', line)
			if obj is None:
				break
			line = obj.group(2)

			stockInfo = []
			stk_item = obj.group(1)
			
			if firstln==1:
				str_arr = stk_item.split(',')
				code = str_arr[1]
				#print "%d '%s'=='%s' "%(i,first_code,code)
				if first_code==code:
					repeat_flag = 1
					break
				first_code = code
				firstln = 0

			ret = check_new_stk(stk_item, stockInfo)
			if ret==0:
				continue
			#print stk_item
			print stockInfo
			#添加到表格中
			k = 0
			ascid = 65
			number = len(stockInfo)
			for k in range(0,number):
				cell = chr(ascid+k) + str(excel_row)
				ws[cell] = stockInfo[k]
			excel_row += 1
			total_item += 1
		#假设最后一页取出数据太少，停止http请求
		if total_item<PAGE_COUNT-10:
			break
		line = response.readline()

filexlsx1 = prepath1 + name
wb.save(filexlsx1)
