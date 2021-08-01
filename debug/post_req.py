#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import re
import os
import string
import urllib
import urllib2
import datetime
import json

#urlall = "http://www.cninfo.com.cn/cninfo-new/memo-2"
#urlall = "http://www.cninfo.com.cn/information/companyinfo_n.html?fulltext?szmb000615"
#urlall = "http://www.cninfo.com.cn/cninfo-new/disclosure/szse/fulltext"
urlall=""
filename = 'debug/_html.txt'

def func1():
	urlall="http://www.cninfo.com.cn/new/information/getSuspensionResumptions?queryDate=2020-06-12"
	#dict = {'stock':'300418','searchkey':'','category':'','pageNum':'1','pageSize':'15','column':'szse_gem','tabName':'latest','sortName':'','sortType':'','limit':'','seDate':''}
	dict = {}
	data = urllib.urlencode(dict)
	#print dict
	#dict['stock']='600060'
	#print dict['aaa']
	#for k,v in dict.items():
	#	print k,v
	#exit(0)

	tf_fl = open(filename, 'w+')
	try:
		#req : urllib2.Request(urlall)
		res_data = urllib2.urlopen(urlall, data)
	except:
		print "Error fupai urlopen"
		#LOOP_COUNT = LOOP_COUNT+1
	if res_data is None:
		print "Open URL fail"
		exit(0)

	content = res_data.read()
	tf_fl.write(content)
	tf_fl.close()

#获取指定时间段的所有公告
# seDate ：指定时间段
# searchkey  指定关键字
def func2(searchkey):
	urlall = "http://www.cninfo.com.cn/new/hisAnnouncement/query"
	#pageNum=1&pageSize=1000&column=szse&tabName=fulltext&plate=&stock=&
	#	searchkey=%E5%81%9C%E7%89%8C%E6%A0%B8%E6%9F%A5&secid=&category=&trade=&seDate=2018-01-01~2020-12-31&
	#	sortName=&sortType=&isHLtitle=true
	dictObj = {'pageNum':1,'pageSize':1000,'column':'szse','tabName':'fulltext','plate':'','stock':'',
		'secid':'','category':'','trade':'',
		'sortName':'','sortType':'','isHLtitle':'true'}
	dictObj['searchkey'] = searchkey
	dictObj['seDate'] = '2021-01-28~2021-07-30'
	data = urllib.urlencode(dictObj)
	#print dictObj
	tf_fl = open(filename, 'w+')
	try:
		#req : urllib2.Request(urlall)
		res_data = urllib2.urlopen(urlall, data)
	except:
		print "Error fupai urlopen"
		#LOOP_COUNT = LOOP_COUNT+1
	if res_data is None:
		print "Open URL fail"
		exit(0)

	content = res_data.read()
	#print content
	tf_fl.write(content)
	tf_fl.close()
	
if __name__=="__main__":
	func2("停牌核查")

'''
s = json.loads(content)
clsAnno = s['classifiedAnnouncements']
annoLen = len(clsAnno)
if annoLen==0:
	print "classifiedAnnouncements No Data"
	exit(0)
items = clsAnno[0]
count = 0
for item in items:
	#print type(item)
	#print item
	for k,v in item.items():
		print k,v
	break
#print clsAnno[0][0]
#print type(clsAnno[0][0])
'''

'''
line = res_data.readline()
while line:
	try:
		tf_fl.write(line)
	except:
		#print "?????????????",line.decode('utf8')
		tf_fl.write(line)
	line = res_data.readline()
'''

