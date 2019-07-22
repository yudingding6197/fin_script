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
	while LOOP_COUNT<3:
		url = urlfmt % (st, sr, curpage, ps)
		try:
			req = urllib2.Request(url)
			response = urllib2.urlopen(req, timeout=5)
		except:
			LOOP_COUNT += 1
			print "URL request timeout"
		else:
			break
	if response is None:
		print "Please check data from DongCai at", curpage
		return -1

	line = response.read().decode('utf8')
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
			new_st_list.append(line.encode('gbk'))
		#file.write(line.encode('gbk')+'\n')
	#到达最大页面，返回0
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
	h_cook = 'ct=Wd8LsPKSX4GS_xjlSOJZvruT4PI9GR3gt2rQLJ8B3hlqjyq01uaBZ2LUojlBAQ53vU0_qSelUymwnY2jkPdaekBZ5_VNsfHy_7i6pMr_iFmHIn1afjpnMeqhofTWEyp9kG1zyLfYQhMeBPRnBV4EXnhXF0kLn_HGajqhZ-Q9o7o; ut=FobyicMgeV4n4cCT8MJKZE37stBPqjN_T1jpiNI2KxShGDT9OMc5u5H4SCqNJWDT_7yZqNrfkmeN3oXaqh-yF7miWvRfmTGnJWNNVFmJXZjnR9SpLIFfxO4mNFb4Muh-xozldZpLYwxyBu9RhdRK6-1kXYtkDGiDBXyTwHeXm4pM5bganDOsHMwglOtE6c6xO6Sxrdj8YMRSXUQdvkllsID-huvJxoZ0tusDR_mWZFAuv3c3SNYTYvotOCsIT1F-aTJGxQAQCJa7CO4uHTGZ-3mks9f8rULR; pi=6100112247957528%3byudingding6197%3bgoutou%3b283EZdd5z5lQfTnO2gF0ZVyBR2zzuQuo%2fLPNyPlaznbUmz%2fWtlecMvB9TcBTZ%2bnKg%2fCTmncBYYbtNW9xnnrXvswAZc6f7nFYBZDoxaCSZllecYH7UmH0NDIBDxZl2blrRXdscWTySYdf97j1O8P6VDutXoeH0JgAt3R7AhylQ7BGGpk6MjwKZdwyKWVLOA537qon9dSz%3biulYPcLYFBPQN35d7nhEnaUqfDrVTmA%2bhu2rTIEFmw3BnDZcZ0zjYDiTbckOQogOMaybaQambDU6CYnh2irQuEFMw3%2bDyE0UL0m4NJT3b6EiB%2fgiSrVEz7ke4h%2fV1xV9cGQjJ%2fcLxyRX6JJecVodDWY3pansLA%3d%3d; uidal=6100112247957528goutou; sid=4725419; vtpst=|; em_hq_fls=js; em-quote-version=topspeed; qgqp_b_id=b6a15eaf1e20abfbc9ee2d393164f4eb; HAList=a-sz-300291-%u534E%u5F55%u767E%u7EB3%2Ca-sz-000423-%u4E1C%u963F%u963F%u80F6%2Ca-sh-603738-%u6CF0%u6676%u79D1%u6280%2Ca-sh-603444-%u5409%u6BD4%u7279; st_si=29065711420899; st_asi=delete; emshistory=%5B%22%E4%BC%9A%E7%A8%BD%E5%B1%B1%22%2C%22%E7%B2%BE%E5%B7%A5%E9%92%A2%E6%9E%84%22%2C%22%E8%82%A1%E6%B5%B7%E7%89%A7%E7%AB%A5%22%5D; st_pvi=50425195960510; st_sp=2019-04-02%2021%3A53%3A59; st_inirUrl=http%3A%2F%2Fstock.eastmoney.com%2Fnews%2Fcbktt.html; st_sn=25; st_psi=20190723002552921-113200301712-1042590200'
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
		#方法1
		#res_data = urllib2.urlopen(urlall)

		#方法2
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
	#先匹配左右(),去掉括号,再匹配括号内内容
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
