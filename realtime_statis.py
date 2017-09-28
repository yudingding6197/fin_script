#!/usr/bin/env python
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
	endstr = ''
	if number<=0:
		return
	elif number>30:
		number = 30
		endstr = '......'
	'''
	for i in range(0, number):
		itm_lst = zt_list[i]
		str = "%2d %6s %-7s	%8.2f %8.2f %8.2f %8.2f %8.2f" % (i+1,itm_lst[0],itm_lst[1],itm_lst[2],itm_lst[3],itm_lst[4],itm_lst[5],itm_lst[6])
		print str
	'''
	df = pd.DataFrame(zt_list)
	df = df.sort_values([7], 0, False)
	i = 1
	for index,itm_lst in df.iterrows():
		str = "%2d %6s %-7s	%8.2f %8.2f %8.2f %8.2f %8.2f %4d" % (i,itm_lst[0],itm_lst[1],itm_lst[2],itm_lst[3],itm_lst[4],itm_lst[5],itm_lst[6],itm_lst[7])
		print str
		i += 1
		if i>number:
			break
	print endstr

def show_dt_info(dt_list, desc):
	number = len(dt_list)
	endstr = ''
	str = "%s [%d]:" % (desc, number)
	if number<=0:
		return
	elif number>30:
		number = 30
		endstr = '......'

	df = pd.DataFrame(dt_list)
	if desc=="DT" or desc=="YZDT":
		df = df.sort_values([7], 0, False)
	else:
		df = df.sort_values([2], 0, False)
	i = 1
	print str
	for index,itm_lst in df.iterrows():
		if desc=="DT" or desc=="YZDT":
			str = "%2d %6s %-7s	%8.2f %8.2f %8.2f %8.2f %8.2f %4d" % (i,itm_lst[0],itm_lst[1],itm_lst[2],itm_lst[3],itm_lst[4],itm_lst[5],itm_lst[6],itm_lst[7])
		else:
			str = "%2d %6s %-7s	%8.2f %8.2f %8.2f %8.2f %8.2f %4d" % (i,itm_lst[0],itm_lst[1],itm_lst[2],itm_lst[3],itm_lst[4],itm_lst[5],itm_lst[6],itm_lst[7])
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

def get_all_stk_info(st_list, today_open, stcsItem):
	today = datetime.date.today()
	number = len(st_list)
	if number<=0:
		return -1

	#�õ�ZS����Ϣ�����ǵ��콻�׵�ʱ�򣬵ò��������
	delta1=datetime.timedelta(days=30)
	sdate = today-delta1
	fmt_start = '%d-%02d-%02d' %(sdate.year, sdate.month, sdate.day)
	kdf = ts.get_k_data('000001', index=True, start=fmt_start)
	kdf = kdf.sort_values(['date'], 0, False)
	last_idx_date = kdf.iloc[0,0]
	#idx_date �õ����һ�콻�׵�����
	idx_date = datetime.datetime.strptime(last_idx_date, '%Y-%m-%d').date()

	#�õ����һ���ʵʱ��Ϣ���õ�����
	idx_df = ts.get_realtime_quotes('399001')
	rq_idx = idx_df.ix[0,'date']
	rq_idx_dt = datetime.datetime.strptime(rq_idx, '%Y-%m-%d').date()

	cmp_delta = rq_idx_dt-idx_date
	if cmp_delta.days>0:
		idx_date = rq_idx_dt

	b_get_data = 1
	#ZTһ��ȡ�� base ��
	#��ȡlist��ͨ��������ʼλ��
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
			name = row[0]
			pre_close = float(row['pre_close'])
			price = float(row['price'])
			change_perc = (price-pre_close)*100/pre_close
			today_high = float(row['high'])
			today_low = float(row['low'])
			today_b1_p = float(row['b1_p'])
			today_a1_p = float(row['a1_p'])
			today_bid = float(row['bid'])
			#�жϽ����Ƿ�trade suspend
			if today_high==today_low and today_high==0.0:
				continue
			elif today_b1_p==0.0 and today_a1_p==0.0 and today_bid==0.0:
				continue

			#ͨ�����K�����ݣ��ж��Ƿ�YZZT�¹�
			yzcx_flag = 0
			if b_get_data == 1:
				#���ÿֻ����ÿ�콻������
				day_info_df = None
				#�¹����п�����Bug
				try:
					day_info_df = ts.get_k_data(code)
				except:
					print "Error for code:", code, name
				if day_info_df is None:
					continue
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
					#print tdrow
					if high!=low:
						if yzzt_day!=0:
							if (yzzt_day+1)==trade_days:
								chg_perc = round((price-pre_close)*100/pre_close,2)
								open_list = [code, name, chg_perc, price, yzzt_day]
								today_open.append(open_list)
							b_open = 1
							break
					#��ZT�򿪣��ͻ�break for ѭ��
					yzzt_day += 1
					pre_close = close
				if b_open==0:
					dt_str=day_info_df.iloc[trade_days-1,0]
					last_date = datetime.datetime.strptime(dt_str, '%Y-%m-%d').date()
					#print code, name, idx_date,last_date
					cmp_delta = idx_date-last_date
					if cmp_delta.days==0:
						stcsItem.s_cx_yzzt += 1
						yzcx_flag = 1

				#��ΪYZZT���ᳬ�� 33 ��������
				if trade_days>33:
					b_get_data = 0
			stk_type = analyze_status(code, name, row, stcsItem, yzcx_flag, pd_list, idx_date)
	return 0

#Main Start:
pindex = len(sys.argv)
cur=datetime.datetime.now()
fmt_time = '%d-%02d-%02d %02d:%02d' %(cur.year, cur.month, cur.day, cur.hour, cur.minute)
print "TIME:",fmt_time

#show index information
show_idx = ['000001', '399001', '399005', '399006']
idx_df=ts.get_index()
show_index_info(idx_df, show_idx)

flag = 0
pindex = len(sys.argv)
if pindex==2:
	flag = int(sys.argv[1])

#�õ����н���item��code
new_st_list = []

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

st_list = []
for i in range(0, len(new_st_list)):
	if new_st_list[i] in st_bas_list[0:10]:
		pass
	else:
		st_list.append(new_st_list[i])
st_list.extend(st_bas_list)

#st_list = st_list[0:50]

'''
st_list = []
st_list=['603225','002050','002282','300597']
#print st_list
'''

today_open = []
stcsItem=statisticsItem()
status = get_all_stk_info(st_list, today_open, stcsItem)
if status==-1:
	exit(0)

non_cx_yz = len(stcsItem.lst_non_yzcx_yzzt)
cx_yz = stcsItem.s_yzzt-non_cx_yz

#��ȡ���ݽ��д�ӡ
str_opn = u"[%d %d %d %d] %3d��,%3d��" % (stcsItem.s_open_zt,stcsItem.s_close_zt,stcsItem.s_open_T_zt,stcsItem.s_dk_zt, stcsItem.s_sw_zt, stcsItem.s_xw_zt)

str_dt = "DTKP:%d" % (stcsItem.s_open_dt)
if stcsItem.s_yzdt>0:
	str_dt = "%s YZDT:%d" % (str_dt, stcsItem.s_yzdt)
if stcsItem.s_open_dt_dk>0:
	str_dt = "%s DTDK:%d" % (str_dt, stcsItem.s_open_dt_dk)
DaoT = stcsItem.s_open_dt-stcsItem.s_yzdt-stcsItem.s_open_dt_dk
if DaoT>0:
	str_dt = "%s DaoT:%d" % (str_dt, DaoT)
print "			ST(%d ZT %d DT)		%s" % (stcsItem.s_st_yzzt, stcsItem.s_st_yzdt, str_dt)
#print "			ST(%d ZT %d DT)		DTKP:%d YZDT:%d DTDK:%d" % (stcsItem.s_st_yzzt, stcsItem.s_st_yzdt, stcsItem.s_open_dt, stcsItem.s_yzdt,stcsItem.s_open_dt_dk)

dtft_qiang = filter_dtft(stcsItem.lst_dtft, -3)
print "%4d-ZT		%4d-DT		%d-X %d--(%d+%d) %s" % (stcsItem.s_zt,stcsItem.s_dt,stcsItem.s_new,stcsItem.s_yzzt, cx_yz, non_cx_yz, str_opn)
print "%4d-CG(%d)	%4d-FT(%d)	%2d-YIN  KD:[%s]" %(stcsItem.s_zthl,len(stcsItem.lst_kd),stcsItem.s_dtft,dtft_qiang,stcsItem.s_zt_o_gt_c,','.join(stcsItem.lst_kd))
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

if flag==0:
	non_cx = len(stcsItem.lst_non_yzcx_yzzt)+len(stcsItem.lst_non_yzcx_zt)
	tol_str = "Total( %d = %d + %d	YZ: %d=%d(%d)+%d):"
	print tol_str%( stcsItem.s_zt, stcsItem.s_zt-non_cx, non_cx, stcsItem.s_yzzt, cx_yz, stcsItem.s_cx_yzzt, non_cx_yz)
	print "id %6s %-12s	%-10s %-9s %-8s %-8s %-8s %-8s" % ("code","name","change","price","opn_p","hgh_p","low_p","z_d")
	show_zt_info(stcsItem.lst_non_yzcx_yzzt, "YZZT")
	print "-------------------- %d+%d" % (stcsItem.s_sw_zt, stcsItem.s_xw_zt)
	show_zt_info(stcsItem.lst_non_yzcx_zt, "ZT")
	print "==================================================="

	show_dt_info(stcsItem.lst_yzdt, "YZDT")
	show_dt_info(stcsItem.lst_dt, "DT")
	show_dt_info(stcsItem.lst_dtft, "DTFT")