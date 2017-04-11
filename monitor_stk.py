# -*- coding:gbk -*-
import sys
import re
import os
import time
import string
import datetime
from internal.ts_common import *

'''
curdate = ''
data_path = "..\\Data\\_tmp1.txt"
stockCode = []

today = datetime.date.today()
curdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)
#print curdate

if os.path.isfile(data_path) is False:
	print "No file:",data_path
	exit(0)

file = open(data_path, 'r')
while 1:
	lines = file.readlines(100000)
	if not lines:
		break
	for line in lines:
		code=line.strip()
		if code.isdigit() is False:
			continue;
		if len(code)!=6:
			if len(code)==7:
				code = code[1:7]
			else:
				continue;
		stockCode.append(code)
		#print code
file.close()

if len(stockCode)==0:
	exit(0)
'''

def get_new_stk_by_ts(yzzt_list, today_open):
	index = -1
	today = datetime.date.today()

	df = ts.get_stock_basics()
	df1 = df.sort_values(['timeToMarket'], 0, False)
	#print df1

	for code,row in df1.iterrows():
		stockInfo = []
		index += 1
		name = row[0].decode('utf8')
		trade_item = row['timeToMarket']
		ltgb = row['outstanding']
		zgb = row['totals']
		#print type(trade_item) 竟然是 long 类型
		#trade_string = str(long(trade_item))
		#trade_date = datetime.datetime.strptime(trade_string, '%Y%m%d').date()
		#delta = trade_date - base_date
		#if delta.days<0:
		#	break

		#获得每只个股每天交易数据
		day_info_df = ts.get_k_data(code)
		#print day_info_df

		b_open = 0
		yzzt_day = 0
		last_close = 0.0
		td_total = len(day_info_df)
		#认为YZZT不会超过 33 个交易日
		if td_total>33:
			break
		for tdidx,tdrow in day_info_df.iterrows():
			open = tdrow[1]
			close = tdrow[2]
			high = float(tdrow['high'])
			low = float(tdrow['low'])
			if high!=low:
				if yzzt_day!=0:
					if (yzzt_day+1)==td_total:
						today_open.append(code)
					b_open = 1
					break

			#当ZT打开，就会break for 循环
			yzzt_day += 1
		if b_open==0:
			dt_str=day_info_df.iloc[td_total-1,0]
			last_date = datetime.datetime.strptime(dt_str, '%Y-%m-%d').date()
			cmp_delta = today-last_date
			if cmp_delta.days==0:
				yzzt_list.append(code)

def get_new_stk_by_file(yzzt_list, today_open):			
	data_path = "..\\Data\\entry\\_no_open_cx.txt"

	if os.path.isfile(data_path) is False:
		print "No file:",data_path
		exit(0)

	file = open(data_path, 'r')
	while 1:
		lines = file.readlines(100000)
		if not lines:
			break
		for line in lines:
			code = line.strip()
			if len(code)!=6:
				continue
			if code.isdigit() is False:
				continue
			yzzt_list.append(code)
	file.close()

#读取每一只的信息，判断是否超过基线范围
def check_zt_status(yzzt_list, today_open):
	df=ts.get_realtime_quotes(yzzt_list)
	#df=ts.get_realtime_quotes('000520')
	yzztidx = 0
	for index,row in df.iterrows():
		high = float(row['high'])
		low = float(row['low'])
		#print row['code'],row['name'],high,low
		#此时不再是YZZT态,将数据pop out，可能停牌
		if high!=low or (high==0.0 and low==0.0):
			if high!=0:
				print yzzt_list[yzztidx],row[0], "NOT YZ"
				today_open.append(yzzt_list[yzztidx])

			yzzt_list.pop(yzztidx)
			base_line.pop(yzztidx)
			buy1_vol.pop(yzztidx)
			continue

		#a代表卖，b代表买
		a1_v = row['a1_v']
		a1_p = row['a1_p']
		if row['b1_v']=="":
			b1_v = 0
		else:
			b1_v = int(row['b1_v'])
		b1_p = row['b1_p']
		#print yzztidx,yzzt_list[yzztidx], a1_p, b1_p

		if b1_v<base_line[yzztidx]:
			if base_line[yzztidx]>2000:
				print "!!!!! Change Base Line:%6s	%5s	%8d"%(yzzt_list[yzztidx],row[0],b1_v)
				base_line[yzztidx]=2000
			elif base_line[yzztidx]==2000:
				print "!!!!! Alarm will OPENN:%6s	%5s	%8d"%(yzzt_list[yzztidx],row[0],b1_v)
			yzztidx += 1
			continue
		if buy1_vol[yzztidx]<=b1_v:
			buy1_vol[yzztidx] = b1_v
			yzztidx += 1
			continue

		delta = buy1_vol[yzztidx]-b1_v
		if delta>base_line[yzztidx]:
			print "!!!!! Quickly MISSS:%6s	%5s	%8d	%d,%d,%d"%(yzzt_list[yzztidx],row[0],b1_v,delta,base_line[yzztidx],buy1_vol[yzztidx])
			buy1_vol[yzztidx] = b1_v
		#print yzzt_list[yzztidx], row[0], b1_p, b1_v
		yzztidx += 1


# Main
today_open = []
yzzt_list = []

#get_new_stk_by_file(yzzt_list, today_open)
get_new_stk_by_ts(yzzt_list, today_open)
if len(yzzt_list)==0:
	print "No CX Data"
	exit(0)

'''
print "DAKA：",len(today_open)
print today_open
print "==============="
print "YIZI：",len(yzzt_list)
print yzzt_list
'''

#首先得到 By1量，设置初始基线
buy1_vol = []
base_line = []
df=ts.get_realtime_quotes(yzzt_list)
new_yzzt = []
for index,row in df.iterrows():
	if row['b1_v']=='':
		print "Warning: ", yzzt_list[index], "no BUY item"
		continue
	new_yzzt.append(yzzt_list[index])
	buy1_vol.append(int(row['b1_v']))
	base_line.append(10000)
	print "%6s	%5s	%.2f	%8s"%(yzzt_list[index], row[0], float(row['b1_p']), row['b1_v'])
yzzt_list = new_yzzt

#开始循环检查 By1 量的状态
while 1:
	if len(yzzt_list)==0:
		break;
	openlen = len(today_open)
	check_zt_status(yzzt_list, today_open)
	if openlen != len(today_open):
		print "New Open ST:", today_open
	time.sleep(0.5)