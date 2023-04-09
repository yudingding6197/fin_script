
# -*- coding:gbk -*-
#!/usr/bin/env python

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
		print "Error",sys._getframe().f_code.co_name
		#LOOP_COUNT = LOOP_COUNT+1

	if res_data is None:
		print ("Open URL fail",sys._getframe().f_code.co_name)
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

#filter_ty:
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
		if filter_tp==0:
			kzzlist.append(d2)
			continue
		if checkTradeZhai(d2, filter_tp)==0:
			continue
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

#��һЩ�Ѿ����»�δ���е�New
#һЩͣ�Ƶģ�һЩ���е�
#��������������ZhengLi
def get_each_page_data1(new_st_list, curpage, st='A', sr=-1, ps=80):
	link = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?"
	key1 = "type=CT&cmd=C._A&sty=FCOIATA&sortType=%s&sortRule=%d"
	urlfmt = link + key1 +"&page=%d&pageSize=%d&js={rank:[(x)],pages:(pc)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c"
	send_headers = {
	'Host': 'nufm.dfcfw.com',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'DNT': 1,
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.8'
	}
	LOOP_COUNT = 0
	response = None
	url = urlfmt % (st, sr, curpage, ps)
	#print(url)
	while LOOP_COUNT<3:
		try:
			req = urllib2.Request(url, headers=send_headers)
			response = urllib2.urlopen(req, timeout=5)
		except:
			LOOP_COUNT += 1
			#print("URL request timeout ", url)
		else:
			break
	if response is None:
		print "Please check data from DongCai at", curpage
		return -1

	content = response.read()
	respInfo = response.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
		#print "Content compressed"
		line = zlib.decompress(content, 16+zlib.MAX_WBITS);

	line = line.decode('utf8')
	#print line
	obj = re.match(r'{rank:\["(.*)"\],pages:(\d+)', line)
	if obj is None:
		print "12Not find matched content at", curpage
		return -1
	totalpage = int(obj.group(2))
	
	rank = obj.group(1)
	array = rank.split('","')
	for i in range(0, len(array)):
		props = array[i].split(',')
		#code = props[1]
		#pre_close = props[9]
		rt_price = props[3]
		market_dt = props[-1]

		#print(line)
		#��δ����
		if market_dt=='-':
			continue
		#����ͣ��
		if rt_price=='-':
			continue
		#line = array[i][2:]
		#new_st_list.append(line.encode('gbk'))
		
		#TODO: debug, can remove it
		if i==11:
			if array[i]=='-':
				print rank
		#TODO: END
		
		new_st_list.append(props)

	#�������ҳ�棬����0
	if totalpage==curpage:
		return 0
	return 1

def get_stk_max_page(curpage, st='A', sr=-1, ps=80):
	link = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?"
	key1 = "type=CT&cmd=C._A&sty=FCOIATA&sortType=%s&sortRule=%d"
	urlfmt = link + key1 +"&page=%d&pageSize=%d&js={rank:[(x)],pages:(pc)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c"
	send_headers = {
	'Host': 'nufm.dfcfw.com',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'DNT': 1,
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.8'
	}
	LOOP_COUNT = 0
	response = None
	url = urlfmt % (st, sr, curpage, ps)
	print(url)
	while LOOP_COUNT<3:
		try:
			req = urllib2.Request(url, headers=send_headers)
			response = urllib2.urlopen(req, timeout=5)
		except:
			LOOP_COUNT += 1
			#print("URL request timeout ", url)
		else:
			break
	if response is None:
		print "Please check data from DongCai at", curpage
		return -1

	content = response.read()
	respInfo = response.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
		#print "Content compressed"
		line = zlib.decompress(content, 16+zlib.MAX_WBITS);

	line = line.decode('utf8')
	#print line
	obj = re.match(r'{rank:\["(.*)"\],pages:(\d+)', line)
	if obj is None:
		print "11Not find matched content at", curpage
		return -1
	totalpage = int(obj.group(2))
	return totalpage

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

#sort mode��
#'A' stock code
#'B' �ɼ�
#'C' �Ƿ�
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

#sort mode��
#'A' stock code
#'B' �ɼ�
#'C' �Ƿ�
def get_stk_code_by_cond1(new_st_list, st='C', sr=-1, ps=80):
	curpage = 1
	#items_list = []
	while 1:
		bnext = get_each_page_data1(new_st_list, curpage, st, sr, ps)
		if bnext==0:
			break
		elif bnext==-1:
			continue
		curpage += 1
	#for item in items_list:
	#	new_st_list.append(item[0:6])
	return 0

	
'''
"financecode":"37884","companycode":"80975294","securityshortname":"N����","securitycode":"601827","subcode":"780827",
"fxzl":378268000.0,"wsfxsl":340442000.0,"applyont":113000.0,"issuepriceMoney":772920.0,"issueprice":6.84,
"purchasedate":"2020-05-21T00:00:00","lwrandate":"2020-05-25T00:00:00","listingdate":"2020-06-05T00:00:00",
"peissuea":22.67,"lwr":0.14984,"cbxjrgbs":246.55989,"sc":"sh",
"mzyqgs":1000.0,"sgzs":65286100000.0,"applyontMoney":1130000.0,"averagelow":10000000.0,
"kb":"δ����",
"zzf":44.0058479532164,"sl":"-","mzyqhl":3010.0,"totaliiqrplaceoff":7539.0,"jg1":6.84,"jg2":6.98,"jg3":6.93,
"pe1":22.67,"pe2":23.16,"pe3":22.99,"bkpe":23.16,"INDUSTRY":"��̬�����ͻ�������ҵ","Close":9.85,"ChangePercent":44.01,
"ZgsmsOrYxs":"AN202005201379971122","Url":"http://topic.eastmoney.com/cqsfhj/",
"INDUSTRYPE":23.16,"newPrice":9.85,"wszqjkr":"2020-05-25T00:00:00",
"MAINBUSIN":"�������շ�����ĿͶ����Ӫ��EPC�����Լ��������շ�������豸�з������",
"ycwssgsx":340000.0,"ycwssgzj":3400000.0,"Update":"2020-06-08 00:09:22","sgrqrow":21.0
'''
#��ȡ��������New STK
def get_new_stk_from_dfcf(stk_list):
	h_cook = ''
	rslt_pre = 'YexzpM'
	url_req = 'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get'
	param = "?type=XGSG_LB&token=70f12f2f4f091e459a279469fe49eca5&st=listingdate,securitycode&sr=-1&ps=80&js=%s={pages:(tp),data:(x)}"
	send_headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
	'Accept': '*/*',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.8',
	'Cookie': h_cook
	}

	urlfmt = url_req + param
	url = urlfmt % (rslt_pre)
	#print("get_new_stk_from_dfcf",url)

	res_data = None
	LOOP_COUNT = 0
	while LOOP_COUNT<3:
		try:
			#����1
			#res_data = urllib2.urlopen(urlall)

			#����2
			req = urllib2.Request(url,headers=send_headers)
			res_data = urllib2.urlopen(req)
		except:
			print "Error",sys._getframe().f_code.co_name
			LOOP_COUNT = LOOP_COUNT+1
		else:
			break
	if res_data is None:
		print ("Open URL fail",sys._getframe().f_code.co_name)
		return

	content = res_data.read()
	objs = re.match(rslt_pre+"={pages:(\d+),data:\[(.*)\]}", content)
	if objs is None:
		print("Error: format invalid1")
		print rslt_pre, content[:20]
		return
	items = objs.group(2).split('},{')
	for item in items:
		#print(item)
		if item[0]!='{':
			item = '{' + item
		if item[-1]!='}':
			item = item + '}'

		dic = json.loads(item);
		stk_list.append(dic)
		#print  dic["securitycode"], dic["securityshortname"]

#��Ҫ�µ����ӻ�ȡ�����еĸ���
def get_new_stk_from_dfcf2(stk_list):
	h_cook = 'qgqp_b_id=015901ad7a28161a23978a92c401c684; ct=Hix2I46MjD-xnmnI4-FCwZtlm5aiY1FBlVVkT7hOyl0TrTZ23_P-NSbz7tjzNGFcdtZVweKOFhs109FLlfBUIa0XtIl5Q0PXaBV_-B02KIKIODNMb1wdXDJqTn-39GOCfSJexm78mmU_Q6OVkDWXjDUNq5seZcMyJ4x19tU41h4; ut=FobyicMgeV5FJnFT189SwAVHQcnCViDRQ6qT5n733e5mQvT0mDaLePCeFbDolrGSKi3hwCSAahpSz-9o-uWSUURwMsE4COV3J8u-9lNP0B9y_vM8VfNcIoVDJwgTsAAMiS6EDF7G931Ufsf7yna4BxRT8PvpqyDJmEYFVZ6OrR9Qo5wyrY-K3kqmQhEuiZU3blfrQjQtq3sr2o3Q7EhIHKs7XmlceEdFwalMKr56-2Xnoe0NnTxujr_UJj_verPA1EWM4fwxPQgfGyKz4WaqoVu7E1ivgErznh9PHJIi7iGqcobX5hEwIFhkZkReVrho9nwPzSEe4OGVTKMK8n95d9W4pwL49san; pi=6100112247957528;yudingding6197;goutou;n1OcxrtieBSLqyWvw85AOiXce1VZjUBvwowTmZcB8bRYti0XAQXSBHObfm4O12CNyigFTNhD6tcK10sF9Nn6JofAUoFKHyl0hTz+1kRniVtMwwSvAqlj3iRBvcDHwOoECmbgaPXWxnAWHCwB7gM4GN1mi52gb/r0w5IyTc+FNVzViAUmDzo1C5heIlF8EMTnBxX4puWK;tn0B6oPKj3z/+/gTpxkuIxkH18QRRvoHNB0+4sqCss74EDlbalkr0YWYKv114pgEVgiin86M+npAp20XFtlaYZyXfS5mWccW9FW1nM/Y1xYro6+1y90wMu3Nz9uVXcoeTlL7cYWuiJCVthC5xL6Z/nCLncaD1w==; uidal=6100112247957528goutou; sid=4725419; em_hq_fls=js; em-quote-version=topspeed; vtpst=|; intellpositionL=1010.67px; cowminicookie=true; emshistory=["N%E5%92%8C%E9%A1%BA"]; xsb_history=873169|%u4E03%u4E30%u7CBE%u5DE5; HAList=a-sz-300251-%u5149%u7EBF%u4F20%u5A92,a-sz-301187-N%u6B27%u5723,a-sz-301150-C%u4E2D%u4E00,a-sz-002432-%u4E5D%u5B89%u533B%u7597,a-sh-600734-*ST%u5B9E%u8FBE,a-sz-300291-%u534E%u5F55%u767E%u7EB3,a-sz-301237-%u548C%u987A%u79D1%u6280,ty-100-HSI-%u6052%u751F%u6307%u6570,a-sh-600062-%u534E%u6DA6%u53CC%u9E64,a-sz-301109-N%u519B%u4FE1,a-sz-301279-N%u91D1%u9053; cowCookie=true; st_si=50864408522409; intellpositionT=855px; st_asi=delete; JSESSIONID=F410A5363087600D3C0FAB1CDE6D81B6; st_pvi=92457965025484; st_sp=2021-06-14 14:12:01; st_inirUrl=https://passport2.eastmoney.com/pub/login; st_sn=20; st_psi=2022042613062016-111000300841-3806071116'
	url_req = 'https://datacenter-web.eastmoney.com/api/data/v1/get'
	param = "?callback=%s&sortColumns=APPLY_DATE,SECURITY_CODE&sortTypes=-1,-1&pageSize=100&pageNumber=1&reportName=RPTA_APP_IPOAPPLY"
	param2 = "&columns=SECURITY_CODE,SECURITY_NAME,TRADE_MARKET_CODE,APPLY_CODE,TRADE_MARKET,MARKET_TYPE,ORG_TYPE,ISSUE_NUM,ONLINE_ISSUE_NUM,OFFLINE_PLACING_NUM,TOP_APPLY_MARKETCAP,PREDICT_ONFUND_UPPER,ONLINE_APPLY_UPPER,PREDICT_ONAPPLY_UPPER,ISSUE_PRICE,LATELY_PRICE,CLOSE_PRICE,APPLY_DATE,BALLOT_NUM_DATE,BALLOT_PAY_DATE,LISTING_DATE,AFTER_ISSUE_PE,ONLINE_ISSUE_LWR,INITIAL_MULTIPLE,INDUSTRY_PE_NEW,OFFLINE_EP_OBJECT,CONTINUOUS_1WORD_NUM,TOTAL_CHANGE,PROFIT,LIMIT_UP_PRICE,INFO_CODE,OPEN_PRICE,LD_OPEN_PREMIUM,LD_CLOSE_CHANGE,TURNOVERRATE,LD_HIGH_CHANG,LD_AVERAGE_PRICE,OPEN_DATE,OPEN_AVERAGE_PRICE,PREDICT_PE,PREDICT_ISSUE_PRICE2,PREDICT_ISSUE_PRICE,PREDICT_ISSUE_PRICE1,PREDICT_ISSUE_PE,PREDICT_PE_THREE,ONLINE_APPLY_PRICE,MAIN_BUSINESS,PAGE_PREDICT_PRICE1,PAGE_PREDICT_PRICE2,PAGE_PREDICT_PRICE3,PAGE_PREDICT_PE1,PAGE_PREDICT_PE2,PAGE_PREDICT_PE3,SELECT_LISTING_DATE,IS_BEIJING,INDUSTRY_PE_RATIO&quoteColumns=f2~01~SECURITY_CODE~NEWEST_PRICE&filter=(APPLY_DATE%3E%272010-01-01%27)"
	jquery = 'jQuery112302960253986578696_1650945385469'
	send_headers = {
		'Host': 'datacenter-web.eastmoney.com',
		'Connection': 'keep-alive',
		'Cache-Control': 'max-age=0',
		'Upgrade-Insecure-Requests': 1,
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'zh-CN,zh;q=0.9',
		'Cookie': h_cook
	}

	urlfmt = url_req + param
	urlfmt = param % (jquery)
	url = url_req + urlfmt + param2
	#print("get_new_stk_from_dfcf2",url)

	res_data = None
	LOOP_COUNT = 0
	while LOOP_COUNT<3:
		try:
			#����1
			#res_data = urllib2.urlopen(urlall)

			#����2
			req = urllib2.Request(url,headers=send_headers)
			res_data = urllib2.urlopen(req)
		except Exception as e:
			print "Error",sys._getframe().f_code.co_name
			print "Error", e
			LOOP_COUNT = LOOP_COUNT+1
		else:
			break
	if res_data is None:
		print ("Open URL fail",sys._getframe().f_code.co_name)
		return

	content = res_data.read()
	respInfo = res_data.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
		content = zlib.decompress(content, 16+zlib.MAX_WBITS);
	#print content.decode('utf8')
	objs = re.match(jquery+"\((.*)\);", content)
	#objs = re.match(jquery+"\((.*)\);", content.decode('utf8'))
	if objs is None:
		print("Error: format invalid2")
		#print rslt_pre, content[:20]
		return
	#print objs.group(1)
	dicObj = json.loads(objs.group(1))
	for item in dicObj['result']['data']:
		'''
		for key,value in item.items():
			if isinstance(value, unicode):
				print key,value.encode('gbk')
			else:
				print key,value
		print "\n"
		'''
		if item['LISTING_DATE'] is None:
			continue
		
		item['listingdate'] = item['LISTING_DATE'][:10]
		item['securitycode'] = item['SECURITY_CODE']
		item['securityshortname'] = item['SECURITY_NAME']
		if item['CONTINUOUS_1WORD_NUM'] is None:
			item['sl'] = '-'
		else:
			item['sl'] = item['CONTINUOUS_1WORD_NUM']
		item['kb'] = item['CONTINUOUS_1WORD_NUM']
		#print item['securitycode'],item['listingdate'],item['securityshortname'].encode('gbk'),type(item['CONTINUOUS_1WORD_NUM'])
		#print  dic["securitycode"], dic["securityshortname"]
		stk_list.append(item)
	
def getNoOpenYZB(yz_list):
	new_stk_list = []
	desc = u"δ����"
	get_new_stk_from_dfcf(new_stk_list)
	for item in new_stk_list:
		if item["kb"]==desc:
			print "Match", item["securityshortname"]
			yz_list.append(item)
	return
	