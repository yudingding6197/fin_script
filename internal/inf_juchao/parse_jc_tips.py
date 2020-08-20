#!/usr/bin/env python
# -*- coding:gbk -*-

#����ÿ�յĽ�����Ϣ
import sys
import re
import os
import datetime
import json
import getopt
from collections import OrderedDict

#from internal.handle_realtime import *
from internal.global_var import g_shcd
from internal.global_var import g_szcd

JUCHAO_PRE_FD = "../data/entry/juchao/"

#��ȡͣ���ơ��ֺ졢�¹�
def read_tfp_fh_in_tips(dt, jc_dict):
	year = dt[:4]
	jcLoc = JUCHAO_PRE_FD + year + '/jc' + dt + ".txt"
	jcFile = open(jcLoc, 'r')
	jcJson = json.load(jcFile)
	jcFile.close()

	headlist = g_shcd + g_szcd
	jc_dict['fupai'] = []
	jc_dict['tingpai'] = []
	jc_dict['newmrk'] = []
	jc_dict['fenhong'] = []
	for item in jcJson:
		#print item['tradingTipsName']
		if item['tradingTipsName'] == u'ͣ����':
			list = []
			for dict in item['tbTrade0112s']:
				code = dict['obSeccode0110']
				#print dict['obSeccode0110'], dict['obSecname0110']
				if code[:3] in headlist:
					list.append(dict['obSeccode0110'])
			jc_dict['tingpai'] = list
			#print list
		elif item['tradingTipsName']==u'������':
			list = []
			#print item['tradingTipsName']
			for dict in item['tbTrade0112s']:
				code = dict['obSeccode0110']
				#print dict['obSeccode0110'], dict['obSecname0110']
				if code[:3] in headlist:
					list.append(dict['obSeccode0110'])
			jc_dict['fupai'] = list
			#print dict['fupai']
		elif item['tradingTipsName']==u'�׷��¹�������':
			list = []
			#print item['tradingTipsName']
			for dict in item['tbTrade0112s']:
				code = dict['obSeccode0110']
				#print dict['obSeccode0110'], dict['obSecname0110']
				if code[:3] in headlist:
					list.append(dict['obSeccode0110'])
			jc_dict['newmrk'] = list
			#print dict['fupai']
		elif item['tradingTipsName']==u'�ֺ�ת����Ȩ��Ϣ��':
			list = jc_dict['fenhong']
			#print item['tradingTipsName']
			for dict in item['tbTrade0112s']:
				code = dict['obSeccode0110']
				#print dict['obSeccode0110'], dict['obSecname0110']
				if code[:3] not in headlist:
					continue
				if code not in list:
					list.append(code)
			jc_dict['fenhong'] = list
		elif item['tradingTipsName']==u'�ֺ�ת������������':
			list = jc_dict['fenhong']
			#print item['tradingTipsName']
			for dict in item['tbTrade0112s']:
				code = dict['obSeccode0110']
				#print dict['obSeccode0110'], dict['obSecname0110']
				if code[:3] not in headlist:
					continue
				if code not in list:
					list.append(code)
			jc_dict['fenhong'] = list
		'''
		'''
	#print jc_dict

#��ȡ������ӻ���ȡ��ST������Ϣ
def read_st_in_daily_tips(dt, stk_list, stk_dict):
	year = dt[:4]
	jcLoc = JUCHAO_PRE_FD + year + "/jc" + dt + ".txt"
	file = open(jcLoc, 'r')
	dobj = json.load(file)
	if isinstance(dobj, list) is False:
		print ("Error, not expected list object")
		return -1
	file.close()

	for item in dobj:
		#print item['tradingTipsName']
		if item['tradingTipsName']==u'ȡ��*������':
			#print item['tradingTipsName']
			for dict in item['tbTrade0112s']:
				code = dict['obSeccode0110']
				if code not in stk_list:
					stk_list.append(code)
					dlist = ["Rem", 1, dict['obSecname0110']]
					stk_dict[code] = OrderedDict()
					stk_dict[code][dt] = dlist
				else:
					if dt not in stk_dict[code].iterkeys():
						dlist = ["Rem", 1, dict['obSecname0110']]
						stk_dict[code][dt] = dlist
					else:
						dlist = ["Rem", 3, dict['obSecname0110']]
						stk_dict[code][dt] = dlist
				#print dict['obSeccode0110'], dict['obSecname0110']
			#print ""
		elif item['tradingTipsName']==u'�����ر�����':
			#print item['tradingTipsName']
			for dict in item['tbTrade0112s']:
				code = dict['obSeccode0110']
				if code not in stk_list:
					stk_list.append(code)
					dlist = ["Rem", 2, dict['obSecname0110']]
					stk_dict[code] = OrderedDict()
					stk_dict[code][dt] = dlist
				else:
					if dt not in stk_dict[code].iterkeys():
						dlist = ["Rem", 2, dict['obSecname0110']]
						stk_dict[code][dt] = dlist
					else:
						dlist = ["Rem", 3, dict['obSecname0110']]
						stk_dict[code][dt] = dlist
			#print ""
		elif item['tradingTipsName']==u'ʵ�����з��վ�ʾ��':
			#print item['tradingTipsName']
			for dict in item['tbTrade0112s']:
				code = dict['obSeccode0110']
				if code not in stk_list:
					stk_list.append(code)
					dlist = ["Add", 1, dict['obSecname0110']]
					stk_dict[code] = OrderedDict()
					stk_dict[code][dt] = dlist
				else:
					if dt not in stk_dict[code].iterkeys():
						dlist = ["Add", 1, dict['obSecname0110']]
						stk_dict[code][dt] = dlist
					else:
						dlist = ["Add", 3, dict['obSecname0110']]
						stk_dict[code][dt] = dlist
				#print dict['obSeccode0110'], dict['obSecname0110']								
			#print ""
		elif item['tradingTipsName']==u'ʵ���ر�����':
			#print item['tradingTipsName']
			for dict in item['tbTrade0112s']:
				code = dict['obSeccode0110']
				if code not in stk_list:
					stk_list.append(code)
					dlist = ["Add", 2, dict['obSecname0110']]
					stk_dict[code] = OrderedDict()
					stk_dict[code][dt] = dlist
				else:
					if dt not in stk_dict[code].iterkeys():
						dlist = ["Add", 2, dict['obSecname0110']]
						stk_dict[code][dt] = dlist
					else:
						dlist = ["Add", 3, dict['obSecname0110']]
						stk_dict[code][dt] = dlist
				#print dict['obSeccode0110'], dict['obSecname0110']								
			#print ""
		elif item['tradingTipsName']==u'���������ڿ�ʼ��':
			#print item['tradingTipsName']
			for dict in item['tbTrade0112s']:
				code = dict['obSeccode0110']
				#print "tus tips", code, dict['obSecname0110']
				if code not in stk_list:
					stk_list.append(code)
					dlist = ["TuS", 2, dict['obSecname0110']]
					stk_dict[code] = OrderedDict()
					stk_dict[code][dt] = dlist
				else:
					if dt not in stk_dict[code].iterkeys():
						dlist = ["TuS", 2, dict['obSecname0110']]
						stk_dict[code][dt] = dlist
					else:
						dlist = ["TuS", 3, dict['obSecname0110']]
						stk_dict[code][dt] = dlist
				#print dict['obSeccode0110'], dict['obSecname0110']								
			#print ""
	#if len(AddST)>0 or len(RemST)>0:
	#	print jcLoc
	return 0

#Main Start:
if __name__=='__main__':
	beginTm = datetime.datetime.now()
	
	handle_argument()
	
	