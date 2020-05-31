#!/usr/bin/env python
# -*- coding:utf8 -*-
import os
import urllib2,time
import datetime
from internal.realtime_obj import *
from internal.trade_date import *

'''
lst_non_yzcx_yzzt		lst_non_yzcx_zt		lst_non_yzcx_zthl
lst_yzdt				lst_dt				lst_dtft
'''

def get_zt_data(stcsItem, zt_dict):
	for i in stcsItem.lst_non_yzcx_yzzt:
		zt_dict[i[0]] = [i[1], 'YZZT']
	for i in stcsItem.lst_non_yzcx_zt:
		zt_dict[i[0]] = [i[1], ' ZT ']

def get_dt_data(stcsItem, dt_dict):
	for i in stcsItem.lst_yzdt:
		dt_dict[i[0]] = [i[1], 'YZDT']
	for i in stcsItem.lst_dt:
		dt_dict[i[0]] = [i[1], ' DT ']

def compare_rt(todayItem, ysdayItem, q_dict, r_dict, flag=''):
	y_zt_dict = {}
	y_dt_dict = {}
	t_zt_dict = {}
	t_dt_dict = {}
	
	get_zt_data(ysdayItem, y_zt_dict)
	get_dt_data(todayItem, t_dt_dict)

	get_zt_data(todayItem, t_zt_dict)
	get_dt_data(ysdayItem, y_dt_dict)
	
	#print(todayItem.s_date)
	#for k in t_zt_dict.keys(): print k
	#print("=====DT\n")
	#for k in y_dt_dict.keys(): print k
	#for k in t_dt_dict.keys(): print k
	
	for i in t_dt_dict.keys():
		#print("code:", i)
		if i in y_zt_dict.iterkeys():
			if flag=='' or flag=='R':
				r_dict[i] = y_zt_dict[i]
				#print("ZRZT, JRDT RRRRR", i)
	#print(r_dict)
	for i in t_zt_dict.keys():
		#print("code:", i)
		if i in y_dt_dict.iterkeys():
			if flag=='' or flag=='Q':
				q_dict[i] = y_dt_dict[i]
				#print("ZRDT, JRZT QQQQQ", i)
	#print(q_dict)
	
	
#Main
if __name__=='__main__':
	pass
