#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import string
import datetime
import platform
import shutil
import getopt
import pandas as pd

sys.path.append('.')
from internal.handle_realtm import *
#from internal.dfcf_inf import *
#from internal.ts_common import show_index_info
from internal.trade_date import *
from internal.update_tday_db import *
from internal.analyze_realtime import *
from internal.compare_realtime import *
from internal.tingfupai import * 
from internal.common_inf import *
from internal.parse_juchao import *


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
	optlist, args = getopt.getopt(sys.argv[1:], 'd:')
	for option, value in optlist:
		if option in ["-l","--nolog"]:
			param_config["NoLog"] = 1
		elif option in ["-d","--date"]:
			param_config["Date"] = value
		elif option in ["-t","--sbtime"]:
			param_config["SortByTime"] = 1
		elif option in ["-a","--all"]:
			param_config["NotAllInfo"] = 1
		elif option in ["-c","--dfcf"]:
			param_config["DFCF"] = 1
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
	"Date":'',
}
REAL_DAILY_PRE_FD = "../data/"

#Main Start:
if __name__=='__main__':
	beginTm = datetime.datetime.now()
	sysstr = platform.system()
	
	flname = REAL_DAILY_PRE_FD + "realtime.txt"
	#TODO: open the comment
	if os.path.isfile(flname):
		os.remove(flname)
	sys.stdout = Logger_IO(flname)

	handle_argument()
	if param_config["Date"]=='':
		print("Error,must need arg -dYYYYMMDD")
		exit(0)
	ret,trade_date=parseDate2(param_config["Date"])
	
	t_fmt = '%d-%02d-%02d %02d:%02d'
	fmt_time = t_fmt %(beginTm.year, beginTm.month, beginTm.day, beginTm.hour, beginTm.minute)

	cur1 = datetime.datetime.now()
	print "TIME:",fmt_time
	
	show_idx = ['000001', '399001', '399005', '399006','399678']
	show_real_index(show_idx)
	
	#get_all_stk_info() 进行日期处理，获取最新交易日期
	pre_date = get_preday(1, trade_date)
	init_trade_list()
	
	year = trade_date[:4]
	jcLoc = "../data/entry/juchao/" + year + '/jc' + trade_date + ".txt"
	if os.path.exists(jcLoc) is False:
		print(jcLoc,"not exist.")
		exit(0)
	jc_dict = {}
	read_tips_info(jcLoc, jc_dict)
	
	
	print ("Current trade day:", trade_date, pre_date)
	
	#获取上一日的Info
	preFlag = 1
	preStatItem = statisticsItem()
	ret = parse_realtime_his_file(pre_date, preStatItem)
	if ret == -1:
		preFlag = 0
		print("Error:No find matched item", pre_date)
		exit(0)
	#print(json.dumps(preStatItem.lst_non_yzcx_yzzt, ensure_ascii=False, encoding='gbk').encode('gbk'))
	
	debug = 0
	today_open = []

	'''
	#TODO: 如何调试呢？
	st_list=['603225','300116','600081','002113', '002676', '000862', '600119', '002309', '600262', '603663']
	debug = 1
	#print st_list
	'''
	#通过条件查询所有STK, start from 000001
	
	st_list = []
	flname = '../data/daily/' + trade_date +"/"+ trade_date + "xd.txt"
	hisFile = open(flname, "r")
	st_list = json.load(hisFile, encoding='gbk')
	hisFile.close()

	st_dict = {}
	st_dict['fup_stk'] = jc_dict['fupai']
	st_dict['new_stk'] = jc_dict['newmk']
	st_dict['all_stk'] = st_list
	st_dict['nkb_stk'] = []

	#print "=====>", len(stcsItem.lst_non_yzcx_zthl)
	stcsItem=statisticsItem()
	print trade_date
	status = collect_all_stock_data2(st_dict, today_open, stcsItem, preStatItem, trade_date, debug)
	if status==-1:
		exit(0)

	exit(0)
	
	'''
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

	cur2 = datetime.datetime.now()
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
	endTm = datetime.datetime.now()
	print "END ", (endTm-beginTm)
	cur2 = datetime.datetime.now()
	print ("delta=",(cur2-cur1))
	'''
