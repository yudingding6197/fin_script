#!/usr/bin/env python
# -*- coding:utf8 -*-
import os
import urllib2,time

from internal.url_163.service_163 import *

DB_PATH = './internal/db'

def update_latest_trade(latest_day):
	if latest_day=='':
		print "Invalid day", latest_day
		return -1
	#print(latest_day)
	
	filenm = 'sh000001'
	if not os.path.exists(DB_PATH):
		os.mikedirs(DB_PATH)
		return get_index_history_byNetease(filenm)
		

	location = DB_PATH + '/' + filenm + '.csv'
	if not os.path.isfile(location):
		return get_index_history_byNetease(filenm)
				

	fl = open(location, 'r')
	line = fl.readline()
	line = fl.readline()
	file_day = line.split(',')[0]
	#print("_____ upd_trd", file_day,latest_day)

	if latest_day != file_day:
		return get_index_history_byNetease(filenm)
	#else:
	#	print("Already the latest")
	return 0
		
'''
if __name__=='__main__':
	latest_day = get_lastday()
	print(latest_day)
	
	filenm = 'sh000001'
	if not os.path.exists(DB_PATH):
		os.mikedirs(DB_PATH)
		get_index_history_byNetease(filenm)
		exit()

	location = DB_PATH + '/' + filenm + '.csv'
	fl = open(location, 'r')
	lines = fl.readlines(5)
	file_day = lines[1].split(',')[0]
	print(file_day)
	
	if latest_day != file_day:
		get_index_history_byNetease(filenm)
'''
