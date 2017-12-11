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
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook
from internal.common import *
from internal.ts_common import *
from fupai import *

def list_stock_news_sum(codeArray, curdate, file):
	codeLen = len(codeArray)
	for j in range(0, codeLen):
		if file is None:
			continue
		df = None
		try:
			df = ts.get_notices(codeArray[j],curdate)
		except:
			pass
		if df is None:
			df = ts.get_notices(codeArray[j])
		for index,row in df.iterrows():
			file.write("%s,%s"%(row['date'],row['title'].encode('gbk') ))
			file.write("\r\n")
		file.write("\r\n")

#Main
prepath = "../data/"
prepath1 = "../data/entry/fupai/"

stockCode = []
stockName = []
totalline = 0
lasttime = ''
filename = prepath + 'fupai' + '_detail'
filetxt = filename + '.txt'
fl = open(filetxt, 'w')

curdate = ''
bLast = 0
curdate, bLast = get_date_with_last()
print curdate, bLast

res_data = get_tingfupai_res(curdate)
if res_data is None:
	exit(0)

totalline = get_all_fupai_data(res_data, fl, 1, curdate, stockCode, stockName)

#将所有的数据汇总输出
fl.write("\n====================================================================================\n")
#list_stock_rt(stockCode, curdate, fl)
if bLast==1:
	list_stock_rt(stockCode, curdate, fl)
else:
	list_fupai_trade(stockCode, stockName, curdate, fl)
list_stock_news_sum(stockCode, curdate, fl)

fl.close()
if (totalline==0):
	print "No Matched Record"
	os.remove(filetxt)
else:
	prepath1 = prepath1 + "fupai" + curdate + "_detail.txt"
	shutil.copy(filetxt, prepath1)
