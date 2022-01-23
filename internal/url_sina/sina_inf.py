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
import time
from ast import literal_eval

sys.path.append(".")
from internal.format_parse import *
from internal.global_var import g_shcd
from internal.global_var import g_szcd


'''
#新浪的实时接口,分为
# 获取单只个股 http://hq.sinajs.cn/list=sh601006
var hq_str_sh601006="大秦铁路, 27.55, 27.25, 26.91, 27.55, 26.20, 26.91, 26.92, 
22114263, 589824680, 4695, 26.91, 57590, 26.90, 14700, 26.89, 14300,
26.88, 15100, 26.87, 3100, 26.92, 8900, 26.93, 14230, 26.94, 25150, 26.95, 15220, 26.96, 2008-01-11, 15:05:32";
这个字符串由许多数据拼接在一起，不同含义的数据用逗号隔开了，按照程序员的思路，顺序号从0开始。
0：”大秦铁路”，股票名字；
1：”27.55″，今日开盘价；
2：”27.25″，昨日收盘价；
3：”26.91″，当前价格；
4：”27.55″，今日最高价；
5：”26.20″，今日最低价；
6：”26.91″，竞买价，即“买一”报价；
7：”26.92″，竞卖价，即“卖一”报价；
8：”22114263″，成交的股票数，由于股票交易以一百股为基本单位，所以在使用时，通常把该值除以一百；
9：”589824680″，成交金额，单位为“元”，为了一目了然，通常以“万元”为成交金额的单位，所以通常把该值除以一万；
10：”4695″，“买一”申请4695股，即47手；
11：”26.91″，“买一”报价；
12：”57590″，“买二”
13：”26.90″，“买二”
14：”14700″，“买三”
15：”26.89″，“买三”
16：”14300″，“买四”
17：”26.88″，“买四”
18：”15100″，“买五”
19：”26.87″，“买五”
20：”3100″，“卖一”申报3100股，即31手；
21：”26.92″，“卖一”报价
(22, 23), (24, 25), (26,27), (28, 29)分别为“卖二”至“卖四的情况”
30：”2008-01-11″，日期；
31：”15:05:32″，时间；

# 获取多只个股 http://hq.sinajs.cn/list=sh601003,sh601001
# 获取指数 http://hq.sinajs.cn/list=s_sh000001

# 获取简要信息：		http://qt.gtimg.cn/q=s_sz002818
v_s_sz002818="51~富森美~002818~72.50~6.59~10.00~203451~144984~~319.00";
0: 不明
1: 名字
2: 代码
3: 现价
4: 涨跌
5: 涨跌%
6: 成交量（手）
7: 成交额（万）
8: /
9: 总市值
# 获取盘口分析：		http://qt.gtimg.cn/q=s_pksz002818
002818="-1.0~-1.0~-1.0~-1.0";
0: 买盘大单
1: 买盘小单
2: 卖盘大单
3: 卖盘小单
# 获取实时资金流向：	http://qt.gtimg.cn/q=ff_sz002818
v_ff_sz002818="sz002818~61516.50~5871.35~55645.15~38.38~83467.00~139111.84~-55644.84~-38.38~144983.50~62989.0~5911.98~富森美~
20161121~20161118^1089.29^40.63~20161117^174.89^0.00~20161116^155.70^0.00~20161115^52.62^0.00";
 0: 代码
 1: 主力流入
 2: 主力流出
 3: 主力净流入
 4: 主力净流入/资金流入流出总和
 5: 散户流入
 6: 散户流出
 7: 散户净流入
 8: 散户净流入/资金流入流出总和
 9: 资金流入流出总和1+2+5+6
10: 不明
11: 不明
12: 名字
13: 日期
# 获取最新行情，访问数据接口：	http://qt.gtimg.cn/q=sz002818
v_sz002818="51~富森美~002818~72.50~65.91~72.46~203451~103832~99620~72.50~6229~72.49~1066~72.48~29~72.47~14~72.46~35~0.00~0~0.00~0~0.00~0~0.00~0~0.00~0~15:00:04
/72.50/356/S/2581000/15070|14:57:00/72.50/5/S/36250/14971|14:56:57/72.50/2/S/14500/14968|14:56:55/72.50/7/S/50750/14963|14:56:51/72.50/13/S/94250/14960|14:56:45
/72.50/9/S/65250/14952~20161121150133~6.59~10.00~72.50~69.46~72.50/203095/1447255013~203451~144984~46.24~70.47~~72.50~69.46~4.61~31.90~319.00~10.57~72.50~59.32~411.68";
 0: 不明
 1: 名字
 2: 代码
 3: 现价
 4: 昨收
 5: 今开
 6: 成交量（手）
 7: 外盘
 8: 内盘
 9: 买一
10: 买一量（手）
11-18: 买二 - 买五
19: 卖一
20: 卖一量
21-28: 卖二 - 卖五
29: 最近逐笔成交
30: 时间
31: 涨跌
32: 涨跌%
33: 最高
34: 最低
35: 价格/成交量（手）/成交额
36: 成交量（手）
37: 成交额（万）
38: 换手率
39: 市盈率
40: /
41: 最高
42: 最低
43: 振幅
44: 流通市值
45: 总市值
46: 市净率
47: 涨停价
48: 跌停价
'''

url_sn = "http://hq.sinajs.cn/list="

urlkline = "http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=%s&scale=%d&ma=%s&datalen=%d"
send_headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'DNT': 1,
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.8'
}

common_sn_inf_headers = {
    'Host': 'hq.sinajs.cn',
    'Connection': 'keep-alive',
	"Referer":"http://finance.sina.com.cn",
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Cache-Control": "max-age=0"
	}

def get_history_trade_info_bysn(len=10, code='sh000001', scale=240, ma='no'):
	urlall = urlkline % (code, scale, ma, len)
	#print(urlall)
	try:
		req = urllib2.Request(urlall,headers=send_headers)
		res_data = urllib2.urlopen(req)
	except:
		print "Error",sys._getframe().f_code.co_name
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
		#print "Error",sys._getframe().f_code.co_name
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
	#print(sys._getframe().f_code.co_name,":",sys._getframe().f_lineno,req_url)
	stockData = None
	while retry<3:
		try:
			req = urllib2.Request(req_url, headers=common_sn_inf_headers)
			stockData = urllib2.urlopen(req, timeout=2).read()
		except:
			if retry==2:
				print "URL timeout",sys._getframe().f_code.co_name,":",sys._getframe().f_lineno
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
			req = urllib2.Request(url, headers=common_sn_inf_headers)
			res_data = urllib2.urlopen(req, timeout=2).read()
		except Exception as e:
			LOOP_COUNT += 1
			time.sleep(0.5)
			if LOOP_COUNT==2:
				print "sina_inf",e
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
	#print ("k5_data:",url)
	
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
