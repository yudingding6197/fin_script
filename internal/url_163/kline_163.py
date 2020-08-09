#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import json
import re
import urllib2
import zlib
#sys.path.append('.')
from internal.format_parse import *

def get_kday_163(code, year):
	urlfmt = "http://img1.money.126.net/data/hs/kline/day/history/%s/%s.json"
	ret, code_wy = parseCode(code, 'wy')
	if ret==-1:
		print("Invalid code", code)
		return None
	url = urlfmt %(year, code_wy)
	#print ("163 kday=",url)

	res_data = None
	LOOP_COUNT=0
	while LOOP_COUNT<3:
		try:
			res_data = urllib2.urlopen(url)
		except:
			LOOP_COUNT += 1
			continue
		else:
			break
	if res_data is None:
		return None

	content = res_data.read()
	respInfo = res_data.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
		#print "Content compressed"
		content = zlib.decompress(content, 16+zlib.MAX_WBITS);
	#print content.decode('utf8')
	
	#parse_price_list(priceListPage, price_dict)
	#print(price_dict)
	#print "c",content[:32]
	return content

if __name__ == "__main__":
	get_kday_163('000029', '2019')
	pass
