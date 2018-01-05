#!/usr/bin/env python
# -*- coding:gbk -*-
#从DFCF中得到所有的信息，包括TP的，保存到指定的文件中

import sys
import re
import os
import datetime
import tushare as ts
sys.path.append(".")
sys.path.append("..")
from internal.dfcf_interface import *

if __name__ == '__main__':
	fpath = "../data/entry/market/latest_stock.txt"
	new_st_list = []
	get_latest_market(new_st_list)
	file=open(fpath, 'w')
	for item in new_st_list:
		#file.write(line.encode('gbk'))
		file.write(item+'\n')
	file.close()

