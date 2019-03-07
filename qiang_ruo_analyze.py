#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import time
import string
import datetime
import getopt
import platform
import tushare as ts
from internal.common_inf import *
from internal.dfcf_interface import *
from internal.ts_common import *
from internal.analyze_data import *






def show_zt_info(zt_list, desc, fmt, outstr, pconfig):
	number = len(zt_list)
	endstr = ''
	if number<=0:
		return
	elif pconfig['AllInfo']==1:
		number = 10000
	elif number>30:
		number = 30
		if desc=="ZTHL":
			number = 10
		endstr = '......'

	print outstr
	df = pd.DataFrame(zt_list)
	if pconfig['SortByTime']==1:
		if desc=="ZT":
			df = df.sort_values([9,7], 0, True)
		elif desc=="ZTHL":
			df = df.sort_values([9,7], 0, True)
		else:
			df = df.sort_values([7], 0, True)
	else:
		if desc=="ZT":
			df = df.sort_values([7,9], 0, [False,True])
		elif desc=="YZZT":
			df = df.sort_values([7], 0, False)
		elif desc=="ZTHL":
			df = df.sort_values([2,7], 0, False)
	i = 1
	for index,itm_lst in df.iterrows():
		#str = "%2d %6s %-7s	%8.2f %8.2f %8.2f %8.2f %8.2f %4d" % (i,itm_lst[0],itm_lst[1],itm_lst[2],itm_lst[3],itm_lst[4],itm_lst[5],itm_lst[6],itm_lst[7])
		cxFlag = ''
		if itm_lst[8]<300:
			cxFlag='CX'
		if desc=="YZZT":
			str = fmt % (i,itm_lst[0],itm_lst[1],itm_lst[2],itm_lst[3],itm_lst[4],itm_lst[5],itm_lst[6],itm_lst[7],cxFlag)
		elif desc=="ZT":
			cxFlag += ' ' + itm_lst[10]
			str = fmt % (i,itm_lst[0],itm_lst[1],itm_lst[2],itm_lst[3],itm_lst[4],itm_lst[5],itm_lst[6],itm_lst[7],cxFlag,itm_lst[9])
		elif desc=="ZTHL":
			cxFlag += ' ' + itm_lst[11]
			str = fmt % (i,itm_lst[0],itm_lst[1],itm_lst[2],itm_lst[3],itm_lst[4],itm_lst[5],itm_lst[6],itm_lst[7],cxFlag,itm_lst[9],itm_lst[10])
		print str
		i += 1
		if i>number:
			break
	print endstr

def show_dt_info(dt_list, desc, fmt, pconfig):
	number = len(dt_list)
	endstr = ''
	str = "%s  [%d]:" % (desc, number)
	if number<=0:
		return
	elif pconfig['AllInfo']==1:
		number = 10000
	elif number>30:
		number = 30
		endstr = '......'

	df = pd.DataFrame(dt_list)
	if pconfig['SortByTime']==1:
		if desc=="DT":
			df = df.sort_values([9,7], 0, True)
		elif desc=="DTFT":
			df = df.sort_values([9,7], 0, True)
		else:
			df = df.sort_values([7], 0, True)
	else:
		if desc=="DT":
			df = df.sort_values([7,9], 0, [False,True])
		elif desc=="YZDT":
			df = df.sort_values([7], 0, False)
		elif desc=="DTFT":
			df = df.sort_values([2,7], 0, False)
	i = 1
	print str
	for index,itm_lst in df.iterrows():
		cxFlag = ''
		if itm_lst[8]<300:
			cxFlag='CX'
		if desc=="YZDT":
			str = fmt % (i,itm_lst[0],itm_lst[1],itm_lst[2],itm_lst[3],itm_lst[4],itm_lst[5],itm_lst[6],itm_lst[7],cxFlag)
		elif desc=="DT":
			cxFlag += ' ' + itm_lst[10]
			str = fmt % (i,itm_lst[0],itm_lst[1],itm_lst[2],itm_lst[3],itm_lst[4],itm_lst[5],itm_lst[6],itm_lst[7],cxFlag,itm_lst[9])
		elif desc=="DTFT":
			cxFlag += ' ' + itm_lst[11]
			str = fmt % (i,itm_lst[0],itm_lst[1],itm_lst[2],itm_lst[3],itm_lst[4],itm_lst[5],itm_lst[6],itm_lst[7],cxFlag,itm_lst[9],itm_lst[10])
		print str
		i += 1
		if i>number:
			break
	print endstr

def filter_dtft(dtft_list, perc):
	if len(dtft_list)==0:
		return 0
	count = 0
	for item in dtft_list:
		if item[2]>perc:
			#print item[0],item[2]
			count += 1
	return count






def rt_quotes(dtFrame, source, qt_stage):
	print(source)
	for index,row in dtFrame.iterrows():
		#print(row)
		r1_len = len(row[1])
		r1 = row[1].decode('gbk')
		for i in range(10-r1_len):
			r1 += ' '

		if row['state']!='00':
			line = "%06s %-s --   --" %(row[0], r1)
			print (line)
			continue

		open = row['open']
		pre_close = row['p_close']
		price = row['price']
		high = row['high']
		low = row['low']
		volume = int(row['volume'])

		price_f = float(price)
		pre_close_f = float(pre_close)
		bidb_f = float(row['bidb'])
		bidb_s = float(row['bids'])
		if float(price)==0 or float(high)==0:
			change = '-'
			change_l = '-'
			change_h = '-'
			change_o = '-'
			if bidb_f==0 and bidb_s==0:
				pass
			elif bidb_f!=0:
				price_f = bidb_f
				change = '%02.02f'%( ((price_f-pre_close_f)/pre_close_f)*100 )
			elif bidb_s!=0:
				price_f = bids_f
				change = '%02.02f'%( ((price_f-pre_close_f)/pre_close_f)*100 )
			else:
				print("Error: Special Case", price, bidb, bids)
				print(row)
		else:
			change = '%02.02f'%( ((price_f-pre_close_f)/pre_close_f)*100 )
			change_l = '%02.02f'%( ((float(low)-pre_close_f)/pre_close_f)*100 )
			change_h = '%02.02f'%( ((float(high)-pre_close_f)/pre_close_f)*100 )
			change_o = '%02.02f'%( ((float(open)-pre_close_f)/pre_close_f)*100 )
		str_fmt = "%06s %-s %6.2f(%6s%%)   %8s(%6s) %8s(%6s)"
		line = str_fmt %(row[0], r1, price_f, change, low, change_l, high, change_h)
		print(line)

def index_follow_ud(head, index_ud):
	if index_ud!='':
		obj = index_ud.split('|')
		up = obj[0]
		ping = obj[1]
		down = obj[2]
		print("%s  %4s %4s %4s"%(head, up, ping, down))
	else:
		print(head)

def index_info(df, show_idx, qt_index):
	if df is None:
		return
	sh_info = ''
	sz_info = ''
	if qt_index is not None:
		qtObj = re.match(r'"(.*?)","(.*)"', qt_index)
		if qtObj is None:
			print("Invalid qt_index", qt_index)
		else:
			index_dt = qtObj.group(1)
			#print (index_dt)
			itemObj = index_dt.split(',')
			sh_info = itemObj[6]
			sz_info = itemObj[7]
	for index,row in df.iterrows():
		if row[0] not in show_idx:
			continue

		open = float(row['open'])
		close = float(row['close'])
		preclose = float(row['preclose'])
		if row['code'] == '000001':
			head = "%8.2f(%6s)"%(close, row[2])
			index_follow_ud(head, sh_info)
		elif row['code'] == '399001':
			head = "%8.2f(%6s)"%(close, row[2])
			index_follow_ud(head, sz_info)
		else:
			print("%8.2f(%6s)"%(close, row[2]))

def read_def(data_path, stockCode, stockCode_sn):
	file = open(data_path, 'r')
	if file is None:
		print("Error open file", data_path)
		return
	if '_self_define' in data_path:
		flag=0
		lines = file.readlines(10000)
		for line in lines:
			line=line.strip()
			if line=='STK':
				flag=1
				continue
			elif flag==1 and line=='END':
				break
			if flag==0:
				continue
			code=line.strip()
			if len(code)!=6:
				continue;
			if not code.isdigit():
				continue;
			stockCode.append(code)
			ncode = sina_code(code)
			stockCode_sn.append(ncode)
	else:
		line = file.readline()
		while line:
			if len(line)>=6:
				code = line[0:6]
				if code.isdigit():
					stockCode.append(code)
					ncode = sina_code(code)
					stockCode_sn.append(ncode)
			line = file.readline()
	file.close()

def analyze_state(tradeList, preday, dict):
	for i in range(0, preday):
		data_path = "../data/entry/realtime/rt_" + tradeList[i] + ".txt"
		#print (data_path)
		if not os.path.isfile(data_path):
			print("No file:" + data_path)
			continue
		parse_realtime_data(data_path, dict)



#Main
pre_day = 3
dict = {}
param_config = {
	"NoLog":0,
	"NoDetail":0,
	"SortByTime":0,
	"AllInfo":1,
	"DFCF":0,
}

sysstr = platform.system()
if __name__=="__main__":
	optlist, args = getopt.getopt(sys.argv[1:], '?p:')
	for option, value in optlist:
		if option in ["-p","--preday"]:
			pre_day=int(value)
		elif option in ["-?","--???"]:
			print("Usage:" + os.path.basename(sys.argv[0]) + " [-d pre_day]")
			exit()

	tradeList = []
	get_pre_trade_date(tradeList, pre_day+2)

	analyze_state(tradeList, pre_day, dict)

	column = []
	create_column(column)
	qt_stage = quotation_st()
	#print(tradeList[pre_day] + " Info")
	
	sn_code = []
	for cd in dict['Q']:
		ncode = sina_code(cd)
		sn_code.append(ncode)

	#rt_list = []
	#realtime_price(sn_code, rt_list)
	#df = pd.DataFrame(rt_list, columns=column)
	#rt_quotes(df, 'Q', qt_stage)

	today_open = []
	stcsItem=statisticsItem()
	status = get_all_stk_info(dict['Q'], 0, today_open, stcsItem)
	if status==-1:
		print("Error Get info")
		exit(0)

	print("Total %4d" % (len(dict['Q'])) )
	non_cx_yz = len(stcsItem.lst_non_yzcx_yzzt)
	cx_yz = stcsItem.s_yzzt-non_cx_yz

	str_opn = "[%d %d %d %d] %3d UP,%3d DOWN" % (stcsItem.s_open_zt,stcsItem.s_close_zt,stcsItem.s_open_T_zt,stcsItem.s_dk_zt, stcsItem.s_sw_zt, stcsItem.s_xw_zt)
	if sysstr == "Linux":
		str_opn = str_opn.decode('gbk').encode('utf-8')

	str_dt = "%d DTKP" % (stcsItem.s_open_dt)
	if stcsItem.s_yzdt>0:
		str_dt = "%s, %d YZDT" % (str_dt, stcsItem.s_yzdt)
	if stcsItem.s_open_dt_dk>0:
		str_dt = "%s, %d DTDK" % (str_dt, stcsItem.s_open_dt_dk)
	DaoT = stcsItem.s_open_dt-stcsItem.s_yzdt-stcsItem.s_open_dt_dk
	if DaoT>0:
		str_dt = "%s, %d DaoT " % (str_dt, DaoT)
	print "			ST(%d ZT %d DT)		%s" % (stcsItem.s_st_yzzt, stcsItem.s_st_yzdt, str_dt)

	#print "			ST(%d ZT %d DT)		DTKP:%d YZDT:%d DTDK:%d" % (stcsItem.s_st_yzzt, stcsItem.s_st_yzdt, stcsItem.s_open_dt, stcsItem.s_yzdt,stcsItem.s_open_dt_dk)

	dtft_qiang = filter_dtft(stcsItem.lst_dtft, -3)
	print "%4d-ZT		%4d-DT		%d-X %d--(%d+%d) %s" % (stcsItem.s_zt,stcsItem.s_dt,stcsItem.s_new,stcsItem.s_yzzt, cx_yz, non_cx_yz, str_opn)
	print "%4d-CG(%d)	%4d-FT(%d)	%2d-YIN  KD:[%s]" %(stcsItem.s_zthl,len(stcsItem.lst_kd),stcsItem.s_dtft,dtft_qiang,stcsItem.s_zt_o_gt_c,','.join(stcsItem.lst_kd))
	print "%4d(%4d)	ZERO:%4d	%4d(%4d)" %(stcsItem.s_open_sz, stcsItem.s_open_dz, stcsItem.s_open_pp, stcsItem.s_open_xd, stcsItem.s_open_dd)
	print "%4d(%4d)	ZERO:%4d	%4d(%4d)" %(stcsItem.s_close_sz, stcsItem.s_close_dz, stcsItem.s_close_pp, stcsItem.s_close_xd, stcsItem.s_close_dd)
	print "4%%:%4d	%4d" %(stcsItem.s_high_zf,stcsItem.s_low_df)

	str = ''
	list = today_open
	if len(list)>0:
		print "CXKB:"
		for i in range(0, len(list)):
			itm_lst = list[i]
			if itm_lst[2]>9.9:
				str1 = "%s(%d, ZT), " % (itm_lst[1], itm_lst[4])
			elif itm_lst[2]<-9.9:
				str1 = "%s(%d, DT), " % (itm_lst[1], itm_lst[4])
			else:
				str1 = "%s(%d, %.2f%%), " % (itm_lst[1], itm_lst[4],itm_lst[2])
			str += str1
		print str
	else:
		print "CXKB:====="
	print ''

	str = ''
	list = stcsItem.lst_nb
	if len(list)>0:
		print "NB:"
		for i in range(0, len(list)):
			itm_lst = list[i]
			str1 = "%s(%.2f%%, %.2f%%), " % (itm_lst[1], itm_lst[2], itm_lst[4])
			str += str1
		print str

	str = ''
	list = stcsItem.lst_jc
	if len(list)>0:
		print "JC:"
		for i in range(0, len(list)):
			itm_lst = list[i]
			str1 = "%s(%.2f%%, %.2f%%), " % (itm_lst[1], itm_lst[2], itm_lst[4])
			str += str1
		print str

	if 0==0:
		non_cx = len(stcsItem.lst_non_yzcx_yzzt)+len(stcsItem.lst_non_yzcx_zt)
		tol_str = "Total( %d = %d + %d	YZ: %d=%d(%d)+%d   %d CXZT,%d CXDT ):"
		print tol_str%( stcsItem.s_zt, stcsItem.s_zt-non_cx, non_cx, stcsItem.s_yzzt, cx_yz, stcsItem.s_cx_yzzt, non_cx_yz, stcsItem.s_cxzt, stcsItem.s_cxdt)
		print "id %6s %-12s	%-10s %-9s %-8s %-8s %-8s %-8s" % ("code","name","change","price","opn_p","hgh_p","low_p","z_d")

		fmt1 = "%2d %6s %-7s	%8.2f %8.2f %8.2f %8.2f %8.2f %4d %3s"
		fmt2 = "%2d %6s %-7s	%8.2f %8.2f %8.2f %8.2f %8.2f %4d %3s %9s"
		fmt3 = "%2d %6s %-7s	%8.2f %8.2f %8.2f %8.2f %8.2f %4d %3s %9s %9s"

		outstr = "YZZT  [%d]:" % (len(stcsItem.lst_non_yzcx_yzzt))
		show_zt_info(stcsItem.lst_non_yzcx_yzzt, "YZZT", fmt1, outstr, param_config)
		outstr = "ZT  [%d+%d]:" % (stcsItem.s_sw_zt, stcsItem.s_xw_zt)
		show_zt_info(stcsItem.lst_non_yzcx_zt, "ZT", fmt2, outstr, param_config)
		outstr = "ZTHL [%d]:" % (stcsItem.s_zthl)
		show_zt_info(stcsItem.lst_non_yzcx_zthl, "ZTHL", fmt3, outstr, param_config)

		fmt0 = "Total DT (%d)		DTFT (%d)==(%d)================================="
		print fmt0 %(len(stcsItem.lst_yzdt)+len(stcsItem.lst_dt), len(stcsItem.lst_dtft), len(stcsItem.lst_yzdt)+len(stcsItem.lst_dt)+len(stcsItem.lst_dtft))
		show_dt_info(stcsItem.lst_yzdt, "YZDT", fmt1, param_config)
		show_dt_info(stcsItem.lst_dt, "DT", fmt2, param_config)
		show_dt_info(stcsItem.lst_dtft, "DTFT", fmt3, param_config)

