#!/usr/bin/env python
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
sys.path.append(".")
sys.path.append("..")
from internal.ts_common import *

#得到所有的股本变动信息，需要得到所有的代码，调用debug/instant_data.py更新数据

url_liut = "http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockStructureHistory/stockid/%s/stocktype/LiuTongA.phtml"
url_totl = "http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockStructureHistory/stockid/%s/stocktype/TotalStock.phtml"
pindex = len(sys.argv)
if pindex==1:
	data_path = "../data/entry/trade/trade_last.txt"
	file = open(data_path, 'r')
	while 1:
		lines = file.readlines(9000)
		if not lines:
			break
		for line in lines:
			code = line.strip()
			if len(code)!=6:
				print code, "Len should be 6"
				continue
			if code.isdigit() is False:
				print code, "Invalid code"
				continue
			ltgb_list = []
			gb_str = get_guben_line(url_liut, code)
			parse_guben(gb_str, ltgb_list)

			zgb_list = []
			gb_str = get_guben_line(url_totl, code)
			parse_guben(gb_str, zgb_list)
			#print ltgb_list,zgb_list
	file.close()
elif pindex==2:
	code = sys.argv[1]
	if len(code)!=6:
		print code, "Len should be 6"
		exit(1);
	if code.isdigit() is False:
		print code, "Invalid code"
		exit(1);

	ltgb_list = []
	gb_str = get_guben_line(url_liut, code)
	parse_guben(gb_str, ltgb_list)

	zgb_list = []
	gb_str = get_guben_line(url_totl, code)
	parse_guben(gb_str, zgb_list)

	for i in range(0, len(ltgb_list)):
		ltobj = ltgb_list[i]
		zobj = zgb_list[i]
		if ltobj[0] != zobj[0]:
			print code, "Not match", ltobj[0], zobj[0]
			break
		str = "%s	%10.4f	%10.4f" %(ltobj[0], ltobj[1], zobj[1])
		print str
