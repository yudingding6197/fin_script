#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import datetime
import urllib2
import getopt
from openpyxl import Workbook
from openpyxl.reader.excel import load_workbook
from internal.ts_common import *
from internal.common_inf import *
from internal.dfcf_inf import *

#Main
g_st = datetime.datetime.now()
if __name__ == "__main__":
	optlist, args = getopt.getopt(sys.argv[1:], '?d:')
	for option, value in optlist:
		if option in ["-d","--day"]:
			pre_day=int(value)
		elif option in ["-?","--???"]:
			print("Usage:" + os.path.basename(sys.argv[0]) + " [-d pre_day]")
			exit()
	#end for

	tradeList = []
	get_his_trade_days(tradeList, 300)

	g_st = datetime.datetime.now()
	st_list = []
	get_stk_code_by_cond(st_list)
	timeShow(g_st)
	print( len(st_list) )
	print(st_list[:10])

	g_st = datetime.datetime.now()
	st_list = []
	new_st_list = []
	get_today_new_stock(new_st_list)
	LOOP_COUNT=0
	st_bas = None
	while LOOP_COUNT<3:
		try:
			st_bas = ts.get_stock_basics()
		except:
			LOOP_COUNT += 1
			time.sleep(0.5)
		else:
			break;
	if st_bas is None:
		print "Timeout to get stock basic info"
		exit(0)
	st_pb_base = st_bas[st_bas.pb!=0]
	st_pb_base = st_pb_base.sort_values(['timeToMarket'], 0, False)
	st_index = st_pb_base.index
	st_bas_list=list(st_index)

	for i in range(0, len(new_st_list)):
		if new_st_list[i] in st_bas_list[0:10]:
			pass
		else:
			st_list.append(new_st_list[i])
	st_list.extend(st_bas_list)
	timeShow(g_st)

	print( len(st_list) )
	print(st_list[:10])

'''
#如果需要记录到csv文件中，修改addcsv=1
addcsv = 0
prepath = "../data/"
url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php"
xmlfile = "internal/array.xml"

pindex = len(sys.argv)
if pindex<3:
	sys.stderr.write("Usage: " +os.path.basename(sys.argv[0])+ " 代码 时间<YYYY-MM-DD or MM-DD> 强制替换<0 or 1> [arr=[number, number...]]\n")
	exit(1);

code = sys.argv[1]
if (len(code) != 6):
	sys.stderr.write("Len should be 6\n")
	exit(1);

ret, code = parseCode(code)
if ret!=0:
	exit(1);
#print code

today = datetime.date.today()
ret,stdate = parseDate(sys.argv[2], today)
if ret==-1:
	exit(1)

replace=0
if pindex>=4:
	replace = int(sys.argv[3])

sarr = ''
if pindex==5:
	sarr = sys.argv[4]
else:
	sarr = get_data_array(sys.argv[1], xmlfile)

init_trade_obj()

edate = datetime.datetime.strptime(stdate, '%Y-%m-%d').date()
delta = edate - today
if (delta.days>=0):
	print "Warning:日期可能不正确，导致数据错误！"

ts_handle_data(addcsv, prepath, 1, url, code, stdate, replace, sarr)
'''