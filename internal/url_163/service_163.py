#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import json
import re
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

if __name__ == "__main__":
	p_dict={}
	get_price_list_163('605108', p_dict)
	pass
