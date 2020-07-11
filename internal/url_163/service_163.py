#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import json
import re
import urllib2
from bs4 import BeautifulSoup
from bs4 import element

#对数据解析
def parse_price_list(priceListPage):
	#soup = BeautifulSoup(content, 'lxml', from_encoding='utf8')
	soup = BeautifulSoup(priceListPage, 'lxml')
	#print(soup.prettify())
	for item in soup.table.children:
		if type(item)!=element.Tag:
			continue
		print (type(item))
		#print ("========")
	#print(soup.table)
	
	
def get_price_list_163(code, price_dict, sort='PRICE', order=-1):
	urlfmt = "http://quotes.money.163.com/service/fenjia_table.html?symbol=%s&sort=%s&order=%d"
	url = urlfmt %(code, sort, order)
	print (url)

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
	#print priceListPage
	parse_price_list(priceListPage)
	return

if __name__ == "__main__":
	p_dict={}
	get_price_list_163('300849', p_dict)
	pass
