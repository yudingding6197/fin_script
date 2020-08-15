#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import string
import urllib
import urllib2
import datetime
import binascii
import shutil
#from openpyxl import Workbook
#from openpyxl.reader.excel  import  load_workbook
#from internal.common import *
#from internal.ts_common import *
from internal.tingfupai import *
from internal.trade_date import *
from internal.url_juchao.tips_res import *

#Main
if __name__=="__main__":
	curdate = ''
	bLast = 0
	#curdate, bLast = get_date_with_last()
	curdate = get_lastday()
	bLast = 1
	print curdate, bLast

	res_data = get_tingfupai_res(curdate)
	if res_data is None:
		exit(0)

	stockCode = []
	stockName = []
	totalline = 0

	prepath = "../data/"
	prepath1 = "../data/entry/fupai/"
	filename = prepath + 'fupai'
	filetxt = filename + '.txt'
	fl = open(filetxt, 'w')

	totalline = get_all_fupai_data(res_data, fl, 0, curdate, stockCode, stockName)

	#将所有的数据汇总输出
	if bLast==1:
		list_stock_rt(stockCode, curdate, fl)
	else:
		if bLast==0:
			list_fupai_trade(stockCode, stockName, curdate, fl)

	fl.close()

	if (totalline==0):
		print "No Matched Record"
		os.remove(filetxt)
	else:
		prepath1 = prepath1 + "fupai" + curdate + ".txt"
		shutil.copy(filetxt, prepath1)
