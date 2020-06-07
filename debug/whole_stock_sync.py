#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import string
import urllib2
import datetime
import pandas as pd
#import numpy as np
#from openpyxl import Workbook
#from openpyxl.reader.excel  import  load_workbook
sys.path.append(".")
from internal.dfcf_inf import *


#获取每天的所有的信息，将new stock选出
#放到 "../data/entry/trade/ns_info.xlxs"

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

def handle_head(nm_list, market):
	nm_list.append("Code")
	nm_list.append("Name")

	c = 'a'
	for i in range(0, (24-len(nm_list))):
		nm_list.append(c+"_itm")
		c = chr(ord(c)+1)
	nm_list.append(market)

# Main
prepath = "internal/db/"
name = "whole_stk.csv"

if __name__=="__main__":
	st_list = []
	get_latest_market(st_list)

	market = "MartketDate"
	nm_list = []
	handle_head(nm_list, market)
	#print(len(nm_list), nm_list)

	new_lst = []
	for i in st_list:
		objs = i.split(',')
		new_lst.append(objs)

	df1 = pd.DataFrame(new_lst, columns=nm_list)
	df1 = df1.set_index('Code')
	df1 = df1.sort_values([market], 0, False)



	df1.to_csv(prepath + name)


