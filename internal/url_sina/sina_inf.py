#!/usr/bin/env python
# -*- coding:gbk -*-
#���Ĳ���
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
#���˵�ʵʱ�ӿ�,��Ϊ
# ��ȡ��ֻ���� http://hq.sinajs.cn/list=sh601006
var hq_str_sh601006="������·, 27.55, 27.25, 26.91, 27.55, 26.20, 26.91, 26.92, 
22114263, 589824680, 4695, 26.91, 57590, 26.90, 14700, 26.89, 14300,
26.88, 15100, 26.87, 3100, 26.92, 8900, 26.93, 14230, 26.94, 25150, 26.95, 15220, 26.96, 2008-01-11, 15:05:32";
����ַ������������ƴ����һ�𣬲�ͬ����������ö��Ÿ����ˣ����ճ���Ա��˼·��˳��Ŵ�0��ʼ��
0����������·������Ʊ���֣�
1����27.55�壬���տ��̼ۣ�
2����27.25�壬�������̼ۣ�
3����26.91�壬��ǰ�۸�
4����27.55�壬������߼ۣ�
5����26.20�壬������ͼۣ�
6����26.91�壬����ۣ�������һ�����ۣ�
7����26.92�壬�����ۣ�������һ�����ۣ�
8����22114263�壬�ɽ��Ĺ�Ʊ�������ڹ�Ʊ������һ�ٹ�Ϊ������λ��������ʹ��ʱ��ͨ���Ѹ�ֵ����һ�٣�
9����589824680�壬�ɽ�����λΪ��Ԫ����Ϊ��һĿ��Ȼ��ͨ���ԡ���Ԫ��Ϊ�ɽ����ĵ�λ������ͨ���Ѹ�ֵ����һ��
10����4695�壬����һ������4695�ɣ���47�֣�
11����26.91�壬����һ�����ۣ�
12����57590�壬�������
13����26.90�壬�������
14����14700�壬��������
15����26.89�壬��������
16����14300�壬�����ġ�
17����26.88�壬�����ġ�
18����15100�壬�����塱
19����26.87�壬�����塱
20����3100�壬����һ���걨3100�ɣ���31�֣�
21����26.92�壬����һ������
(22, 23), (24, 25), (26,27), (28, 29)�ֱ�Ϊ���������������ĵ������
30����2008-01-11�壬���ڣ�
31����15:05:32�壬ʱ�䣻

# ��ȡ��ֻ���� http://hq.sinajs.cn/list=sh601003,sh601001
# ��ȡָ�� http://hq.sinajs.cn/list=s_sh000001

# ��ȡ��Ҫ��Ϣ��		http://qt.gtimg.cn/q=s_sz002818
v_s_sz002818="51~��ɭ��~002818~72.50~6.59~10.00~203451~144984~~319.00";
0: ����
1: ����
2: ����
3: �ּ�
4: �ǵ�
5: �ǵ�%
6: �ɽ������֣�
7: �ɽ����
8: /
9: ����ֵ
# ��ȡ�̿ڷ�����		http://qt.gtimg.cn/q=s_pksz002818
002818="-1.0~-1.0~-1.0~-1.0";
0: ���̴�
1: ����С��
2: ���̴�
3: ����С��
# ��ȡʵʱ�ʽ�����	http://qt.gtimg.cn/q=ff_sz002818
v_ff_sz002818="sz002818~61516.50~5871.35~55645.15~38.38~83467.00~139111.84~-55644.84~-38.38~144983.50~62989.0~5911.98~��ɭ��~
20161121~20161118^1089.29^40.63~20161117^174.89^0.00~20161116^155.70^0.00~20161115^52.62^0.00";
 0: ����
 1: ��������
 2: ��������
 3: ����������
 4: ����������/�ʽ����������ܺ�
 5: ɢ������
 6: ɢ������
 7: ɢ��������
 8: ɢ��������/�ʽ����������ܺ�
 9: �ʽ����������ܺ�1+2+5+6
10: ����
11: ����
12: ����
13: ����
# ��ȡ�������飬�������ݽӿڣ�	http://qt.gtimg.cn/q=sz002818
v_sz002818="51~��ɭ��~002818~72.50~65.91~72.46~203451~103832~99620~72.50~6229~72.49~1066~72.48~29~72.47~14~72.46~35~0.00~0~0.00~0~0.00~0~0.00~0~0.00~0~15:00:04
/72.50/356/S/2581000/15070|14:57:00/72.50/5/S/36250/14971|14:56:57/72.50/2/S/14500/14968|14:56:55/72.50/7/S/50750/14963|14:56:51/72.50/13/S/94250/14960|14:56:45
/72.50/9/S/65250/14952~20161121150133~6.59~10.00~72.50~69.46~72.50/203095/1447255013~203451~144984~46.24~70.47~~72.50~69.46~4.61~31.90~319.00~10.57~72.50~59.32~411.68";
 0: ����
 1: ����
 2: ����
 3: �ּ�
 4: ����
 5: ��
 6: �ɽ������֣�
 7: ����
 8: ����
 9: ��һ
10: ��һ�����֣�
11-18: ��� - ����
19: ��һ
20: ��һ��
21-28: ���� - ����
29: �����ʳɽ�
30: ʱ��
31: �ǵ�
32: �ǵ�%
33: ���
34: ���
35: �۸�/�ɽ������֣�/�ɽ���
36: �ɽ������֣�
37: �ɽ����
38: ������
39: ��ӯ��
40: /
41: ���
42: ���
43: ���
44: ��ͨ��ֵ
45: ����ֵ
46: �о���
47: ��ͣ��
48: ��ͣ��
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
	#val = tr_obj.td.encode('gbk').find("�䶯����")
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
	title = ['�䶯����', '','','','�ܹɱ�','','��ͨA��','�߹ܹ�','����A��']
	filter = [0, 4, 6, 7, 8]
	total_list = []
	for gb_tab in rm_list:
		tab_item = item.find(id=gb_tab)
		tbody_obj = tab_item.tbody
		idx = 0
		for tr_obj in tbody_obj.find_all('tr'):
			#print((tr_obj.td.string))
			#val = td.encode('gbk').find("�䶯����")
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

#���еĽ������� '00,'
#���еĽ������� '00'
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
