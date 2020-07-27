#!/usr/bin/env python
# -*- coding:gbk -*-
#中文测试
import sys
import os
import re
import datetime
import urllib2
import json
import zlib
import bs4
from ast import literal_eval

sys.path.append(".")
from internal.format_parse import *
from internal.global_var import g_shcd
from internal.global_var import g_szcd

url_sn = "http://hq.sinajs.cn/list="

urlkline = "http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=%s&scale=%d&ma=%s&datalen=%d"
send_headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'DNT': 1,
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.8'
}

def get_history_trade_info_bysn(len=10, code='sh000001', scale=240, ma='no'):
	urlall = urlkline % (code, scale, ma, len)
	#print(urlall)
	try:
		req = urllib2.Request(urlall,headers=send_headers)
		res_data = urllib2.urlopen(req)
	except:
		print "Error fupai urlopen"
		#LOOP_COUNT = LOOP_COUNT+1
	if res_data is None:
		print "Open URL fail"
		exit(0)

	content = res_data.read()
	respInfo = res_data.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
		#print "Content compressed"
		content = zlib.decompress(content, 16+zlib.MAX_WBITS);
	return content

def parse_each_item(tr_obj, key, pos, list):
	#print((tr_obj.td.encode('gbk')))
	b_match = 0
	for td in tr_obj.children:
		if b_match==0:
			val = td.encode('gbk').find(key)
			if val>-1:
				b_match = 1
				continue
		if b_match==1:
			if pos == 0:
				list.append(td.string)
				continue

			if td.string=='--':
				list.append(0)
			else:
				#print(td.string)
				s = re.findall("\d+",td.string)[0]
				#print("val=", s, s.isdigit())
				if not s.isdigit():
					print("Error: inval digit", s)
					return -1
				#print(td.string.split())
				#print([int(s) for s in td.string.split() if s.isdigit()])
				list.append(int(s))
		#end if b_match
	#end for tr_obj.children
	#val = tr_obj.td.encode('gbk').find("变动日期")
	#print "\n\n"

url_gb='http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockStructure/stockid/%s.phtml'
url_gb_dt='http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockStructurePicture/stockid/%s/alertdate/%s.phtml'
def get_guben_change_bysn(code):
	res_data = None
	url = url_gb % (code)
	#print(url)
	try:
		req = urllib2.Request(url,headers=send_headers)
		res_data = urllib2.urlopen(req)
	except:
		pass
		#print("Error fupai urlopen")
		#LOOP_COUNT = LOOP_COUNT+1
	if res_data is None:
		print("Open URL fail", url)
		return None

	content = res_data.read()
	respInfo = res_data.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
		content = zlib.decompress(content, 16+zlib.MAX_WBITS);
	#print(content)

	soup = bs4.BeautifulSoup(content, 'lxml')
	
	item = soup.find(id='con02-1')
	if item is None:
		print("No find id con02-1")
		return None
	#print(item.encode('gbk'))
	scrp_tag = item.find("script")
	if scrp_tag is None:
		print("No script tag")
		return None
	scrp_str = scrp_tag.string.strip()
	scrp_obj = re.match(r'romanceTables\((.*)\);', scrp_str)
	if scrp_obj is None:
		print("Not match romanceTables[]", scrp_str)
		return None
	romance = scrp_obj.group(1)
	if romance=="[]":
		print("No data in romanceTables[]", code)
		return None

	rm_list =literal_eval(romance)
	title = ['变动日期', '','','','总股本','','流通A股','高管股','限售A股']
	filter = [0, 4, 6, 7, 8]
	total_list = []
	for gb_tab in rm_list:
		tab_item = item.find(id=gb_tab)
		tbody_obj = tab_item.tbody
		idx = 0
		for tr_obj in tbody_obj.find_all('tr'):
			#print((tr_obj.td.string))
			#val = td.encode('gbk').find("变动日期")
			#handle(
			if idx in filter:
				pos = filter.index(idx)
				temp_list = []
				ret = parse_each_item(tr_obj, title[idx], pos, temp_list)
				if ret==-1:
					return None
				#print(pos)
				#print(temp_list)

				if len(total_list)<=pos:
					total_list.append(temp_list)
				else:
					total_list[pos].extend(temp_list)
			idx += 1
			#break
			#print(tr_obj.td)
		#end for tr_obj 
		#break
	#end for gb_tab
	#print("\n")
	#print(total_list)
	return total_list

#沪市的结果最后是 '00,'
#深市的结果最后是 '00'
def req_data_bysn(fmt_code):
	retry = 0
	req_url = url_sn + fmt_code
	#print(req_url)
	stockData = None
	while retry<3:
		try:
			req = urllib2.Request(req_url)
			stockData = urllib2.urlopen(req, timeout=2).read()
		except:
			if retry==2:
				print "URL timeout"
			retry += 1
			continue
		else:
			break
			'''
			for i in range(0, stockLen):
				sobj = stockObj[i].decode('gbk')
				print u"%02d:	%s" % (i, sobj)
			'''
	return stockData

def get_index_data(idx_list, idx_str):
	res_data = ''
	url = "http://hq.sinajs.cn/?_=0.7577027725009173&list=" + idx_str
	#print("Sine index", url)
	LOOP_COUNT = 0
	while LOOP_COUNT<3:
		try:
			req = urllib2.Request(url)
			res_data = urllib2.urlopen(req, timeout=2).read()
		except:
			LOOP_COUNT += 1
			time.sleep(0.5)
		else:
			break;
	resObj = res_data.split(';')
	for item in resObj:
		idx_list.append(item)	

def sina_code(code):
	ncode = code
	head3 = code[0:3]
	if head3 in g_szcd:
		ncode = 'sz' + code
	elif head3 in g_shcd:
		ncode = 'sh' + code
	else:
		print("Error: Not match code=" + code)
	return ncode

url_fenshi_k="https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData"
def get_k5_data_bysn(code, fenshi=5, ma='no', len=240):
	url_arg = "symbol=%s&scale=%d&ma=%s&datalen=%d"
	ret, ncode=parseCode(code)
	url_arg_fill = url_arg % (ncode, fenshi, ma, len)
	url = "%s?%s" % (url_fenshi_k, url_arg_fill)
	#print (url)
	
	stockData = None
	LOOP_COUNT=0
	while LOOP_COUNT<3:
		try:
			stockData = urllib2.urlopen(url).read()
		except:
			LOOP_COUNT += 1
			continue
		else:
			break
	if stockData is None:
		print("Get sina fenshi K fail", url)
		return None
	
	klist = json.loads(stockData)
	#print(stockData)
	return klist

def get_kday_data_bysn(code, fenshi=240, ma='no', len=60):
	url_arg = "symbol=%s&scale=%d&ma=%s&datalen=%d"
	ret, ncode=parseCode(code)
	url_arg_fill = url_arg % (ncode, fenshi, ma, len)
	url = "%s?%s" % (url_fenshi_k, url_arg_fill)
	#print (url)
	
	stockData = None
	LOOP_COUNT=0
	while LOOP_COUNT<3:
		try:
			stockData = urllib2.urlopen(url).read()
		except:
			LOOP_COUNT += 1
			continue
		else:
			break
	if stockData is None:
		print("Get sina fenshi K fail", url)
		return None
	
	klist = json.loads(stockData)
	#print(stockData)
	return klist

if __name__=="__main__":
	klist = get_k5_data_bysn('300291')
	for item in klist:
		print(item)
