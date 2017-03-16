# -*- coding:gbk -*-
import sys
import re
import os
import time
import string
import datetime
import tushare as ts
import internal.common
from internal.ts_common import *

def show_zt_info(zt_list, desc):
	number = len(zt_list)
	if number<=0:
		return
	for i in range(0, number):
		itm_lst = zt_list[i]
		str = "%2d %6s %-7s	%8.2f %8.2f %8.2f %8.2f %8.2f" % (i+1,itm_lst[0],itm_lst[1],itm_lst[2],itm_lst[3],itm_lst[4],itm_lst[5],itm_lst[6])
		print str

def show_dt_info(dt_list, desc):
	number = len(dt_list)
	if number>0 and number<30:
		print desc, ":"
		for i in range(0, number):
			itm_lst = dt_list[i]
			str = "%2d %6s %-7s	%8.2f %8.2f %8.2f %8.2f %8.2f" % (i+1,itm_lst[0],itm_lst[1],itm_lst[2],itm_lst[3],itm_lst[4],itm_lst[5],itm_lst[6])
			print str
	elif number>=30:
		print desc," number too much:", number

def get_all_stk_info(st_list, today_open, stcsItem):
	today = datetime.date.today()
	number = len(st_list)
	if number<=0:
		return -1

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
				print "Get real time except:"
				time.sleep(0.5)
				LOOP_COUNT += 1
				stdf = None
			else:
				break
		if stdf is None:
			print "Get list fail at:", cur_list
			continue

		#print stdf
		yzcx_flag = 0
		for index,row in stdf.iterrows():
			stockInfo = []
			code = cur_list[index]
			index += 1
			name = row[0]
			pre_close = float(row['pre_close'])
			price = float(row['price'])

			#通过获得K线数据，判断是否YZZT新股
			if b_get_data == 1:
				#获得每只个股每天交易数据
				day_info_df = ts.get_k_data(code)
				#print day_info_df
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
					dt_str=day_info_df.iloc[trade_days-1,0]
					last_date = datetime.datetime.strptime(dt_str, '%Y-%m-%d').date()
					cmp_delta = today-last_date
					if cmp_delta.days==0:
						stcsItem.s_cx_yzzt += 1
						yzcx_flag = 1

				#认为YZZT不会超过 33 个交易日
				if trade_days>33:
					b_get_data = 0

			stk_type = analyze_status(code, name, row, stcsItem, yzcx_flag, pd_list)
	return 0

#Main Start:
pindex = len(sys.argv)

#show index information
show_idx = ['000001', '399001', '399005', '399006']
idx_df=ts.get_index()
show_index_info(idx_df, show_idx)

flag = 0
pindex = len(sys.argv)
if pindex==2:
	flag = int(sys.argv[1])

#得到所有交易item的code
LOOP_COUNT=0
st_today_base = None
while LOOP_COUNT<3:
	try:
		st_today_base = ts.get_today_all()
	except:
		LOOP_COUNT += 1
		time.sleep(0.5)
	else:
		break;
if st_today_base is None:
	print "Timeout to get stock basic info"
	exit(0)
st_today = st_today_base.sort_values(['changepercent'], 0, False)
new_st_list = []
for index,row in st_today.iterrows():
	code = row[0].encode('gbk')
	if row['changepercent']>11:
		new_st_list.append(code)
print ''

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

st_list = []
for i in range(0, len(new_st_list)):
	if new_st_list[i] in st_bas_list[0:10]:
		pass
	else:
		st_list.append(new_st_list[i])
st_list.extend(st_bas_list)

'''
st_list = []
st_list=['603977','000415','300611','601212','603281','300534']
#print st_list
'''

today_open = []
stcsItem=statisticsItem()
status = get_all_stk_info(st_list, today_open, stcsItem)
if status==-1:
	exit(0)

#获取数据进行打印
str_opn = "[%d %d %d %d]" % (stcsItem.s_open_zt,stcsItem.s_close_zt,stcsItem.s_open_T_zt,stcsItem.s_dk_zt)
print "%4d-ZT	%4d-DT		%d-X %d--%s" % (stcsItem.s_zt,stcsItem.s_dt,stcsItem.s_new,stcsItem.s_yzzt, str_opn)
print "%4d-CG	%4d-FT		KD:[%s]  %2d-YIN" %(stcsItem.s_zthl,stcsItem.s_dtft,','.join(stcsItem.lst_kd),stcsItem.s_zt_o_gt_c)
for i in range(0, len(stcsItem.lst_kd)):
	print stcsItem.lst_kd[i]
print "%4d(%4d)	ZERO:%4d	%4d(%4d)" %(stcsItem.s_open_sz, stcsItem.s_open_dz, stcsItem.s_open_pp, stcsItem.s_open_xd, stcsItem.s_open_dd)
print "%4d(%4d)	ZERO:%4d	%4d(%4d)" %(stcsItem.s_close_sz, stcsItem.s_close_dz, stcsItem.s_close_pp, stcsItem.s_close_xd, stcsItem.s_close_dd)
print "4%%:%4d	%4d" %(stcsItem.s_high_zf,stcsItem.s_low_df)
#print today_open

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

if flag==1:
	print "Non CiXin ZT:"
	print "id %6s %-12s	%-10s %-9s %-8s %-8s %-8s " % ("code","name","change","price","opn_p","hgh_p","low_p")
	show_zt_info(stcsItem.lst_non_yzcx_yzzt, "YZZT")
	print "--------------------"
	show_zt_info(stcsItem.lst_non_yzcx_zt, "ZT")
	print "==================================================="

	show_dt_info(stcsItem.lst_dt, "DT")
	show_dt_info(stcsItem.lst_dtft, "DTFT")