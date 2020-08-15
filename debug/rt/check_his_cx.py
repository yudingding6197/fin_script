#!/usr/bin/env python
# -*- coding:utf-8 -*-
#检查history realtm文件中所有的个股，哪些是CX，哪些不是
import sys
import re
import os
import string
import datetime
import shutil

sys.path.append(".")
from internal.trade_date import *
from internal.realtime_obj import *
from internal.analyze_realtime import *
from internal.handle_realtime import *

#Main
if __name__=="__main__":
	curdate = ''
	bLast = 0
	trade_day = get_lastday()
	pre_date = get_preday(0, trade_day)
	#pre_date = trade_day

	preStatItem = statisticsItem()
	ret = parse_realtime_his_file(pre_date, preStatItem)
	
	pre300_date = get_preday(CX_DAYS, pre_date)
	print pre_date,pre300_date
	
	st_list = []
	ret = get_stk_code_by_dfcf(st_list, 'A', 0)
	stkList = [
		preStatItem.lst_non_yzcx_yzzt,
		preStatItem.lst_non_yzcx_zt,
		preStatItem.lst_non_yzcx_zthl,
		preStatItem.lst_yzdt,
		preStatItem.lst_dt,
		preStatItem.lst_dtft,
	]
	for iList in stkList:
		for item in iList:
			bFlag = 0
			for tdItem in st_list:
				if tdItem[1] == item[0]: 
					bFlag=1
					#print "Not Match",item[0],item[1],tdItem[-1]
					trd_date = datetime.datetime.strptime(pre_date, '%Y-%m-%d').date()
					mk_date = datetime.datetime.strptime(tdItem[-1], '%Y-%m-%d').date()
					if (trd_date-mk_date).days>CX_DAYS:
						pass
						#print "",item[0],item[1],''
					else:
						print "",item[0],item[1],'  CCCCCC'
			if bFlag==0:
				print "Not Match",item[0],item[1]
		print ""
	