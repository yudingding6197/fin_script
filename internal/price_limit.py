#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import re
import os
import time
import string
import datetime
import platform
import shutil
import getopt
import urllib2,time
import datetime

sys.path.append(".")
from url_dfcf.dc_hangqing import *
from url_dfcf.limit_ban import *
from url_sina.sina_inf import *
from internal.math_common import *
from internal.trade_date import *
from internal.global_var import *

def handle_today_ticks(df, code, trade_date, chk_price, type):
	tmstr = '??:??'
	return tmstr

def get_kline5_data(code, length):
	klist = get_k5_data_bysn(code, len=length)
	return klist

def get_kline_day_data(code, length):
	klist = get_kday_data_bysn(code, len=length)
	return klist
	
# minute: 期望减去几分钟，如果是涨跌停开板时间不用减
# flag: 是否加上？号，有的涨跌停就是一瞬间，意义不大
def covert_time_fmt(tmobj, minute, flag):
	#将当前时间减去5分钟
	dt = datetime.datetime.strptime(tmobj, "%Y-%m-%d %H:%M:%S")
	newdt = dt - datetime.timedelta(minutes=minute)
	tmNewObj = newdt.strftime("%Y-%m-%d %H:%M")

	timeObj = re.match(r'.* (\d{2}):(\d{2})', tmNewObj)
	if (timeObj is None):
		print code, "非法时间格式2：" +str(row['date'])+ ", 期望格式: HH:MM"
		return ''
	hour = int(timeObj.group(1))
	minute = int(timeObj.group(2))
	if hour<=11:
		if flag==1:
			tmstr = "%02d:%02d??" %(hour, minute)
		else:
			tmstr = "%02d:%02d" %(hour, minute)
	else:
		if flag==1:
			tmstr = "%02d:%02d--??" %(hour, minute)
		else:
			tmstr = "%02d:%02d--" %(hour, minute)
	#if hour<=11:
	#	tmstr = "%02d:%02d??" %(hour, minute)
	#else:
	#	tmstr = "%02d:%02d--??" %(hour, minute)
	return tmstr

def covert_only_time_fmt(tmobj, minute, flag):
	#将当前时间减去5分钟
	dt = datetime.datetime.strptime(tmobj, "%H:%M")
	newdt = dt - datetime.timedelta(minutes=minute)
	tmNewObj = newdt.strftime("%H:%M")

	timeObj = re.match(r'(\d{2}):(\d{2})', tmNewObj)
	if (timeObj is None):
		print code, "非法时间格式3：" +str(row['date'])+ ", 期望格式: HH:MM"
		return ''
	hour = int(timeObj.group(1))
	minute = int(timeObj.group(2))
	if hour<=11:
		if flag==1:
			tmstr = "%02d:%02d??" %(hour, minute)
		else:
			tmstr = "%02d:%02d" %(hour, minute)
	else:
		if flag==1:
			tmstr = "%02d:%02d--??" %(hour, minute)
		else:
			tmstr = "%02d:%02d--" %(hour, minute)
	#if hour<=11:
	#	tmstr = "%02d:%02d??" %(hour, minute)
	#else:
	#	tmstr = "%02d:%02d--??" %(hour, minute)
	#print tmobj, tmstr
	return tmstr

def handle_k5_data(klist, code, trade_date, chk_price, type, tm_array):
	tmstr = '??:??'
	tmobj = ''
	tmend = ''
	mx_prc = 0
	for row in klist:
		if row['day'][:10] != trade_date:
			continue
		#print(row['day'][:10])

		#ZT
		if type==0:
			price = round(float(row['high']), 2)
			if mx_prc<price:
				mx_prc = price
				tmobj = row['day']
				tmend = row['day']
			elif mx_prc==price:
				tmend = row['day']
		#DT
		elif type==1:
			price = round(float(row['low']), 2)
			if mx_prc==0:
				mx_prc = price
				tmobj = row['day']
				tmend = row['day']
			if mx_prc>price:
				mx_prc = price
				tmobj = row['day']
				tmend = row['day']
			elif mx_prc==price:
				tmend = row['day']
		else:
			print ("Error:Unknown type", type)
			break
	binst = 0
	#print mx_prc, chk_price
	if mx_prc!=chk_price:
		binst = 1

	#print tmobj, tmend
	if tmobj!='':
		tmstr = covert_time_fmt(tmobj, 5, binst)
		tm_array[0]=tmstr
	if tmend!='':
		tmstr = covert_time_fmt(tmend, 0, binst)
		tm_array[1]=tmstr
	#print(tmstr)
	return tmstr
		
	'''
	df_today = df.loc[df['date'].str.contains(str(trade_date))]
	if len(df_today)<=0:
		print code, trade_date, "No data"
		#print "Not find data"
		return

	tmobj = ''
	tmend = ''
	mx_prc = 0
	#读出的数据就是float类型
	for index,row in df_today.iterrows():
		close = row['close']
		if type==0:
			price = row['high']
			if mx_prc<price:
				mx_prc = price
				tmobj = row['date']
				tmend = row['date']
			elif mx_prc==price:
				tmend = row['date']
		else:
			price = row['low']
			if mx_prc==0:
				mx_prc = price
				tmobj = row['date']
				tmend = row['date']
			if mx_prc>price:
				mx_prc = price
				tmobj = row['date']
				tmend = row['date']
			elif mx_prc==price:
				tmend = row['date']

	binst = 0
	if mx_prc!=chk_price:
		binst = 1

	if tmobj!='':
		tmstr = covert_time_fmt(tmobj, 5, binst)
		tm_array.append(tmstr)
	if tmend!='':
		tmstr = covert_time_fmt(tmend, 0, binst)
		tm_array.append(tmstr)
	return tmstr
	'''

#获取首次触板ZT or DT的时间
#type  0:ZT  1:DT
def get_zdt_time(code, trade_date, chk_price, type, tm_array):
	'''
	tm_array.append("17:17")
	tm_array.append("18:18")
	return tmstr
	'''

	flag = 0
	today = datetime.date.today()
	#if (today-trade_date).days>0:
	#	flag = 1
	
	flag = 1
	klist = get_kline5_data(code, 120)
	#tmstr = handle_k5_data(klist, code, trade_date, chk_price, type, tm_array)
	try:
		tmstr = handle_k5_data(klist, code, trade_date, chk_price, type, tm_array)
	except:
		print("Error data", code)
		print(klist)
		exit(0)

	'''
	TODO:
	if flag == 0:
		tmstr = handle_today_ticks(df, code, trade_date, chk_price, type)
	else:
		tmstr = handle_kdata(df, code, trade_date, chk_price, type, tm_array)
	#print code, type, tmstr
	'''
	return tmstr

#返回值是ZDT的天数，
#stk_list[0]返回上市交易天数，用于判断是否是次新
#cur_zdt:表示当天是否是ZDT状态
#type:   
#	1:ZT;  2:DT
#TODO：方法不精确，需要改进
def get_zf_days(code, type, trade_date, cur_zdt, stk_list):
	dcMethod=1
	if dcMethod==1:
		#print("TODO: harry UP,SB",code,trade_date)
		count = 0
		yzcount = 0

		pre_date = get_preday(50, trade_date)
		rt,bg=parseDate2(pre_date,'')
		rt,ed=parseDate2(trade_date,'')
		content = get_kline_by_dc(code, bg, ed, 1, 6)
		if content is None:
			stk_list[0] = 0
			return -1
		jsObj=json.loads(content)
		klineObj = jsObj['data']['klines']
		klLen=len(klineObj)
		lastDt=''
		for item in reversed(klineObj):
			#print item
			itemList = item.split(',')
			#获取最新的交易日，和trade_date比较，判断ZDT数量是否需要加1
			if lastDt=='':
				lastDt = itemList[0]
				if lastDt != trade_date:
					print("Not tradedate", code, lastDt,trade_date)
			openp = float(itemList[1])
			close = float(itemList[2])
			high = float(itemList[3])
			low = float(itemList[4])
			val = float(itemList[8])
			bZDT = 0
			if type==1:
				if code[:3] in G_LARGE_FLUC:
					if (val>19.8 and high==close) or (high==low and val>2):
						bZDT = 1
				else:
					if (val>9.8 and high==close) or (high==low and val>2):
						bZDT = 1
						#print val, itemList[0],high,close,low
				if bZDT==1:
					count += 1
					if high==low:
						yzcount += 1
			elif type==2:
				if code[:3] in G_LARGE_FLUC:
					if (val<-19.88 and low==close) or (high==low and val<-2):
						bZDT = -1
				else:
					if (val<-9.88 and low==close) or (high==low and val<-2):
						bZDT = -1
				if bZDT==-1:
					count += 1
					if high==low:
						yzcount += 1
			#碰到某一天不再满足ZDT条件，中断计数
			if bZDT==0:
				break
		#print("%s,%s,count=%d yzct=%d"%(code, lastDt, count, yzcount))
		return count
	rtntype = 1
	jstr = 'fsData1515847425760'
	content = get_zdting_by_dc(code, jstr, rtntype)
	#print "get_zdf_d", code, content
	if content is None:
		stk_list[0] = 0
		return -1

	jslen = len(jstr)
	content = content[(jslen+1):]
	contObj = content.split("\r")

	#如果当天的数据已经得到，不需要多加一天，得到ZT or DT
	#只有正在进行交易的时候，当天数据得不到，ZT or DT需要加1
	count = 0
	yzcount = 0
	dayLen = len(contObj)
	stk_list[0] = dayLen
	while dayLen>0:
		dayCont = contObj[dayLen-1]
		if len(dayCont)<=8:
			dayLen -= 1
			continue
		#print(dayCont)
		itemObj = dayCont.strip().split(',')

		index = itemObj[0]
		close = float(itemObj[2])
		high = float(itemObj[3])
		low = float(itemObj[4])
		#最开始上市那天，以前不再有数据
		if dayLen<=1:
			count += 1
			yzcount += 1
			if yzcount!=0:
				count -= yzcount
			break
		preDayCont = contObj[dayLen-2]
		preItemObj = preDayCont.strip().split(',')
		preClose = float(preItemObj[2])

		val = round((close-preClose)*100/preClose, 2)
		bflag = 0
		if str(index)==str(trade_date):
			if cur_zdt==1:
				count += 1
			dayLen -= 1
			continue
		#print index, trade_date, type, val
		bZDT = 0
		if type==1:
			if code[:3] in G_LARGE_FLUC:
				if (val>19.8 and high==close) or (high==low and val>2):
					bZDT = 1
			else:
				if (val>9.8 and high==close) or (high==low and val>2):
					bZDT = 1
			if bZDT==1:
				count += 1
				if high==low:
					yzcount += 1
				bflag = 1
		elif type==2:
			if code[:3] in G_LARGE_FLUC:
				if (val<-19.88 and low==close) or (high==low and val<-2):
					bZDT = 1
			else:
				if (val<-9.88 and low==close) or (high==low and val<-2):
					bZDT = 1
			if bZDT==1:
				count += 1
				if high==low:
					yzcount += 1
				bflag = 1
		if bflag==0:
			break
		dayLen -= 1
	return count

#返回值是ZDT的天数，stk_list[0]表示上市交易的天数，判断是否是次新
def check_pre_day_state(code, trade_date):
	rtntype = 1
	if 1:
		pre_date = get_preday(50, trade_date)
		rt,bg=parseDate2(pre_date,'')
		rt,ed=parseDate2(trade_date,'')
		content = get_kline_by_dc(code, bg, ed, 1, 6)
		if content is None:
			print("No content")
			return 'ERROR'
		#print(content)
		jsObj=json.loads(content)
		name = jsObj['data']['name']
		if name[:2]==u'退市':
			print("TuiShi?")
			item[1] = name[2:]
		elif name[-1:]==u'退':
			print("TuiShi?")
			item[1] = name[:-1]
		klineObj = jsObj['data']['klines']
		klLen=len(klineObj)
		lastDt=''
		desc = ''
		#仅仅判断前一天的ZDT情况
		for item in reversed(klineObj):
			#print item
			itemList = item.split(',')
			#获取最新的交易日，和trade_date比较，判断ZDT数量是否需要加1
			if lastDt=='':
				lastDt = itemList[0]
				if lastDt != trade_date:
					print("Not tradedate", code, lastDt,trade_date)
			openp = float(itemList[1])
			close = float(itemList[2])
			high = float(itemList[3])
			low = float(itemList[4])
			val = float(itemList[8])
			bZDT = 0
			if code[:3] in G_LARGE_FLUC:
				if (val>19.8 and high==close):
					if (high==low and val>2):
						desc = 'YZZT'
					else:
						desc = 'ZT'
				elif (val<-19.8 and low==close):
					if (high==low and val<-2):
						desc = 'YZDT'
					else:
						desc = 'DT'
			else:
				if (val>9.8 and high==close):
					if (high==low and val>2):
						desc = 'YZZT'
					else:
						desc = 'ZT'
				elif (val<-9.8 and low==close):
					if (high==low and val<-2):
						desc = 'YZDT'
					else:
						desc = 'DT'
		return desc
	jstr = 'fsData1515847425760'
	content = get_zdting_by_dc(code, jstr, rtntype)
	if content is None:
		return 'ERROR'

	jslen = len(jstr)
	content = content[(jslen+1):]
	if len(content) < 30:
		print "Warning, TuiShi?", code, trade_date
		return 'TUISHI'

	#print code, content
	contObj = content.split("\n")
	dayLen = len(contObj)
	#print contObj[dayLen-1][:10]
	#print contObj[dayLen-2][:10]
	
	last_dt = contObj[dayLen-1][:10].strip()
	lastDate = datetime.datetime.strptime(last_dt, '%Y-%m-%d').date()
	trdDate = datetime.datetime.strptime(trade_date, '%Y-%m-%d').date()
	preDayItem = ''
	pre2DayItem = ''
	if (trdDate-lastDate).days>0:
		#trade_data的数据还没有，意味着这天还正在交易中
		preDayItem = contObj[dayLen-1]
		pre2DayItem = contObj[dayLen-2]
		#print "nnn", preDayItem, pre2DayItem
	else:
		while dayLen>0:
			dayCont = contObj[dayLen-1]
			if len(dayCont)<=8:
				dayLen -= 1
				continue
			#print(dayCont)
			cur_dt = dayCont[:10].strip()
			if cur_dt == trade_date:
				#print "cccc",cur_dt
				preDayItem = contObj[dayLen-2]
				pre2DayItem = contObj[dayLen-3]
				break
			dayLen -= 1
		#print "yyy", preDayItem, pre2DayItem
	#end if-else
	
	if preDayItem=='':
		print "Not find pre day info"
		return 'ERROR'

	itemObj = preDayItem.strip().split(',')

	#前一天的信息
	preDayDt = itemObj[0]
	close = float(itemObj[2])
	high = float(itemObj[3])
	low = float(itemObj[4])

	#获取前两天的信息，计算后一天的ZDT价格
	preItemObj = pre2DayItem.strip().split(',')
	preClose = float(preItemObj[2])
	
	zt_price1 = preClose * 1.1
	dt_price1 = preClose * 0.9
	zt_price = spc_round2(zt_price1,2)
	dt_price = spc_round2(dt_price1,2)

	desc = ''
	if close == zt_price:
		if high==low:
			desc="YZZT"
		else:
			desc = "ZT"
	elif close==dt_price:
		if high==low:
			desc = "YZDT"
		else:
			desc = "DT"
	return desc

if __name__=="__main__":
	stk_list=[0, 0]
	trade_date='2022-12-09'
	get_zf_days('600185', 1, trade_date, 1, stk_list)
	tm_array=['','']
	#get_zdt_time('600095', '2020-08-20', 20.13, 0, tm_array)
	#check_pre_day_state('600158', '2019-06-27')
	#print "TM Array", tm_array[0],tm_array[1]
	rtntype = 1
	jstr = 'fsData1515847425760'
	pre_date = get_preday(90, trade_date)
	rt,bg=parseDate2(pre_date,'')
	rt,ed=parseDate2(trade_date,'')
	#content = get_kline_by_dc('000520', bg, ed,1,6)
	#print content
	
