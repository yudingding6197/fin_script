# -*- coding:gbk -*-
import sys
import re
import os
import time
import string
import datetime
import tushare as ts
from internal.ts_common import *

today = datetime.date.today()

#说明show_flag
#0：不获得每一只的流通盘，不会计算换手率
#1：获得每一只的流通盘，并且计算换手率
#2：显示每一只最新的新闻，当天的新闻全部显示，当天没有只显示一条news
pindex = len(sys.argv)

st_today_base = ts.get_today_all()
st_today = st_today_base.sort_values(['changepercent'], 0, False)
#new_st_list = list(st_today[st_today.changepercent>11]['code'])
new_st_list = []
for index,row in st_today.iterrows():
	code = row[0].encode('gbk')
	if row['changepercent']>11:
		new_st_list.append(code)
print ''
#print new_st_list

st_bas=ts.get_stock_basics()
st_pb_base = st_bas[st_bas.pb!=0]
st_pb_base = st_pb_base.sort_values(['timeToMarket'], 0, False)
st_index = st_pb_base.index
st_bas_list=list(st_index)
#st_bas.to_excel("a_stock_base.xlsx")
#st_pb_base.to_excel("a_stock_pb_base.xlsx")
#print st_pb_base.head(10)
'''
st_list=['002740','300364','002850']
print st_list
'''

st_list = []
for i in range(0, len(new_st_list)):
	if new_st_list[i] in st_bas_list[0:10]:
		pass
	else:
		st_list.append(new_st_list[i])
st_list.extend(st_bas_list)
	
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

		#通过获得K线数据，判断是否YZZT新股
		if b_get_data == 1:
			#获得每只个股每天交易数据
			day_info_df = ts.get_k_data(code)
			#print day_info_df
			trade_days = len(day_info_df)

			b_open=0
			yzzt_day = 0
			for tdidx,tdrow in day_info_df.iterrows():
				open = tdrow[1]
				close = tdrow[2]
				high = tdrow['high']
				low = tdrow['low']
				if high!=low:
					if yzzt_day!=0:
						if (yzzt_day+1)==trade_days:
							today_open.append(code)
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

			#认为YZZT不会超过 33 个交易日
			if trade_days>33:
				b_get_data = 0

		stk_type = analyze_status(code, name, row, stcsItem)
	#if i>2:
	#	break
print '\n'.join(['%s:%s' % item for item in stcsItem.__dict__.items()])
