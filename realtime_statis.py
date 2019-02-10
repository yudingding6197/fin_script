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
from internal.ts_common import *
from internal.dfcf_interface import *

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

def get_all_stk_info(st_list, dc_data, today_open, stcsItem):
	today = datetime.date.today()
	number = len(st_list)
	if number<=0:
		return -1

	#得到ZS的信息，但是当天交易的时候，得不到当天的
	delta1=datetime.timedelta(days=30)
	sdate = today-delta1
	fmt_start = '%d-%02d-%02d' %(sdate.year, sdate.month, sdate.day)
	kdf = ts.get_k_data('000001', index=True, start=fmt_start)
	kdf = kdf.sort_values(['date'], 0, False)
	last_idx_date = kdf.iloc[0,0]
	#idx_date 得到最近一天交易的日期
	idx_date = datetime.datetime.strptime(last_idx_date, '%Y-%m-%d').date()

	#得到最近一天的实时信息，得到日期
	rq_idx = get_last_trade_dt()
	print rq_idx
	rq_idx_dt = datetime.datetime.strptime(rq_idx, '%Y-%m-%d').date()

	cmp_delta = rq_idx_dt-idx_date
	if cmp_delta.days>0:
		idx_date = rq_idx_dt

	b_get_data = 1
	#ZT一次取出 base 个
	#截取list，通过配置起始位置
	base = 23
	loop_ct = number/base
	if number%base!=0:
		loop_ct += 1

	pd_list = []
	for i in range(0, loop_ct):
		end_idx = min(base*(i+1), number)
		cur_list = st_list[i*base:end_idx]
		if len(cur_list)==0:
			break
		#print cur_list
		LOOP_COUNT = 0
		stdf = None
		while LOOP_COUNT<5:
			try:
				stdf = ts.get_realtime_quotes(cur_list)
			except:
				print cur_list, "Get real time except:", LOOP_COUNT
				time.sleep(0.5)
				LOOP_COUNT += 1
				stdf = None
			else:
				break
		if stdf is None:
			print "Get list fail at:", cur_list
			continue

		#print stdf
		for index,row in stdf.iterrows():
			stockInfo = []
			code = cur_list[index]
			index += 1
			if sysstr=="Windows":
				name = row[0].encode('gbk')
			elif sysstr == "Linux":
				name = row[0].encode('utf8')
			pre_close = float(row['pre_close'])
			price = float(row['price'])
			volumn = int(row['volume'])

			ask = float(row['ask'])
			if volumn==0 and dc_data==1:
				return 0
			if pre_close==0:
				print ("%s %s invalid value" %(code, name))
				continue
			change_perc = (price-pre_close)*100/pre_close
			today_high = float(row['high'])
			today_low = float(row['low'])
			today_b1_p = float(row['b1_p'])
			today_a1_p = float(row['a1_p'])
			today_bid = float(row['bid'])
			#判断今日是否trade suspend
			if today_high==today_low and today_high==0.0:
				continue
			elif today_b1_p==0.0 and today_a1_p==0.0 and today_bid==0.0:
				continue

			#通过获得K线数据，判断是否YZZT新股
			yzcx_flag = 0
			if b_get_data == 1:
				#获得每只个股每天交易数据
				day_info_df = None
				#新股上市可能有Bug
				try:
					day_info_df = ts.get_k_data(code)
				except:
					print "Error for code:", code, name
				if day_info_df is None:
					continue
				#print code, day_info_df
				trade_days = len(day_info_df)

				b_open=0
				yzzt_day = 0
				if trade_days==0:
					if name[0:1]=='N':
						stcsItem.s_new += 1
						yzcx_flag = 1
						continue
				if trade_days==1:
					if name[0:1]=='N':
						stcsItem.s_new += 1
						yzcx_flag = 1
				for tdidx,tdrow in day_info_df.iterrows():
					open = tdrow[1]
					close = tdrow[2]
					high = tdrow['high']
					low = tdrow['low']
					if high!=low:
						if yzzt_day!=0:
							if (yzzt_day+1)==trade_days:
								chg_perc = round((price-pre_close)*100/pre_close,2)
								open_list = [code, name, chg_perc, price, yzzt_day]
								today_open.append(open_list)
							b_open = 1
							break
					#当ZT打开，就会break for 循环
					yzzt_day += 1
					pre_close = close
				if b_open==0:
					try:
						dt_str=day_info_df.iloc[trade_days-1,0]
					except:
						print code,trade_days
						print day_info_df
						exit()
					last_date = datetime.datetime.strptime(dt_str, '%Y-%m-%d').date()
					#print code, name, idx_date,last_date
					cmp_delta = idx_date-last_date
					if cmp_delta.days==0:
						stcsItem.s_cx_yzzt += 1
						yzcx_flag = 1

				#如果是通过东财获得个股排行，不要判断新股的上市天数
				if dc_data==0:
					#认为YZZT不会超过 33 个交易日
					if trade_days>33:
						b_get_data = 0
				else:
					if trade_days>1:
						l_volume = float(day_info_df.iloc[trade_days-2,2])
						l_pclose = float(day_info_df.iloc[trade_days-2,2])
						l_close = float(day_info_df.iloc[trade_days-1,2])
						l_high = float(day_info_df.iloc[trade_days-1,3])
						chg_perc = round((l_close-l_pclose)*100/l_pclose,2)
						if l_close != l_high or chg_perc<9.5:
							b_get_data = 0
			
			stk_type = analyze_status(code, name, row, stcsItem, yzcx_flag, pd_list, idx_date)
	return 0

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

print "TIME:",fmt_time

#show index information
show_idx = ['000001', '399001', '399005', '399006']
idx_df=ts.get_index()
show_index_info(idx_df, show_idx)

codeArray = ['399678']
show_extra_index(codeArray)

flag = 0

param_config = {
	"NoLog":0,
	"NoDetail":0,
	"SortByTime":0,
	"AllInfo":0,
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
		param_config["AllInfo"] = 1
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
	baklog.write('##############################################################\n')
	baklog.write(content)
	baklog.write('\n')
	baklog.close()

	tmp_file = path + "b_rt.txt"
	shutil.copy(flname, tmp_file)
endTm = datetime.datetime.now()
print "END ", (endTm-beginTm)