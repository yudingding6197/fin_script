#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import time
import string
import datetime

yzzt_list = ['603345','603238','000520','300613','300608','300553','603615']
add_list = ['002815','300291']

if __name__=="__main__":
	#ͨ��extend����׷�ӣ�����ʹ��append
	yzzt_list.extend(add_list)

	list = yzzt_list
	print '\n�����б���2��'
	# ����2
	for i in range(len(list)):
		print ("��ţ�%s   ֵ��%s" % (i + 1, list[i]))

	# ����3
	print '\n�����б���3��'
	for i, val in enumerate(list):
		print ("��ţ�%s   ֵ��%s" % (i + 1, val))

	# ����3
	print '\n�����б���3 �����ñ�����ʼ��ʼλ�ã�ֻ�ı�����ʼ��ţ���'
	for i, val in enumerate(list, 2):
		print ("��ţ�%s   ֵ��%s" % (i + 1, val))

	lists = [[]] * 3
	print lists
	lists[0].append(3)
	print lists
	# 3�������ֵͬʱ���� [[3], [3], [3]]

	lists = [[] for i in range(3)]
	lists[0].append(3)
	print lists
	lists[1].append(7)
	print lists
	
	#��ά���鴴����ʽ�޸�Ϊ
	myList = [([0] * 3) for i in range(4)]
	print myList
	