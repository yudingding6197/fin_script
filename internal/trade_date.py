#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
from internal.url_sina.fetch_sina import *

DB_PATH = 'internal/db'
filenm = 'sh000001'

def get_preday(days=1, cur_day=''):
	pre_day = ''
	if cur_day=='':
		cur_day = get_lastday()

	location = DB_PATH + '/' + filenm + '.csv'
	fl = open(location, 'r')
	#排除第一行
	line = fl.readline()
	line = fl.readline()
	count = 0
	flag = 0
	while line:
		file_day = line.split(',')[0]
		if file_day==cur_day:
			flag = 1
			line = fl.readline()
			continue
		if flag==0:
			continue
		if count+1==days:
			pre_day = file_day	
			break
		count += 1
		line = fl.readline()

	return pre_day

def get_lastday(src='sina'):
	value = ''
	if src=='sina':
		value = get_sina_lastday()
	elif src=='163':
		value = get_163_lastday()
	elif src=='qq':
		value = get_qq_lastday()
	#print(value)
	return value

#Main
#for i in range(0,1000):
#	formatRand()
if __name__ == "__main__":
	pass
