#!/usr/bin/env python
# -*- coding: gbk -*-
import sys
import os
from internal.tingfupai import * 
from internal.url_juchao.tips_res import *
from internal.url_dfcf.dc_hq_push import *
from internal.trade_date import *

def fetch_kday_page1(url):  #获取页面数据
	req=urllib2.Request(url,headers={
		'Connection': 'Keep-Alive',
		'Accept': 'text/html, application/xhtml+xml, */*',
		'Accept-Language':'zh-CN,zh;q=0.8',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
	})
	LOOP_COUNT = 0
	opener = None
	while LOOP_COUNT<3:
		try:
			opener=urllib2.urlopen(req)
		except:
			LOOP_COUNT += 1
			time.sleep(1)
		else:
			break
	if opener is None:
		return ''
	
	content = opener.read()
	respInfo = opener.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
		#print "Content compressed"
		content = zlib.decompress(content, 16+zlib.MAX_WBITS);
	return content


def get_index_history_byNetease_js1(location, index_temp):
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
	#url='http://img1.money.126.net/data/hs/kline/day/times/%s.json'%(index_id)
	url = 'http://quotes.money.163.com/service/chddata.html?code=0000001'
	#print('netease js', url)

	page=fetch_kday_page1(url)
	#print page[:300]
	#print "pp", type(page)
	if page=='':
		return -1

	#print page
	#json.dumps(page.encode('gbk'))
	obj = re.split('\r\n', page)
	print len(obj)
	dtObj = []
	for i in range(1, len(obj)):
		#print obj[i][:10]
		if obj[i][-5:]!=',None':
			print obj[i]
		else:
			dtObj.append(obj[i][:10])
	file = open('_test.json','w')
	json.dump(dtObj, file)
	file.close()
	#print obj[0]
	#print obj[1]
	#print obj[2]
	
	file = open('_test.json','r')
	info = json.load(file)
	file.close()
	
	print type(info)
	print info[0]
	print info[-1]
	
	#with open("./internal/db/"+index_temp+"_json.txt", "wb") as code:     
	#	code.write(page)
	#page.to_csv('_a.csv')
	return 0


#Main Start:
if __name__=='__main__':
	#pre_day = read_preday_json(days, cur_day)
	dt= get_preday(0)
	print dt;
	exit(0)
	location = '_cur_json.txt'
	index_temp = 'sh000001'
	get_index_history_byNetease_js1(location, index_temp)
	
	