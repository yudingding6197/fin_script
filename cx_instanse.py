# -*- coding:gbk -*-
import sys
import re
import os
import time
import string
import datetime
import pandas as pd
import tushare as ts
from internal.ts_common import *
from decimal import Decimal

def handle_st_data(code, name, row):
	if len(code)!=6:
		return 0
	if code.isdigit() is False:
		return 0

	status = 0
	high = float(row['high'])
	low = float(row['low'])
	open = float(row['open'])
	price = float(row['price'])
	pre_close = float(row['pre_close'])

	#排除当天没有交易
	if pre_close==0:
		print "PRE_CLOSE Not exist!!!", code, name
		return 0

	if high==0 or low==0:
		return 0

	b_ST = 0
	if name.find("ST")>=0 or name.find("st")>=0:
		b_ST = 1
		#print code,name

def output_info(desc, type, stk_list):
	print "%s(%d)" % (desc, len(stk_list))
	if len(stk_list)<=0:
		return

	df_tdy = pd.DataFrame(stk_list)
	if type==1:
		df_tdy1 = df_tdy.sort_values([2], 0, False)
	elif type==2:
		df_tdy1 = df_tdy.sort_values([5], 0, False)
	else:
		return

	id = 0
	for index, row in df_tdy1.iterrows():
		id += 1
		if type==1:
			print "%2d %6s %-7s	%8.2f %8.2f %8.2f %8.2f %8.2f %6d" % (id,row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
		elif type==2:
			print "%2d %6s %-7s	%8.2f %8.2f %3d %8d" % (id,row[0],row[1],row[2],row[3],row[4],row[5])
	print ''


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

st_list = []
for i in range(0, len(new_st_list)):
	if new_st_list[i] in st_bas_list[0:10]:
		pass
	else:
		st_list.append(new_st_list[i])
st_list.extend(st_bas_list)

'''
st_list = ['603603','300613','300601','002849','300616','002852','603955','601212']
'''

number = len(st_list)
if number<=0:
	exit(0)

today_open = []
two_day_open = []
three_day_open = []
four_day_open = []
new_stk = []
stcsItem=statisticsItem()
b_get_data = 1
#ZT一次取出 base 个
#截取list，通过配置起始位置
base = 23
loop_ct = number/base
if number%base!=0:
	loop_ct += 1
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
	for index,row in stdf.iterrows():
		stockInfo = []
		code = cur_list[index]
		index += 1
		name = row[0]
		high = float(row['high'])
		low = float(row['low'])
		open = float(row['open'])
		price = float(row['price'])
		pre_close = float(row['pre_close'])
		if high==0 or low==0:
			continue

		o_percent = (open-pre_close)*100/pre_close
		c_percent = (price-pre_close)*100/pre_close
		h_percent = (high-pre_close)*100/pre_close
		l_percent = (low-pre_close)*100/pre_close
		open_percent = float('{:.2f}'.format(Decimal(str(o_percent))))
		change_percent = float('{:.2f}'.format(Decimal(str(c_percent))))
		high_zf_percent = float('{:.2f}'.format(Decimal(str(h_percent))))
		low_df_percent = float('{:.2f}'.format(Decimal(str(l_percent))))
		by1_vol = 0
		if row['b1_v'].isdigit():
			by1_vol = int(row['b1_v'])

		#通过获得K线数据，判断是否YZZT新股
		if b_get_data == 1:
			#获得每只个股每天交易数据
			day_info_df = ts.get_k_data(code)
			trade_days = len(day_info_df)

			b_open=0
			yzzt_day = 0
			if trade_days==0:
				stcsItem.s_new += 1
				continue
			if trade_days==1:
				if name[0:1]=='N':
					stcsItem.s_new += 1
			for tdidx,tdrow in day_info_df.iterrows():
				h_open = tdrow[1]
				h_close = tdrow[2]
				h_high = tdrow['high']
				h_low = tdrow['low']
				if h_high!=h_low:
					if yzzt_day!=0:
						list = []
						if (yzzt_day+4)>=trade_days:
							list = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent, yzzt_day]

						if (yzzt_day+1)==trade_days:
							today_open.append(list)
						elif (yzzt_day+2)==trade_days:
							two_day_open.append(list)
						elif (yzzt_day+3)==trade_days:
							three_day_open.append(list)
						elif (yzzt_day+4)==trade_days:
							four_day_open.append(list)
						b_open = 1
						break
				#当ZT打开，就会break for 循环
				yzzt_day += 1
			if b_open==0:
				dt_str=day_info_df.iloc[trade_days-1,0]
				last_date = datetime.datetime.strptime(dt_str, '%Y-%m-%d').date()
				cmp_delta = today-last_date
				if cmp_delta.days==0:
					stcsItem.s_cx_yzzt += 1
					list = [code, name, change_percent, price, yzzt_day, by1_vol]
					new_stk.append(list)

			#认为YZZT不会超过 33 个交易日
			if trade_days>33:
				b_get_data = 0
				break
	if b_get_data==0:
		break

output_info("One   Day", 1, today_open)
output_info("Two   Day", 1, two_day_open)
output_info("Thr   Day", 1, three_day_open)
output_info("Fur   Day", 1, four_day_open)
output_info("YZZT Len", 2, new_stk)