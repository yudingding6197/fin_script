#!/usr/bin/env python
# -*- coding:gbk -*-
#��DFCF�еõ����е���Ϣ������TP�ģ����浽ָ�����ļ���

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

