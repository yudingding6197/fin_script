#!/usr/bin/env python
# -*- coding:gbk -*-
#可转债
import sys
import re
import urllib2
import time
import datetime
import zlib
import json
import getopt
import pickle
import pandas as pd
sys.path.append(".")
sys.path.append("..")
from internal.dfcf_inf import *

'''
urlall = "http://data.eastmoney.com/kzz/default.html"

==========
[STARTDATE]='2017-12-04T00:00:00'		申购日期
[QSCFJ]='7.31'				强赎触发价
[TEXCH]='CNSESZ'			交易所代码
[AISSUEVOL]='10.0'			发行规模
[ISSUEPRICE]='100.0'		发行价
[DELISTDATE]='-'			摘牌日期
[BCODE]='17270600001JBV'	？？编码
[SWAPSCODE]='002284'		正股代码
[CORRESNAME]='亚太发债'		债券发行名称
[BONDCODE]='128023'			债券代码
[PB]='2.36'					PB
[SNAME]='亚太转债'			债券名称
[PARVALUE]='100.0'			？？
[MarketType]='2'			市场类型 1：上交，2：深交
[LISTDATE]='2017-12-26T00:00:00'		上市交易日期
[HSCFJ]='13.57'				回售触发价
[SECURITYSHORTNAME]='亚太股份'			正股名称
[GDYX_STARTDATE]='2017-12-01T00:00:00'	股权登记日
[LUCKRATE]='0.0245376003'	中签率
[ZGJZGJJZ]='81.6091954023'	当前转股价值
[LIMITBUYIPUB]='100.0'		最大申购上限
[MEMO]=''					备注
[ZGJ]='8.52'				转股价
[ZQHDATE]='2017-12-06T00:00:00'			中签号发布日
[YJL]='22.5352112676'		溢价率
[FSTPLACVALPERSTK]='1.3558'	每股配售额
[ZQNEW]='100.0'				债券最新价格
[CORRESCODE]='072284'		申购代码
[SWAPPRICE]='10.44'			？？初始转股价
[ZGJ_HQ]='8.52'				正股价
[ZGJZGJ]='10.44'			当前转股价
'''

urlfmt = 'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=KZZ_LB&token=70f12f2f4f091e459a279469fe49eca5&cmd=&st=STARTDATE&sr=-1&p=%d&ps=50&js=iGeILSKk={pages:(tp),data:(x)}&rt=50463927'
send_headers = {
'Host':'dcfm.eastmoney.com',
'Connection':'keep-alive',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
'Accept':'*/*',
'DNT': '1',
'Referer': 'http://data.eastmoney.com/kzz/default.html',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.8',
'Cookie': 'st_pvi=33604263703666; emstat_bc_emcount=300285734935048278; \
pi=6100112247957528%3byudingding6197%3bgoutou%3bcUC1rQLS6GFOJIpJ%2b0I6Wt5AdIat%2bLRj2ZvGrlzeObRNvIHEcy62FDfQ%2boIImkvxiIyCd9QIklChsWI2qjINWL\
5DdBKYMZ71JGBsgoVjEXYjdw1rWDHu45I%2bNugmP4pbtdgvhUf884FcXhI1tqTCeHOobtdLSzpfA7h3MiSCx5rf8AdOH0uOhUuvYFxLUOx0oD6KGdMI%3bJ7wwpyq2YPDBfbw\
AqENYGA8GKWnFXYc1dIR5LuUNwKNYfZKtn2ufQSBXaOy%2fJuok5A10Hmp70CM%2bH4jRSUeLe8OOEOwSG5o1tvO4rx%2fTjNoq%2fbM2d6QYkUKtXL0XTX8nREubTh%2bPugi\
WdGxX3hARJpanE0qULw%3d%3d; \
uidal=6100112247957528goutou; vtpst=|; '
}

rturl = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeDataSimple?page=%d&num=80&sort=symbol&asc=1&node=hskzz_z&_s_r_a=page'
rt_headers = {
'Host': 'vip.stock.finance.sina.com.cn',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
'Content-type': 'application/x-www-form-urlencoded',
'Accept': '*/*',
'DNT': 1,
'Referer': 'http://vip.stock.finance.sina.com.cn/mkt/',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.8',
'Cookie': 'U_TRS1=0000000e.db0f67d9.58743532.0ab3855e; UOR=www.baidu.com,blog.sina.com.cn,; vjuids=-4f7e5f1b8.15985efc8ab.0.b0009b04a9d3a; \
SINAGLOBAL=114.243.223.213_1484010803.467733; SGUID=1490330513641_6143460; \
SCF=ApQZBkYNx5ED9eRh4x7RWZjDJZfZGEsCEcgqoaFHnaP7DqJZQpUkYRbUtwv1spWbrMvv9eU5YBJ8U5RXwjUggcc.; \
FINA_V_S_2=sz300648,sh603600; vjlast=1504425305; Apache=10.13.240.35_1513310793.422171; U_TRS2=00000016.b8c612f7.5a3398c2.608c14c5; \
SessionID=oe6kbh7j9v4usqdkigqe4inb71; ULV=1513330875049:56:5:3:10.13.240.35_1513310793.422171:1513225944670; \
sso_info=v02m6alo5qztbmdlpGpm6adpJqWuaeNo4S5jbKZtZqWkL2Mk5i1jaOktYyDmLOMsMDA; \
SUB=_2A253Rcj3DeThGedI7lQY9S7KyD-IHXVUMr0_rDV_PUNbm9AKLWTjkW9NVwM9cn_D0fMlGi8-URaLNK3j_mTGomwb; \
SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5.n90RO.U79QHoy5Rk17Op5NHD95QpSo-c1K-7Soe0Ws4Dqcjdi--NiKyFiK.Ni--4i-zpi-ihi--fi-2Xi-zX; \
ALF=1545792551; rotatecount=2; SR_SEL=1_511; lxlrttp=1513341002; FINANCE2=8d5626b3132364178ca15d9e87dc4f27; \
SINA_FINANCE=yudingding6197%3A1656950633%3A4'
}

'''
def getKZZConnect(page):
	global content
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
		content = ''
		return
	content = res_data.read().decode('utf8')
	return
'''

#得到交易日KZZ的实时价格
def getKZZRtSinaByPage(list, page):
	global content
	LOOP_COUNT=0
	urllink = rturl % (page)
	res_data = None
	while LOOP_COUNT<3:
		try:
			#print urllink
			req = urllib2.Request(urllink,headers=rt_headers)
			res_data = urllib2.urlopen(req)
		except:
			if LOOP_COUNT==1:
				print "Exception kzz urlopen"
				print urllink
			time.sleep(0.5)
			LOOP_COUNT += 1
		else:
			break
	#print ("res_data", res_data)
	if res_data is None:
		print "Error: Fail to get request"
		content = ''
		return 'error'
	content = res_data.read()
	respInfo = res_data.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")) :
		content = zlib.decompress(content, 16+zlib.MAX_WBITS);
	#print (content)
	if content=='null':
		return content
	if len(content)<=2:
		content = ''
		return 'error'

	if content[0]=='[' and content[-1]==']':
		content = content [1:-1]

	# 'settlement'是昨收
	conv_clmn=['changepercent','trade','pricechange','open','high','low','settlement']
	while 1:
		obj = re.match(r'{(.*?)},?(.*)', content)
		if obj is None:
			break
		record = obj.group(1)
		#print record
		content = obj.group(2)
		dict = {}
		ll = record.split(',')
		for item in ll:
			#第二项表示非"字符进行匹配
			dictObj = re.match(r'(.*?):"?([^"]*)', item)
			if dictObj is None:
				print "Invalid item in dict", item
				break
			#将symbol前面的sh or sz 去掉
			if dictObj.group(1)=='symbol':
				dict[dictObj.group(1)] = dictObj.group(2)[2:]
			#将涨跌百分比强转float
			elif dictObj.group(1) in conv_clmn:
				dict[dictObj.group(1)] = float(dictObj.group(2))
			else:
				dict[dictObj.group(1)] = dictObj.group(2)
		list.append(dict)
	return 'ok'
def getKZZRtSina(list):
	for page in range(1,10):
		ret = getKZZRtSinaByPage(list, page)
		if ret=='null':
			break

#['BONDCODE','SNAME','ZQNEW','YJL','ZGJZGJJZ','ZGJ_HQ','SWAPSCODE','SECURITYSHORTNAME','ZGJZGJ']
def output(kdf):
	fmt = u"%2d %6s %8s	%8s   %5.2f	%5.2f	%5.2f	%5.2f"
	df = kdf.sort_values(['YJL'],0,True)
	rank = 0
	for index,items in df.iterrows():
		value=items[1]
		nmlen=len(items[1].encode('gbk'))
		if nmlen<8:
			left=8-nmlen
			while left>0:
				value=' '+value
				left-=1

		ZQNEW = items['ZQNEW']
		YJL = float(items['YJL'])
		ZGJZ = float(items['ZGJZGJJZ'])
		ZGJ_HQ = float(items['ZGJ_HQ'])
		ZGJZGJ = float(items['ZGJZGJ'])

		str = fmt % (rank+1, items[0],items[1],ZQNEW,YJL,ZGJZ,ZGJ_HQ,ZGJZGJ)
		rank += 1
		print str
	return

def show_item(rank, items):
	fmt = "%2d %6s %8s	%5.2f	%5.2f	%5.2f	%5.2f	%5.2f	%5.2f	%5.2f"
	if items is not None:
		value=items['name']
		nmlen=len(value)
		if nmlen<8:
			left=8-nmlen
			while left>0:
				value=' '+value
				left-=1

		code = items['code']
		cp = items['changepercent']
		trade = items['trade']
		open = items['open']
		high = items['high']
		low = items['low']
		z_close = items['settlement']
		open_p = (open-z_close)*100/z_close
		high_p = (high-z_close)*100/z_close
		low_p = (low-z_close)*100/z_close
		if high==0:
			open_p = 0
			high_p = 0
			low_p = 0
		YJL = (items['YJL'])
		ZGJZ = (items['ZGJZGJJZ'])
		if trade==0:
			str = fmt % (rank, code, value.decode('gbk'), cp,trade,open,high,low,YJL,ZGJZ)
		else:
			str = fmt % (rank, code, value.decode('gbk'), cp,trade,open_p,high_p,low_p,YJL,ZGJZ)
		print str

def output_rank(mgdf, priority):
	fmt = "   %6s %8s      %-7s	%-7s	%-7s	%-7s	%-7s	%-7s	%-7s"
	print fmt%('code', 'name', 'change', 'price', 'open', 'high', 'low', 'YJL', 'ZGJZ')

	flag = False
	sortitem = 'changepercent'
	if param_config['Daoxu']==1:
		flag = True
	if param_config['Price']==1:
		sortitem = 'trade'
	elif param_config['YJL']==1:
		sortitem = 'YJL'
	elif param_config['ZGJZ']==1:
		sortitem = 'ZGJZGJJZ'
	#df = mgdf.sort_values([sortitem],0, flag)
	rank = 0
	#for code in priority:
		#print code
	#	items = df.ix[code]
		#print items
	#	show_item(rank, items)
	print '=================================================='
	print ''
	for index,items in df.iterrows():
		if param_config['ALL']==0 and rank>21:
			break
		rank += 1
		show_item(rank, items)
	return

def readKZZDataFrame(df, kzzlist):
	req_count=0
	curpage = 1
	totalpage = 0
	while 1:
		req_count += 1
		if req_count>10:
			break

		content = getKZZConnect(urlfmt, send_headers, curpage)

def getKZZDataFrame(kzzlist):
	req_count=0
	curpage = 1
	totalpage = 0
	str1 = ''
	while 1:
		req_count += 1
		if req_count>1:
			#print("Read page greater than 20")
			break

		content = getKZZConnect(urlfmt, send_headers, curpage)
		#print(content.encode('gbk'))
		if content=='':
			break
		dataObj = re.match('^iGeILSKk={pages:(\d+),data:\[(.*)\]}', content)
		if dataObj is None:
			print "Content format not match"
			break
		if totalpage < 1:
			totalpage = int(dataObj.group(1))
		if curpage>totalpage:
			#print("current page(%d) greater than total page(%d)" % (curpage, totalpage))
			break
		curpage += 1

		#print(dataObj.group(2))
		if str1 == '':
			str1 = dataObj.group(2)
		else:
			str1 += ',' + dataObj.group(2)
		#str = "[" + dataObj.group(2) + "]"
		#page_df = pd.read_json(str)

		#print(page_df)
		#df = df.append(page_df)

		#分析具体的每一项数据
		getFilterZhai(dataObj.group(2), 1, kzzlist)
		#print curpage, totalpage
		#break
	str1 = "[" + str1 + "]"
	df = pd.read_json(str1)
	return df

kzz_file = "a.df.csv"
param_config = {
	"Daoxu":0,
	"Placement":0,
	"YJL":0,
	"ZGJZ":0,
	"ALL":0
}

#Main
if __name__=="__main__":
	#倒序，价格，溢价率
	optlist, args = getopt.getopt(sys.argv[1:], 'dpyza')
	for option, value in optlist:
		if option in ["-d","--daoxu"]:
			param_config["Daoxu"] = 1
		#配售数量
		elif option in ["-p","--placement"]:
			param_config["Placement"] = 1
		elif option in ["-y","--yjl"]:
			param_config["YJL"] = 1
		elif option in ["-z","--zgjz"]:
			param_config["ZGJZ"] = 1
		elif option in ["-a","--all"]:
			param_config["ALL"] = 1
	pass

	#pd.set_option('display.max_columns', None)
	priority = []
	'''
	flag = 0
	data_path = "debug/_self_define.txt"
	file = open(data_path, 'r')
	while 1:
		lines = file.readlines(100000)
		if not lines:
			break
		for line in lines:
			line=line.strip()
			if line=='KZZ':
				flag=1
				continue
			elif flag==1 and line=='END':
				break
			if flag==0:
				continue
			code=line.strip()
			if len(code)!=6:
				continue;
			if not code.isdigit():
				continue;
			priority.append(code)
	file.close()
	'''

	#kzzdf = pd.DataFrame()
	kzzlist = []
	kzzdf = getKZZDataFrame(kzzlist)

	if len(kzzlist)==0:
		print "Not find data"
		exit()

	#print(kzzdf)
	#kzzdf.to_csv(kzz_file, encoding='gbk')

	#正股价 'ZGJ'
	#每股配股价 'FSTPLACVALPERSTK'
	#正股价转股价价值 'ZGJZGJJZ'
	#可换购数量 'PURS'
	
	df = kzzdf[kzzdf['LISTDATE']=='-']
	new_col = 'PURS'
	df[new_col] = df.apply(lambda x: 10000/x['ZGJ'] * x['FSTPLACVALPERSTK'], axis=1)

	keylist = ['BONDCODE','SNAME','ZGJ','ZGJZGJJZ','ZGJZGJ',new_col]
	df1 = df[keylist]
	
	#print(df1)
	priority = []
	output_rank(mgdf, priority)

	#i = 0
	#for index, row in df1.iterrows():
	#	i += 1
	#	print(i, row)
	
	#print(datetime.datetime.now())
	#print(kzzlist)
	#print (str(kzzlist).replace('u\'','\'').decode("unicode-escape"))
	
	'''
	keylist = ["STARTDATE", "QSCFJ", "TEXCH", "AISSUEVOL", "ISSUEPRICE", "DELISTDATE",
	"BCODE", "SWAPSCODE", "CORRESNAME", "BONDCODE", "PB", "SNAME", "PARVALUE", "MarketType",
	"LISTDATE", "HSCFJ", "SECURITYSHORTNAME", "GDYX_STARTDATE", "LUCKRATE", "ZGJZGJJZ",
	"LIMITBUYIPUB", "MEMO", "ZGJ", "ZQHDATE", "YJL", "FSTPLACVALPERSTK", "ZQNEW",
	"CORRESCODE", "SWAPPRICE", "ZGJ_HQ", "ZGJZGJ"]
	keylist = ['BONDCODE','SNAME','ZQNEW','YJL','ZGJZGJJZ','ZGJ_HQ','SWAPSCODE','SECURITYSHORTNAME','ZGJZGJ']
	kzzdf = pd.DataFrame(kzzlist, columns=keylist)
	kzzdf1 = kzzdf.set_index('BONDCODE')

	sinakey = ['sell', 'volume', 'buy', 'name', 'ticktime', 'symbol', 'pricechange', 'changepercent', 'trade', 'high', 'amount','code', 'low', 'settlement', 'open']
	sina_rt = []
	getKZZRtSina(sina_rt)
	if len(sina_rt)==0:
		print "Get Sina KZZ fail"
		exit()
	sinadf=pd.DataFrame(sina_rt, columns=sinakey)
	sinadf=sinadf.set_index('symbol')

	#直接合并2个dataFrame，根据索引合并
	mgdf = pd.merge(sinadf, kzzdf1, how='left', left_index=True, right_index=True)

	#output(kzzdf)
#	for indexs in kzzdf.index:
#		print(kzzdf.loc[indexs].values[0:-1])
	output_rank(mgdf, priority)
	'''
