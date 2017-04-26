#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import time
import string
import datetime
import tushare as ts
from internal.ts_common import *
from decimal import Decimal

today = datetime.date.today()

#说明show_flag
#0：不获得每一只的流通盘，不会计算换手率
#1：获得每一只的流通盘，并且计算换手率
#2：显示每一只最新的新闻，当天的新闻全部显示，当天没有只显示一条news
pindex = len(sys.argv)

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
#new_st_list = list(st_today[st_today.changepercent>11]['code'])
new_st_list = []
for index,row in st_today.iterrows():
	code = row[0].encode('gbk')
	if row['changepercent']>11:
		new_st_list.append(code)
print ''
#print new_st_list

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
#st_bas.to_excel("a_stock_base.xlsx")
#st_pb_base.to_excel("a_stock_pb_base.xlsx")
#print st_pb_base.head(10)

st_list = []
for i in range(0, len(new_st_list)):
	if new_st_list[i] in st_bas_list[0:10]:
		pass
	else:
		st_list.append(new_st_list[i])
st_list.extend(st_bas_list)

'''
st_list = st_list[0:60]
st_list.append('300175')
st_list.append('603558')
#st_list=['600828','002819','300611']
#print st_list
'''

number = len(st_list)
if number<=0:
	exit(0)

today_open = []
stcsItem=statisticsItem()
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
	excecount = 0
	stdf = None
	while excecount<5:
		try:
			stdf = ts.get_realtime_quotes(cur_list)
		except:
			print "Get except:"
			time.sleep(0.5)
			excecount += 1
			if excecount<5:
				continue
			stdf = None
			break
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
			if trade_days==1:
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
	#if i>2:
	#	break

#if len(pd_list)>0:
#	df_tdy = pd.DataFrame(pd_list)
#	df_tdy1 = df_tdy.sort_values([0], 0, False)

str_opn = "[%d %d %d %d]" % (stcsItem.s_open_zt,stcsItem.s_close_zt,stcsItem.s_open_T_zt,stcsItem.s_dk_zt)
print "%4d-ZT	%4d-DT		%d-X %d--%s" % (stcsItem.s_zt,stcsItem.s_dt,stcsItem.s_new,stcsItem.s_yzzt, str_opn)
print "%4d-CG	%4d-FT		KD:[%s]  %2d-YIN" %(stcsItem.s_zthl,stcsItem.s_dtft,','.join(stcsItem.lst_kd),stcsItem.s_zt_o_gt_c)
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
else:
	print "NB:====="
print ''

str = ''
list = stcsItem.lst_jc
if len(list)>0:
	print "JC:"
	for i in range(0, len(list)):
		itm_lst = list[i]
		str1 = "%s(%.2f%%, %.2f%%), " % (itm_lst[1], itm_lst[2], itm_lst[4])
		str += str1
	print str
else:
	print "JC:====="

#print '\n'.join(['%s:%s' % item for item in stcsItem.__dict__.items()])
