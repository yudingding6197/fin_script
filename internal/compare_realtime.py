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
		zt_dict[i[0]] = [i[1], i[7], 'YZZT', '']
		#print "lst_non_yzcx_yzzt", i[0], i[1], i
	for i in stcsItem.lst_non_yzcx_zt:
		zt_dict[i[0]] = [i[1], i[7], ' ZT ', '']
		#print "lst_non_yzcx_zt", i[0], i[1], i

def get_dt_data(stcsItem, dt_dict):
	for i in stcsItem.lst_yzdt:
		dt_dict[i[0]] = [i[1], i[7], 'YZDT', '']
		#print "lst_non_yzdt", i[0], i[1]
	for i in stcsItem.lst_dt:
		dt_dict[i[0]] = [i[1], i[7], ' DT ', '']
		#print "lst_non_dt", i[0], i[1]

def compare_qiangruo(todayItem, ysdayItem, q_dict, r_dict, flag=''):
	y_zt_dict = {}
	y_dt_dict = {}
	t_zt_dict = {}
	t_dt_dict = {}
	
	get_zt_data(ysdayItem, y_zt_dict)
	get_dt_data(todayItem, t_dt_dict)
	#print json.dumps(y_zt_dict, ensure_ascii=False)
	#print ""
	#print json.dumps(t_dt_dict, ensure_ascii=False)

	#print("===== today ZT, ytoday DT=====")
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
				r_dict[i][2] = y_zt_dict[i][2] + '-' + t_dt_dict[i][2]
				#print("ZRZT, JRDT RRRRR", i, r_dict[i])
	#还有开板的CX
	#r_dict[i] = 
	
	#print(r_dict)
	for i in t_zt_dict.keys():
		#print("code:", i)
		if i in y_dt_dict.iterkeys():
			if flag=='' or flag=='Q':
				q_dict[i] = y_dt_dict[i]
				q_dict[i][2] = y_dt_dict[i][2] + '-' + t_zt_dict[i][2]
				#print("ZRDT, JRZT QQQQQ", i)
	#print(q_dict)
	
	
#Main
if __name__=='__main__':
	pass
