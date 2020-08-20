#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import json
import re
import time
import zlib
import urllib2
from bs4 import BeautifulSoup
from bs4 import element

#对数据解析
def parse_price_list(priceListPage, price_dict):
	#soup = BeautifulSoup(content, 'lxml', from_encoding='utf8')
	soup = BeautifulSoup(priceListPage, 'lxml')
	#print(soup.prettify())
	for item in soup.table.children:
		if type(item)!=element.Tag:
			continue
		if item.name!='tr':
			continue;
		index=0
		for tdObj in item.children:
			if type(tdObj)==element.NavigableString:
				continue
			if index==0:
				key = tdObj.string
			elif index==1:
				#超过1000的时候，用','分割，去掉','
				vol = tdObj.string.replace(',','')
				value = int(vol)
			else:
				break
			index += 1
		#print (key, value)
		price_dict[key] = value
	#print(soup.table)
	return
	
def get_price_list_163(code, price_dict, sort='PRICE', order=-1):
	urlfmt = "http://quotes.money.163.com/service/fenjia_table.html?symbol=%s&sort=%s&order=%d"
	url = urlfmt %(code, sort, order)
	#print ("fenjiabiao=",url)

	priceListPage = None
	LOOP_COUNT=0
	while LOOP_COUNT<3:
		try:
			priceListPage = urllib2.urlopen(url).read()
		except:
			LOOP_COUNT += 1
			continue
		else:
			break
	if priceListPage is None:
		print("Get 163 price list fail", url)
		return
	parse_price_list(priceListPage, price_dict)
	#print(price_dict)
	return

def fetch_kday_page(url):  #获取页面数据
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
		print "Content compressed"
		content = zlib.decompress(content, 16+zlib.MAX_WBITS);
	return content

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
	#print('netease', url)

	page=fetch_kday_page(url)#.decode('gb2312')

	if page=='':
		return -1
	with open("./internal/db/"+index_temp+".csv", "wb") as code:     
		code.write(page)
	#page.to_csv('_a.csv')
	return 0

def get_index_history_byNetease_js(location, index_temp):
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
	url='http://img1.money.126.net/data/hs/kline/day/times/%s.json'%(index_id)
	print('netease js', url)

	page=fetch_kday_page(url)#.decode('gb2312')
	#print "pp", type(page)
	if page=='':
		return -1

	#print page
	#json.dumps(page.encode('gbk'))
	
	file = open(location, "w")
	json.dump(page.encode('gbk'), file)
	file.close()
	
	#with open("./internal/db/"+index_temp+"_json.txt", "wb") as code:     
	#	code.write(page)
	#page.to_csv('_a.csv')
	return 0

if __name__ == "__main__":
	p_dict={}
	get_price_list_163('605108', p_dict)
	pass
