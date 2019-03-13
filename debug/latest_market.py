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
from internal.dfcf_inf import *

if __name__ == '__main__':
	file   = "latest_stock.txt"
	folder = "../data/entry/market"

	if not os.path.isdir(folder):
		os.makedirs(folder)

	new_st_list = []
	get_latest_market(new_st_list)

	fpath = os.path.join(folder, file)
	file=open(fpath, 'w')
	for item in new_st_list:
		#file.write(line.encode('gbk'))
		file.write(item+'\n')
	file.close()

