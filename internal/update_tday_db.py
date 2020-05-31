#!/usr/bin/env python
# -*- coding:utf8 -*-
import os
import urllib2,time
from internal.trade_date import *

DB_PATH = './internal/db'

def get_page(url):  #获取页面数据
	req=urllib2.Request(url,headers={
		'Connection': 'Keep-Alive',
		'Accept': 'text/html, application/xhtml+xml, */*',
		'Accept-Language':'zh-CN,zh;q=0.8',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
	})
	opener=urllib2.urlopen(req)
	page=opener.read()
	return page

def get_index_history_byNetease(index_temp):
	"""
	:param index_temp: for example, 'sh000001' 上证指数
	:return:
	"""
	index_type=index_temp[0:2]
	index_id=index_temp[2:]
	if index_type=='sh':
		index_id='0'+index_id
	if index_type=="sz":
		index_id='1'+index_id
	#url='http://quotes.money.163.com/service/chddata.html?code=%s&start=19900101&
	#end=%s&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER'%(index_id,time.strftime("%Y%m%d"))
	url='http://quotes.money.163.com/service/chddata.html?code=%s'%(index_id)
	#print(url)

	page=get_page(url)#.decode('gb2312')
	with open("./internal/db/"+index_temp+".csv", "wb") as code:     
		code.write(page)
	#page.to_csv('_a.csv')

def update_latest_trade(latest_day=''):
	if latest_day=='':
		latest_day = get_lastday()
	#print(latest_day)
	
	filenm = 'sh000001'
	if not os.path.exists(DB_PATH):
		os.mikedirs(DB_PATH)
		get_index_history_byNetease(filenm)
		return

	location = DB_PATH + '/' + filenm + '.csv'
	if not os.path.isfile(location):
		get_index_history_byNetease(filenm)
		return		

	fl = open(location, 'r')
	lines = fl.readlines(5)
	file_day = lines[1].split(',')[0]
	#print(file_day)

	if latest_day != file_day:
		get_index_history_byNetease(filenm)
	#else:
	#	print("Already the latest")
	return
		
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
