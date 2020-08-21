#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import re
import os

from internal.common_inf import *

def show_real_index(show_idx, src='sn'):
	idx_list = []
	get_index_info(idx_list, show_idx, src)
	for i in idx_list:
		if len(i)<10:
			continue
		str1 = i[i.index('"')+1:-1]
		idxObj = str1.split(',')
		f_pre_cls = float(idxObj[2])
		f_price = float(idxObj[3])
		ratio = round((f_price-f_pre_cls)*100/f_pre_cls, 2)
		print "%8.2f(%6s)"%(f_price, ratio)

if __name__=="__main__":
	print "Realtime Common Interface"
	
