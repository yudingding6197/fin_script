#!/usr/bin/env python
# -*- coding:utf8 -*-
import json
import zlib
import random
import urllib2
from collections import OrderedDict

#交易所的url

sz_urlAddr = 'http://www.szse.cn/api/report/ShowReport/data'
sz_urlfmt = '%s?SHOWTYPE=JSON&CATALOGID=1803_sczm&TABKEY=tab1&txtQueryDate=%s&random=%.16f'
send_headers = {
'Host': 'www.szse.cn',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': 1,
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
'DNT': 1,
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9'
}

def query_szse_daily_stats(query_date, type='string'):
	r1 = random.random()
	urlall = sz_urlfmt %(sz_urlAddr, query_date, r1) 
	#print urlall

	#list = json.loads(content)
	#print json.dumps(list[0]['data'], ensure_ascii=False)

	#filename = 'debug/_html.txt'
	#tf_fl = open(filename, 'w+')

	res_data = None
	LOOP_COUNT = 0
	while LOOP_COUNT<3:
		try:
			req = urllib2.Request(urlall,headers=send_headers)
			res_data = urllib2.urlopen(req, timeout=1)
		except Exception as e:
			if LOOP_COUNT==2:
				print "Error: urlopen", e
				exit(0)
			LOOP_COUNT = LOOP_COUNT+1
		else:
			break
		
	#print res_data
	if res_data is None:
		return None

	content = res_data.read()
	respInfo = res_data.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
		content = zlib.decompress(content, 16+zlib.MAX_WBITS);
	#print content.decode('utf8')

	#tf_fl.write(content)
	if type=='string':
		return content
	elif type=='json':
		listObj = json.loads(content,object_pairs_hook=OrderedDict)
		return listObj
	else:
		print("Error: unknown type", type)
	return None

sh_urlAddr = 'http://query.sse.com.cn/commonQuery.do'
sh_urlfmt = '%s?jsonCallBack=%s&searchDate=%s&sqlId=COMMON_SSE_SJ_GPSJ_CJGK_DAYCJGK_C&stockType=90&_=%s'
sh_send_headers = {
'Host': 'query.sse.com.cn',
'Connection': 'keep-alive',
'Referer': 'http://www.sse.com.cn/market/stockdata/overview/day/',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9'
}
#'DNT': 1,

def query_shse_daily_stats(query_date, type='string'):
	r1 = random.random()
	r2 = random.random()
	sf1 = "%.13f" % r1
	sf2 = "%.5f" % r2
	jsonFmt = "jsonpCallback%s"
	jsonCb = jsonFmt % (sf2[2:])
	urlall = sh_urlfmt %(sh_urlAddr, jsonCb, query_date, sf1[2:])
	#print urlall

	#list = json.loads(content)
	#print json.dumps(list[0]['data'], ensure_ascii=False)

	#filename = 'debug/_html.txt'
	#tf_fl = open(filename, 'w+')

	res_data = None
	LOOP_COUNT = 0
	while LOOP_COUNT<3:
		try:
			req = urllib2.Request(urlall,headers=sh_send_headers)
			res_data = urllib2.urlopen(req, timeout=1)
		except Exception as e:
			if LOOP_COUNT==2:
				print "Error: urlopen", e
				exit(0)
			LOOP_COUNT = LOOP_COUNT+1
		else:
			break
	#jsonpCallback70871	
	#print res_data
	if res_data is None:
		return None

	content = res_data.read()
	respInfo = res_data.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
		content = zlib.decompress(content, 16+zlib.MAX_WBITS);
	content = content.strip()
	
	content = content[len(jsonCb)+1:-1]
	errIdx = content.find("'error_en'")
	if errIdx != -1:
		print "Error: invalid content"
		print content.decode('utf8')
		return None
	#print content.decode('utf8')
	#print content

	if type=='string':
		return content
	elif type=='json':
		listObj = json.loads(content,object_pairs_hook=OrderedDict)
		return listObj
	else:
		print("Error: unknown type", type)
	return None
