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
import tushare as ts
import internal.common
from internal.output_general import *
from internal.ts_common import *
from internal.dfcf_inf import *
from internal.trade_date import *

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

#Main Start:
beginTm = datetime.datetime.now()
prepath = "../data/"
sysstr = platform.system()
cur=datetime.datetime.now()
fmt_time = '%d-%02d-%02d %02d:%02d' %(cur.year, cur.month, cur.day, cur.hour, cur.minute)
flname = prepath + "realtime.txt"
if os.path.isfile(flname):
	os.remove(flname)
#重定向同时输出到console和文件
sys.stdout = Logger_IO(flname)

print("Please first use quick search")
print "TIME:",fmt_time

#show index information
show_idx = ['000001', '399001', '399005', '399006','399678']
show_real_index(show_idx)

flag = 0
param_config = {
	"NoLog":0,
	"NoDetail":0,
	"SortByTime":0,
	"NotAllInfo":0,
	"DFCF":0,
}

optlist, args = getopt.getopt(sys.argv[1:], 'ldtac')
for option, value in optlist:
	if option in ["-l","--nolog"]:
		param_config["NoLog"] = 1
	elif option in ["-d","--nodetail"]:
		param_config["NoDetail"] = 1
	elif option in ["-t","--sbtime"]:
		param_config["SortByTime"] = 1
	elif option in ["-a","--all"]:
		param_config["NotAllInfo"] = 1
	elif option in ["-c","--dfcf"]:
		param_config["DFCF"] = 1
#print param_config

#comment加在这里便于调试
#得到所有交易item的code
new_st_list = []
st_list = []
if param_config["DFCF"]==1:
	get_stk_code_by_cond(st_list)
else:
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

	#st_list = st_list[0:50]

'''
st_list = []
st_list=['603225','300116','600081','002113', '002676', '000862', '600119', '002309', '600262', '603663']
#print st_list
'''

trade_date = get_lastday()
trdDt = datetime.datetime.strptime(trade_date, '%Y-%m-%d').date()
cybDt = datetime.datetime.strptime(CYB_REFORM_DT, '%Y-%m-%d').date()
if (trdDt-cybDt).days>=0:
	G_LARGE_FLUC[1] = '300'
	G_LARGE_FLUC[3] = '301'

today_open = []
stcsItem=statisticsItem()
status = get_all_stk_info(st_list, param_config["DFCF"], today_open, stcsItem)
if status==-1:
	exit(0)

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

if param_config["NoDetail"]==0:
	non_cx = len(stcsItem.lst_non_yzcx_yzzt)+len(stcsItem.lst_non_yzcx_zt)
	#YZ: %d=%d(%d)+%d 4项
	#%d: 总共YZZT的item，排除第一天挂牌N
	#%d: 还没有开板的CX
	#%d: 还没有开板的CX和第一天挂牌的总和
	#%d: 已经开板的所有item，不限于CX
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

if param_config["NoLog"]==0:
	sys.stdout.flush()
	log = open(flname, 'r')
	content = log.read()
	log.close()

	fmt_time = '%d-%02d-%02d' %(cur.year, cur.month, cur.day)
	path = '../data/entry/realtime/'
	flname = path + "rt_" + fmt_time + ".txt"
	baklog = open(flname, 'a')
	baklog.write('#####V2#######################################################\n')
	baklog.write(content)
	baklog.write('\n')
	baklog.close()

	tmp_file = path + "b_rt.txt"
	shutil.copy(flname, tmp_file)
endTm = datetime.datetime.now()
print "END ", (endTm-beginTm)