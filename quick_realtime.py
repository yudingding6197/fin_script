#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import time
import string
import datetime
import platform
import shutil
import getopt
import chardet
import pandas as pd
#import tushare as ts
#import internal.common
from internal.handle_realtime import *
#from internal.dfcf_inf import *
#from internal.ts_common import show_index_info
from internal.trade_date import *
from internal.update_tday_db import *
from internal.analyze_realtime import *
from internal.compare_realtime import *
from internal.tingfupai import * 
from internal.common_inf import * 

class Logger_IO(object): 
	def __init__(self, filename="Default.log"):
		self.terminal = sys.stdout
		self.log = open(filename, "w")

	def write(self, message):
		self.terminal.write(message)
		self.log.write(message)

	def flush(self):
		self.log.flush()
		pass

#可以和show_dt_info 合并, 通过 desc in ['DT','ZT']进行判断
def show_zt_info(zt_list, desc, fmt, outstr, pconfig):
	number = len(zt_list)
	endstr = ''
	if number<=0:
		return
	elif pconfig['NotAllInfo']==0:
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
		if itm_lst[8]<CX_DAYS:
			cxFlag='CX'
		if desc=="YZZT":
			str = fmt % (i,itm_lst[0],itm_lst[1],itm_lst[2],itm_lst[3],itm_lst[4],itm_lst[5],itm_lst[6],itm_lst[7],cxFlag)
		elif desc=="ZT":
			cxFlag += ' ' + itm_lst[10]
			str = fmt % (i,itm_lst[0],itm_lst[1],itm_lst[2],itm_lst[3],itm_lst[4],itm_lst[5],itm_lst[6],itm_lst[7],cxFlag,itm_lst[9])
		elif desc=="ZTHL":
			cxFlag += ' ' + itm_lst[11]
			str = fmt % (i,itm_lst[0],itm_lst[1],itm_lst[2],itm_lst[3],itm_lst[4],itm_lst[5],itm_lst[6],itm_lst[7],cxFlag,itm_lst[9],itm_lst[10])
		if isinstance(str, unicode): str = str.encode('gbk')
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
	elif pconfig['NotAllInfo']==0:
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
	if isinstance(str, unicode): str = str.encode('gbk')
	print str
	for index,itm_lst in df.iterrows():
		cxFlag = ''
		if itm_lst[8]<CX_DAYS:
			cxFlag='CX'
		if desc=="YZDT":
			str = fmt % (i,itm_lst[0],itm_lst[1],itm_lst[2],itm_lst[3],itm_lst[4],itm_lst[5],itm_lst[6],itm_lst[7],cxFlag)
		elif desc=="DT":
			cxFlag += ' ' + itm_lst[10]
			str = fmt % (i,itm_lst[0],itm_lst[1],itm_lst[2],itm_lst[3],itm_lst[4],itm_lst[5],itm_lst[6],itm_lst[7],cxFlag,itm_lst[9])
		elif desc=="DTFT":
			cxFlag += ' ' + itm_lst[11]
			str = fmt % (i,itm_lst[0],itm_lst[1],itm_lst[2],itm_lst[3],itm_lst[4],itm_lst[5],itm_lst[6],itm_lst[7],cxFlag,itm_lst[9],itm_lst[10])
		if isinstance(str, unicode): str = str.encode('gbk')
		print str
		i += 1
		if i>number:
			break
	print endstr

#fmt1 = "%2d %6s %-7s	%8.2f %8.2f %8.2f %8.2f %8.2f %4d %3s"
def show_tuishi_info(tuis_list, fmt):
	number=len(tuis_list)
	
	desc = "TUISHI [%d]"%(number)
	print desc

	for i in range(len(tuis_list)):
		props = tuis_list[i]
		#print props
		
		high = round(float(props[11]),2)
		low = round(float(props[12]),2)
		open = round(float(props[10]),2)
		price = round(float(props[3]),2)
		pre_close = round(float(props[9]),2)
		volume = int(props[8])
		
		o_percent = (open-pre_close)*100/pre_close
		c_percent = (price-pre_close)*100/pre_close
		h_percent = (high-pre_close)*100/pre_close
		l_percent = (low-pre_close)*100/pre_close
		open_percent = spc_round2(o_percent,2)
		change_percent = spc_round2(c_percent,2)
		high_zf_percent = spc_round2(h_percent,2)
		low_df_percent = spc_round2(l_percent,2)
		
		stk_list = [0, 0]
		count = 0
		stat = ''
		if high==low:
			if price>pre_close:
				count = get_zf_days(props[1], 1, trade_date, 1, stk_list)
				stat = 'YZZT'
			else:
				count = get_zf_days(props[1], 2, trade_date, 1, stk_list)
				stat = 'YZDT'

		desc = fmt % (i+1,props[1],props[2],change_percent,price,o_percent,high_zf_percent,low_df_percent,count,stat)
		print desc.encode('gbk')
	print ""
	
def filter_dtft(dtft_list, perc):
	if len(dtft_list)==0:
		return 0
	count = 0
	for item in dtft_list:
		if item[2]>perc:
			#print item[0],item[2]
			count += 1
	return count

def handle_argument():
	optlist, args = getopt.getopt(sys.argv[1:], 'ldtaq')
	for option, value in optlist:
		if option in ["-l","--nolog"]:
			param_config["NoLog"] = 1
		elif option in ["-d","--nodetail"]:
			param_config["NoDetail"] = 1
		elif option in ["-t","--sbtime"]:
			param_config["SortByTime"] = 1
		elif option in ["-a","--all"]:
			param_config["NotAllInfo"] = 1
		elif option in ["-q","--tuishi"]:
			param_config["TuiShi"] = 1
	#print param_config

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
	#codeArray = ['399678']
	#show_extra_index(codeArray)


param_config = {
	"NoLog":0,
	"NoDetail":0,
	"SortByTime":0,
	"NotAllInfo":0,
	"TuiShi":0,
}
REAL_PRE_FD = "../data/"

#http://hq.sinajs.cn/list=sh000001,sz399001,sz399005,sz399006,sz399678

#Main Start:
if __name__=='__main__':
	beginTm = datetime.datetime.now()
	sysstr = platform.system()
	
	flname = REAL_PRE_FD + "realtime.txt"
	#TODO: open the comment
	if os.path.isfile(flname):
		os.remove(flname)
	sys.stdout = Logger_IO(flname)

	handle_argument()
	t_fmt = '%d-%02d-%02d %02d:%02d'
	fmt_time = t_fmt %(beginTm.year, beginTm.month, beginTm.day, beginTm.hour, beginTm.minute)

	cur1 = datetime.datetime.now()
	print "TIME:",fmt_time
	
	show_idx = ['000001', '399001', '399005', '399006','399678']
	show_real_index(show_idx)
	
	#get_all_stk_info() 进行日期处理，获取最新交易日期
	trade_date = get_lastday()
	pre_date = get_preday(1, trade_date)
	init_trade_list()
	#print ("Current trade day:", trade_date, pre_date)
	new_st_list = []
	new_st_code_list = []
	non_kb_list = []
	get_new_market_stock(trade_date, new_st_list, non_kb_list, new_st_code_list)
	#for item in non_kb_list:
	#	print item['securitycode'], item['securityshortname']
	#print(non_kb_list)

	#重出江湖STK
	fp_list = []
	fp_code_list = []
	pickup_fupai_item(trade_date, fp_list, fp_code_list)
	cur2 = datetime.datetime.now()
	#print("eee.py: get fupai", (cur2-cur1))
	#for it in fp_list:
	#	print it['obSeccode0111'],it['obSecname0111']
	
	#获取上一日的Info
	preFlag = 1
	preStatItem = statisticsItem()
	ret = parse_realtime_his_file(pre_date, preStatItem)
	if ret == -1:
		preFlag = 0
		print("Error:No find matched item", pre_date)
		exit(0)
	#print(preStatItem.lst_non_yzcx_yzzt)
	
	cur2 = datetime.datetime.now()
	#print("eee.py: parse pre rt file Fin", (cur2-cur1))
	
	debug = 0
	today_open = []
	
	#TODO: 如何调试呢？
	'''
	st_list=['603225','300116','600081','002113', '002676', '000862', '600119', '002309', '600262', '603663']
	debug = 1
	#print st_list
	'''
	#通过条件查询所有STK, start from 000001
	st_list = []
	ret = get_stk_code_by_dfcf(st_list, 'A', 0)
	#ret = get_stk_code_by_cond1(st_list, 'A', 0)
	if ret==-1:
		exit(0)
	
	#调试的时候移动注释到这一行下面
	cur2 = datetime.datetime.now()
	#print("eee.py: get all stk by cond Fin", (cur2-cur1))

	st_dict = {}
	st_dict['fup_stk'] = fp_code_list
	st_dict['new_stk'] = new_st_code_list
	st_dict['all_stk'] = st_list
	st_dict['nkb_stk'] = non_kb_list
	st_dict['tui_stk'] = []

	#print "=====>", len(stcsItem.lst_non_yzcx_zthl)
	stcsItem=statisticsItem()
	print trade_date
	status = collect_all_stock_data(st_dict, today_open, stcsItem, preStatItem, trade_date, debug)
	if status==-1:
		exit(0)

	cur2 = datetime.datetime.now()
	#print ("collect all Fin",(cur2-cur1))
	#exit(0)

	non_cx_yz = len(stcsItem.lst_non_yzcx_yzzt)
	cx_yz = stcsItem.s_yzzt-non_cx_yz

	#获取数据进行打印
	str_opn = "[%d %d %d %d] %3d 上,%3d 下" % (stcsItem.s_open_zt,stcsItem.s_close_zt,stcsItem.s_open_T_zt,stcsItem.s_dk_zt, stcsItem.s_sw_zt, stcsItem.s_xw_zt)
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
	kd_str = ','.join(stcsItem.lst_kd)
	if isinstance(kd_str, unicode): kd_str = kd_str.encode('gbk')
	print "%4d-CG(%d)	%4d-FT(%d)	%2d-YIN  KD:[%s]" %(stcsItem.s_zthl,len(stcsItem.lst_kd),stcsItem.s_dtft,dtft_qiang,stcsItem.s_zt_o_gt_c,kd_str)
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
		if isinstance(str, unicode):
			str = str.encode('gbk')
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
			if type(itm_lst[1]) is unicode:
				sname = itm_lst[1].encode('gbk')
			else:
				sname = itm_lst[1]
			str1 = "%s(%.2f%%, %.2f%%), " % (sname, itm_lst[2], itm_lst[4])
			str += str1
		print str

	str = ''
	list = stcsItem.lst_jc
	if len(list)>0:
		print "JC:"
		for i in range(0, len(list)):
			itm_lst = list[i]
			if type(itm_lst[1]) is unicode:
				sname = itm_lst[1].encode('gbk')
			else:
				sname = itm_lst[1]
			str1 = "%s(%.2f%%, %.2f%%), " % (sname, itm_lst[2], itm_lst[4])
			str += str1
		print str

	if param_config["NoDetail"]==0:
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

		if param_config["TuiShi"]==1:
			show_tuishi_info(st_dict['tui_stk'], fmt1)
	if param_config["NoLog"]==0:
		sys.stdout.flush()
		log = open(flname, 'r')
		content = log.read()
		log.close()

		fmt_time = '%d-%02d-%02d' %(beginTm.year, beginTm.month, beginTm.day)
		path = '../data/entry/realtime/'
		flname = path + "rt_" + fmt_time + ".txt"
		baklog = open(flname, 'a')
		baklog.write('#####quik_rt#########################################################\n')
		baklog.write(content)
		baklog.write('\n')
		baklog.close()

		tmp_file = path + "b_rt.txt"
		shutil.copy(flname, tmp_file)
	'''
	'''
	endTm = datetime.datetime.now()
	print "END ", (endTm-beginTm)
	cur2 = datetime.datetime.now()
	print ("delta=",(cur2-cur1))
