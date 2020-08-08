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
	#这个if可能判断多余，强行左右匹配引号里的内容""
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
	#排名	板块名称	相关资讯	最新价	涨跌额	涨跌幅	总市值(亿)	换手率	上涨家数	下跌家数	领涨股票	涨跌幅
	#1	昨日涨停	行情股吧 资金流	9541.65	379.05	4.14%	304	9.66%	9	0	阿石创	10.00%
	#2	国产芯片	行情股吧 资金流	1240.10	30.68	2.54%	4929	2.14%	34	5	聚灿光电	10.03%

	#Flag(0)板块号 板块名称(2)涨幅 总市值 换手率 上涨家数|平盘家数|下跌家数|停牌家数(6),个股代码(7)Flag 个股名称(9)价格 涨幅(11),个股代码(12)Flag 个股名称(14)价格 跌幅(16),Flag 最新值(18)涨跌额(19) 
	#1,BK0891,国产芯片,2.53,493268904578,2.28,35|1|4|1,300708,2,聚灿光电,17.01,10.03,300613,2,富瀚微,206.99,-2.31,3,1239.97,30.55
	#1,BK0706,人脑工程,-0.15,70185675359,0.28,4|1|3|0,300238,2,冠昊生物,24.18,1.00,300244,2,迪安诊断,27.20,-2.30,3,1667.64,-2.57

	#bk 板块
	#lz 领涨
	rank = 0
	strline = u'排名,板块名称,板块涨幅,家数,领涨个股,涨幅,领跌个股,跌幅'
	while 1:
		#通过非贪婪模式进行匹配，关键字'?'
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

#检查是否正在交易，过滤没有交易的
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
# 0: 不过滤，得到所有的
# 1: 只保留正在交易的
# 2: 正在交易的和将要上市还未交易的
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
	#到达最大页面，返回0
	if totalpage==curpage:
		return 0
	return 1

#有一些已经打新还未上市的New
#一些停牌的，一些退市的
#但是它包含退市ZhengLi
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
		print "1Not find matched content at", curpage
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
		#还未上市
		if market_dt=='-':
			continue
		#上市停牌
		if rt_price=='-':
			continue
		#line = array[i][2:]
		#new_st_list.append(line.encode('gbk'))
		new_st_list.append(props)

	#到达最大页面，返回0
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
		print "1Not find matched content at", curpage
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

#sort mode：
#'A' stock code
#'B' 股价
#'C' 涨幅
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

#sort mode：
#'A' stock code
#'B' 股价
#'C' 涨幅
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
"financecode":"37884","companycode":"80975294","securityshortname":"N三峰","securitycode":"601827","subcode":"780827",
"fxzl":378268000.0,"wsfxsl":340442000.0,"applyont":113000.0,"issuepriceMoney":772920.0,"issueprice":6.84,
"purchasedate":"2020-05-21T00:00:00","lwrandate":"2020-05-25T00:00:00","listingdate":"2020-06-05T00:00:00",
"peissuea":22.67,"lwr":0.14984,"cbxjrgbs":246.55989,"sc":"sh",
"mzyqgs":1000.0,"sgzs":65286100000.0,"applyontMoney":1130000.0,"averagelow":10000000.0,
"kb":"未开板",
"zzf":44.0058479532164,"sl":"-","mzyqhl":3010.0,"totaliiqrplaceoff":7539.0,"jg1":6.84,"jg2":6.98,"jg3":6.93,
"pe1":22.67,"pe2":23.16,"pe3":22.99,"bkpe":23.16,"INDUSTRY":"生态保护和环境治理业","Close":9.85,"ChangePercent":44.01,
"ZgsmsOrYxs":"AN202005201379971122","Url":"http://topic.eastmoney.com/cqsfhj/",
"INDUSTRYPE":23.16,"newPrice":9.85,"wszqjkr":"2020-05-25T00:00:00",
"MAINBUSIN":"垃圾焚烧发电项目投资运营、EPC建造以及垃圾焚烧发电核心设备研发制造等",
"ycwssgsx":340000.0,"ycwssgzj":3400000.0,"Update":"2020-06-08 00:09:22","sgrqrow":21.0
'''
#获取当日上市New STK
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
			#方法1
			#res_data = urllib2.urlopen(urlall)

			#方法2
			req = urllib2.Request(url,headers=send_headers)
			res_data = urllib2.urlopen(req)
		except:
			print "Error fupai urlopen"
			LOOP_COUNT = LOOP_COUNT+1
		else:
			break
	if res_data is None:
		print "Open URL fail"
		return

	content = res_data.read()
	objs = re.match(rslt_pre+"={pages:(\d+),data:\[(.*)\]}", content)
	if objs is None:
		print("Error: format invalid")
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
	
def getNoOpenYZB(yz_list):
	new_stk_list = []
	desc = u"未开板"
	get_new_stk_from_dfcf(new_stk_list)
	for item in new_stk_list:
		if item["kb"]==desc:
			print "Match", item["securityshortname"]
			yz_list.append(item)
	return
	