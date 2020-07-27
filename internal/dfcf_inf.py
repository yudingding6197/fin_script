#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import os
import re
import datetime
import urllib2
import json
import zlib

urlall = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._BKGN&sty=FPGBKI&st=c&sr=-1&p=1&ps=5000&cb=&token=7bc05d0d4c3c22ef9fca8c2a912d779c&v=0.2694706493189898"
send_headers = {
 'Host':'nufm.dfcfw.com',
 'User-Agent':'User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
 'Accept':'*/*',
 'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
 'DNT':'1',
 'Connection':'keep-alive'
}

class bkStatInfo:
	increase = 0
	fall = 0
	s_zthl = 0
	zt_count = 0
	zt_list = []
	dt_count = 0
	dt_list = []

def query_gainianbankuai(listobj, bkInfo):
	try:
		req = urllib2.Request(urlall,headers=send_headers)
		res_data = urllib2.urlopen(req)
	except:
		print "Error fupai urlopen"
		#LOOP_COUNT = LOOP_COUNT+1

	if res_data is None:
		print "Open URL fail"
		return

	content = res_data.read()
	line = content.decode('utf8')
	obj = re.match('.*\(\[(.*)\]\)',line)
	line = obj.group(1)
	#���if�����ж϶��࣬ǿ������ƥ�������������""
	if line is None:
		pos = line.find('"')
		if pos == -1:
			print "NOT Find Left"
			return
		rpos = line.rfind('"')
		if rpos==-1:
			print "NOT Find Right"
			return
		if rpos<=pos:
			print "Invalid result"
			return
		line = line[pos:rpos+1]
	#����	�������	�����Ѷ	���¼�	�ǵ���	�ǵ���	����ֵ(��)	������	���Ǽ���	�µ�����	���ǹ�Ʊ	�ǵ���
	#1	������ͣ	����ɰ� �ʽ���	9541.65	379.05	4.14%	304	9.66%	9	0	��ʯ��	10.00%
	#2	����оƬ	����ɰ� �ʽ���	1240.10	30.68	2.54%	4929	2.14%	34	5	�۲ӹ��	10.03%

	#Flag(0)���� �������(2)�Ƿ� ����ֵ ������ ���Ǽ���|ƽ�̼���|�µ�����|ͣ�Ƽ���(6),���ɴ���(7)Flag ��������(9)�۸� �Ƿ�(11),���ɴ���(12)Flag ��������(14)�۸� ����(16),Flag ����ֵ(18)�ǵ���(19) 
	#1,BK0891,����оƬ,2.53,493268904578,2.28,35|1|4|1,300708,2,�۲ӹ��,17.01,10.03,300613,2,���΢,206.99,-2.31,3,1239.97,30.55
	#1,BK0706,���Թ���,-0.15,70185675359,0.28,4|1|3|0,300238,2,�������,24.18,1.00,300244,2,�ϰ����,27.20,-2.30,3,1667.64,-2.57

	#bk ���
	#lz ����
	rank = 0
	strline = u'����,�������,����Ƿ�,����,���Ǹ���,�Ƿ�,�������,����'
	while 1:
		#ͨ����̰��ģʽ����ƥ�䣬�ؼ���'?'
		obj = re.match(r'"(.*?)",?(.*)', line)
		if obj is None:
			break
		line = obj.group(2)
		#print obj.group(1)
		str_arr = obj.group(1).split(',')
		bk_code = str_arr[1]
		bk_name = str_arr[2]
		left = 10-len(bk_name.encode('gbk'))
		for i in range(0, left):
			bk_name += ' '
		bk_change = str_arr[3]
		if str_arr[3]=='-':
			bk_change_f = 0
		else:
			bk_change_f = float(str_arr[3])
		bk_stat = str_arr[6]
		lz_code = str_arr[7]
		lz_name = str_arr[9]
		left = 10-len(lz_name.encode('gbk'))
		for i in range(0, left):
			lz_name += ' '
		lz_change = str_arr[11]
		if lz_change=='-':
			print "lz_change", lz_change
			lz_change_f = 0
		else:
			lz_change_f = float(lz_change)
		if lz_change_f>=9.9:
			lz_change = '##' + lz_change
			if lz_code not in bkInfo.zt_list:
				bkInfo.zt_count += 1
				bkInfo.zt_list.append(lz_code)
		else:
			lz_change = '  ' + lz_change
		ld_code = str_arr[12]
		ld_name = str_arr[14]
		left = 10-len(ld_name.encode('gbk'))
		for i in range(0, left):
			ld_name += ' '
		ld_change = str_arr[16]
		ld_change_f = float(ld_change)
		if ld_change_f<=-9.9:
			ld_change = '**' + ld_change
			if ld_code not in bkInfo.dt_list:
				bkInfo.dt_count += 1
				bkInfo.dt_list.append(ld_code)
		else:
			ld_change = '  ' + ld_change
		bk_price = str_arr[18]
		bk_value = str_arr[19]

		rank += 1
		fmt = "%4d %-s %6s  %-16s %-s %-8s %-s %-8s"
		str = fmt % (rank, bk_name, bk_change, bk_stat, lz_name, lz_change, ld_name, ld_change)
		#print str
		listobj.append(str)
		
		if bk_change_f>0:
			bkInfo.increase += 1
		elif bk_change_f<0:
			bkInfo.fall += 1
	return

#����Ƿ����ڽ��ף�����û�н��׵�
def checkTradeZhai(kzzdt, filter_tp):
	if kzzdt['ZGJ']=='-':
		return 0
	if filter_tp==2:
		return 1
	trdate = kzzdt['LISTDATE']
	if trdate=='-':
		return 0

	#[LISTDATE]='2016-01-18T00:00:00'
	trdate = trdate[0:10]
	trd_date = datetime.datetime.strptime(trdate, '%Y-%m-%d').date()
	tdy_date = datetime.date.today()
	delta = (tdy_date - trd_date).days
	if delta<0:
		return 0
	return 1

#filter_tp:
# 0: �����ˣ��õ����е�
# 1: ֻ�������ڽ��׵�
# 2: ���ڽ��׵ĺͽ�Ҫ���л�δ���׵�
def getFilterZhai(content, filter_tp, kzzlist):
	if content=='':
		return

	tick = 0
	while 1:
		dataObj = re.match(r'({.*?}),?(.*)', content)
		if dataObj is None:
			break
		item = dataObj.group(1)
		content = dataObj.group(2)

		d2 = json.loads(item)
		#print("item=", type(d2))
		if filter_tp==0:
			kzzlist.append(d2)
			continue
		if checkTradeZhai(d2, filter_tp)==0:
			continue
		#print "filter===",d2['SNAME']
		kzzlist.append(d2)
	return

def getZhaiDetail(content, kzzlist):
	if content=='':
		return
	getFilterZhai(content, 0, kzzlist)
	return

def getKZZConnect(urlfmt, send_headers, page):
	LOOP_COUNT=0
	urllink = urlfmt % (page)
	res_data = None
	while LOOP_COUNT<3:
		try:
			#print urllink
			req = urllib2.Request(urllink,headers=send_headers)
			res_data = urllib2.urlopen(req)
		except:
			print "Exception kzz urlopen"
			LOOP_COUNT += 1
		else:
			break
	if res_data is None:
		print "Error: Fail to get request"
		return ''

	content = res_data.read()
	respInfo = res_data.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
		#print "Content compressed"
		content = zlib.decompress(content, 16+zlib.MAX_WBITS);
	#else:
	#	print "Content not zip"

	content = content.decode('utf8')
	#print (content)
	return content

'''
GET /EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._A&sty=FCOIATA&sortType=A&sortRule=1&page=1&pageSize=20&js=var%20quote_123%3d{rank:[(x)],pages:(pc)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.11244183898795046 HTTP/1.1
Host: nufm.dfcfw.com
Connection: keep-alive
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36
Accept: */*
DNT: 1
Referer: http://quote.eastmoney.com/center/list.html
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.8

'''
def get_each_page_data(new_st_list, curpage, st='A', sr=-1, ps=80):
	link = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?"
	key1 = "type=CT&cmd=C._A&sty=FCOIATA&sortType=%s&sortRule=%d"
	urlfmt = link + key1 +"&page=%d&pageSize=%d&js={rank:[(x)],pages:(pc)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c"

	LOOP_COUNT = 0
	response = None
	url = urlfmt % (st, sr, curpage, ps)
	#print(url)
	while LOOP_COUNT<3:
		try:
			req = urllib2.Request(url)
			response = urllib2.urlopen(req, timeout=5).read()
		except:
			LOOP_COUNT += 1
			print("URL request timeout ", url)
		else:
			break
	if response is None:
		print "Please check data from DongCai at", curpage
		return -1

	line = response.decode('utf8')
	#print line
	obj = re.match(r'{rank:\["(.*)"\],pages:(\d+)', line)
	if obj is None:
		print "Not find matched content at", curpage
		return -1
	totalpage = int(obj.group(2))
	
	rank = obj.group(1)
	array = rank.split('","')
	for i in range(0, len(array)):
		props = array[i].split(',')
		#code = props[1]
		pre_close = props[9]
		if pre_close!='0.00':
			line = array[i][2:]
			#print(line)
			new_st_list.append(line.encode('gbk'))
		#file.write(line.encode('gbk')+'\n')
	#�������ҳ�棬����0
	if totalpage==curpage:
		return 0
	return 1

def get_latest_market(new_st_list):
	curpage = 1
	while 1:
		bnext = get_each_page_data(new_st_list, curpage)
		if bnext==0:
			break
		elif bnext==-1:
			continue
		curpage += 1
	return

def get_market_by_chg_per(new_st_list, st='C', sr=-1, ps=80):
	curpage = 1
	while 1:
		bnext = get_each_page_data(new_st_list, curpage, st, sr, ps)
		if bnext==0:
			break
		elif bnext==-1:
			continue
		curpage += 1
	return

def get_stk_code_by_cond(new_st_list, st='C', sr=-1, ps=80):
	curpage = 1
	items_list = []
	while 1:
		bnext = get_each_page_data(items_list, curpage, st, sr, ps)
		if bnext==0:
			break
		elif bnext==-1:
			continue
		curpage += 1
	for item in items_list:
		new_st_list.append(item[0:6])
	return

def getSelfDefStock(stk_arr):
	'''
	h_cook=\
'ct=0MQGTduqB7_LXzJefU6a84F3axofQVJHEBs6uOpXoMyFssYG4WXsYR9VRS2qe7xEjRbpI0x9NeBLzBXO2pSeXs-EUqnRH6u8\
G0iKbyXg5WgHZa2DAPg8m5awyb1kz2T5cIf2Ai7eI9dxL2R5_xsHifIJ2Pq0zcUAR9LVVSlR7-I; ut=FobyicMgeV4UJna6Au6ASu7wtul_n26_zn\
6kEQZ0cxP_TJaAGEHI10yGGvZqOGB_iuq8qRe-QXGC8BrY0FM7PobIY8SwUBNW2WeJuN65h0-s4vjZ_M7hL9xBF7lspjMki1CnUiFTfptLZJn1\
mb8E_x9ZYWIhCyakraCd0Tl8EWqlDGefSBj6FjSec7PSwye3AgIhmlVY6VMeL3pRsVw6pNPcDG30oX38hevvlF8MMS-dCGgysgIVQtBZ_LfymTDGU\
pxDm-U8wjNX4i6gUh6HGld3r1jNmdez; uidal=6100112247957528goutou; sid=4725419;'
	'''
	h_cook = 'ct=O9ZbuRz1amNRNaHuo6p_zDrKzlpcmMMVE-I1pORXze0hFFJmIfaVfCVT1ZcTmqfm5seYjyHFZQ4JlqFr3PmjCq7nI2KRllEPhWeJC2jpGGqbwT3kR2WmKskG52FVhoqtE5wXs_MWZOwKp5VXHNrLnoGJY7AtPtheKaIA_q-b4cc; ut=FobyicMgeV5ghfUPKWOH5-EbXa3GCsCh6Q30W7-VNW_UnLFG_MdgzYGBtd4GAeTiJtHTVQiNxpl2h0NwV6n1RXoRUuthaz6dCYLKYm2925w4OiK5JsUb8hIH4sIyertjQs-NQXBQYIvk24PwJZxYgZ3KvDkWrRVW-3mRLATfABleSx80pH9rhTMsDI_EMLOB7ok1zVXIDIOs80M32p9bw9HZ0MqKhGyo4E4gUJUohSblEPhcYlXMdzmqnz3qUIStTYsyjHhPTR8kZc7RIrzvLDAAx_nxgfOc; pi=6100112247957528%3byudingding6197%3bgoutou%3bvPGmLLZOT7HuuGpA2MxZSWwqFz3mUhG5n8op%2fwV4R%2bSfU9DXvhqnxHc0jlj%2b3Tk72lPHhT8k1IYVbrFHbTFpQhDTdF2S3lj2Fw862vuvLCrBHEAZg%2fsv7Abkj9ET7Bd7bilQ3uLyaSLDpzFLsOuyt%2b5q%2bAtFdVAxh%2bS50Jfl6bH9UgKzl4ZaSe06BhVIN64bR2u9JRJA%3b2vts%2fCaYY8wl9ETF%2b9x7cLixcC%2f0OdlTSRYCeFwb6vMJGELum8agNvRvvQcxsWRDMKpz5hsFrYXFXJ3k7nwczS2x%2bhcIcZkHCgwX4pEaf2lcy9DYJ8UJ56vIzVzJzxNqAPJjLmqUg%2fKx5FfhK7092iywo5lDpQ%3d%3d; uidal=6100112247957528goutou; '
	prestr = 'getStockInfo'
	urlall = 'http://myfavor1.eastmoney.com/mystock?f=gs&cb='+ prestr +'&g=41445869&0.617530589249439'
	send_headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
	'Accept': '*/*',
	'DNT': 1,
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.8',
	'Cookie': h_cook
	}

	#print(urlall)
	res_data = None
	try:
		#����1
		#res_data = urllib2.urlopen(urlall)

		#����2
		req = urllib2.Request(urlall,headers=send_headers)
		res_data = urllib2.urlopen(req)
	except:
		print "Error fupai urlopen"
		#LOOP_COUNT = LOOP_COUNT+1

	if res_data is None:
		print "Open URL fail"
		return

	content = res_data.read()
	respInfo = res_data.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
		#print "Content compressed"
		content = zlib.decompress(content, 16+zlib.MAX_WBITS);
	else:
		#print "Content not zip"
		pass
	#��ƥ������(),ȥ������,��ƥ������������
	obj = re.match(r'^'+ prestr +'\((.*)\)', content)
	stkobj = json.loads(obj.group(1))
	if stkobj['result']=='-1':
		print stkobj['data']['msg']
		return ''

	strstr = stkobj['data']['order']
	stk_obj = strstr.split(',')
	stk_arr.extend(stk_obj)

def getHSIndexStat():
	urlall = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=0000011,3990012&sty=DFPIU&st=z&sr=&p=&ps=&cb=&js=(x)&token=44c9d251add88e27b65ed86506f6e5da&0.7034708404131944'
	res_data = None
	try:
		req = urllib2.Request(urlall,headers=send_headers)
		res_data = urllib2.urlopen(req)
	except:
		print "Error: open url"

	if res_data is None:
		print "Open URL fail"
		return None

	content = res_data.read()
	respInfo = res_data.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
		#print "Content compressed"
		content = zlib.decompress(content, 16+zlib.MAX_WBITS);
	return (content)

def get4IndexRaw():
	urlall = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=SZ.CYB,SZ.ZXB&sty=UDFN&js=(x)&token=de1161e2380d231908d46298ae339369'
	res_data = None
	try:
		req = urllib2.Request(urlall,headers=send_headers)
		res_data = urllib2.urlopen(req)
	except:
		print "Error: open url"
		return None

	if res_data is None:
		print "Open URL fail"
		return None

	content = res_data.read()
	respInfo = res_data.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
		#print "Content compressed"
		content = zlib.decompress(content, 16+zlib.MAX_WBITS);
	return (content)

# ["791|63|657|12,1092|78|1028|29,366|23|362|9","791|63|657|12,1092|78|1028|29,468|38|429|14"]
def get4IndexInfoList(idxList):
	rawData = get4IndexRaw()
	if rawData is None:
		return -1
	qtObj = re.match(r'"(.*?)","(.*)"', rawData)
	if qtObj is None:
		print("Quatate None")
		return -1

	indexObj = qtObj.group(1).split(',')

	#shang zhen
	zsObj = indexObj[0].split('|')
	idxList.append(zsObj)
	#shen zhen
	zsObj = indexObj[1].split('|')
	idxList.append(zsObj)
	#zxbz
	zsObj = indexObj[2].split('|')
	idxList.append(zsObj)
	
	indexObj = qtObj.group(2).split(',')
	#cybz
	zsObj = indexObj[2].split('|')
	idxList.append(zsObj)

	#print(idxList)
	return 0

def get4IndexInfo(idxDict):
	rawData = get4IndexRaw()
	if rawData is None:
		return -1
	qtObj = re.match(r'"(.*?)","(.*)"', rawData)
	if qtObj is None:
		print("Quatate None")
		return -1

	indexObj = qtObj.group(1).split(',')

	#shang zhen
	zsObj = indexObj[0].split('|')
	idxDict['000001'] = zsObj
	#idxList.append(zsObj)
	#shen zhen
	zsObj = indexObj[1].split('|')
	idxDict['399001'] = zsObj
	#zxbz
	zsObj = indexObj[2].split('|')
	idxDict['399005'] = zsObj
	
	indexObj = qtObj.group(2).split(',')
	#cybz
	zsObj = indexObj[2].split('|')
	idxDict['399006'] = zsObj

	#print(idxList)
	return 0
