#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import os
import re
import datetime
import urllib2
import json
import zlib

urlall = ""
send_headers = {
 'Host':'nufm.dfcfw.com',
 'User-Agent':'User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
 'Accept':'*/*',
 'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
 'DNT':'1',
 'Connection':'keep-alive'
}

def get_stk_push_max_page(curpage, st='A', sr=-1, ps=80):
	link = "http://11.push2.eastmoney.com/api/qt/clist/get?"
	key1 = "cb=%s&pn=%d&pz=%d&po=%d&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=%s&_=1605696197667"
	urlfmt = link + key1
	jq = 'jQuery112402337896881202678_1605696197666'
	fileds = 'f1,f2,f3'
	send_headers = {
	'Host': '11.push2.eastmoney.com',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'DNT': 1,
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.8'
	}
	LOOP_COUNT = 0
	response = None
	url = urlfmt % (jq, ps, 1, 1, fileds)
	#print(url)
	while LOOP_COUNT<3:
		try:
			req = urllib2.Request(url, headers=send_headers)
			response = urllib2.urlopen(req, timeout=5)
		except:
			LOOP_COUNT += 1
			#print("URL request timeout ", url)
		else:
			break
	if response is None:
		print "Please check data from DongCai at", curpage
		return -1

	content = response.read()
	respInfo = response.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
		#print "Content compressed"
		line = zlib.decompress(content, 16+zlib.MAX_WBITS);
	else:
		line = content

	#line = line.decode('utf8')
	#print line
	
	obj = re.match(r'(.*)\{"total":(\d+),(.*)', line)
	if obj is None:
		print "11Not find matched content at", curpage
		return -1

	totalNumber = int(obj.group(2))
	totalpage = totalNumber/ps
	if totalNumber%ps!=0:
		totalpage += 1

	return totalpage

'''
pn: 页数
pz: 
po: 
np: 序号是否存在
fltt=2&invt=2:小数点处理
'''
def get_each_page_push_data1(new_st_list, curpage, st='A', sr=-1, ps=80):
	link = "http://push2.eastmoney.com/api/qt/clist/get?"
	key1 = "cb=%s&pn=%d&pz=%d&po=%d&np=%d&fltt=2&invt=2&fid=%s&fs=%s&fields=%s&_=1605696197667"
	urlfmt = link + key1
	
	jq = 'jQuery11240233789688120261_1605696197666'
	fid = 'f12'
	field1 = 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20'
	field2 = 'f21,f23,f24,f25,f26,f22,f11,f62'
	fields = field1 + ',' + field2
	fs = 'm:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23'
	pn = curpage
	pz = ps

	send_headers = {
	'Host': 'push2.eastmoney.com',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'DNT': 1,
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.8'
	}
	LOOP_COUNT = 0
	response = None
	url = urlfmt % (jq, pn, pz, 0, 1, fid, fs, fields)
	#自定义条件，进行打印调试
	debug = (curpage==1)
	#if debug==1:
	#	print(url)

	while LOOP_COUNT<3:
		try:
			req = urllib2.Request(url, headers=send_headers)
			response = urllib2.urlopen(req, timeout=5)
		except:
			LOOP_COUNT += 1
			#print("URL request timeout ", url)
		else:
			break
	if response is None:
		print "Please check data from DongCai at", curpage
		return -1

	content = response.read()
	respInfo = response.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
		#print "Content compressed"
		line = zlib.decompress(content, 16+zlib.MAX_WBITS);
	else:
		line = content

	dictStr = line[len(jq)+1:-2]
	#if debug==1:
	#	print dictStr

	try:
		dic = json.loads(dictStr)
	except Exception as e:
		print "Invalid data in page", curpage
		return -1

	if dic['data'] is None:
		return 0

	#line = line.decode('utf8')
	#if debug==1:
	#	print dic['data']['diff'][1]

	'''
	0:?
	1:code
	2:name
	'''
	diffObj = dic['data']['diff']
	for item in diffObj:
		props = [''] * 26
		#code = props[1]
		#pre_close = props[9]
		rt_price = item['f2']
		market_dt = item['f26']

		#print(line)
		#还未上市
		if market_dt=='-':
			continue
		#上市停牌
		if rt_price=='-':
			continue
		#line = array[i][2:]
		#new_st_list.append(line.encode('gbk'))
		props[0] = '?'
		props[1] = item['f12']
		props[2] = item['f14']
		props[3] = item['f2']
		props[8] = item['f5']
		props[9] = item['f18']
		props[10] = item['f17']
		props[11] = item['f15']
		props[12] = item['f16']
		market_dt = "%d" % (item['f26'])
		props[25] = market_dt[:4] + '-' + market_dt[4:6] + '-' + market_dt[6:]

		#if debug:
		#	print props[1], props[25], type(item['f26'])
		
		#TODO: debug, can remove it
		#if i==11:
		#	if array[i]=='-':
		#		print rank
		#TODO: END
		
		new_st_list.append(props)
	return 1
