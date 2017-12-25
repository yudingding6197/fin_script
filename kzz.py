#!/usr/bin/env python
# -*- coding:gbk -*-
#可转债
import sys
import re
import urllib2
import datetime
import zlib
import pandas as pd
from internal.dfcf_interface import *

'''
urlall = "http://data.eastmoney.com/kzz/default.html"

http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=KZZ_LB&token=70f12f2f4f091e459a279469fe49eca5&cmd=&st=STARTDATE&sr=-1&p=2&ps=50&js=var%20fnhOGnNf={pages:(tp),data:(x)}&rt=50462432
curl 'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=KZZ_LB&token=70f12f2f4f091e459a279469fe49eca5&cmd=&st=STARTDATE&sr=-1&p=2&ps=50&js=var%20ShTNyQGa=\{pages:(tp),data:(x)\}&rt=50462435' -H 'Referer: http://data.eastmoney.com/kzz/default.html' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2986.0 Safari/537.36' --compressed ;
curl 'http://datapic.eastmoney.com/img/loading.gif' -H 'Referer: http://data.eastmoney.com/kzz/default.html' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2986.0 Safari/537.36' --compressed
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
'Cookie': 'st_pvi=33604263703666; emstat_bc_emcount=300285734935048278; pi=6100112247957528%3byudingding6197%3bgoutou%3bcUC1rQLS6GFOJIpJ%2b0I6Wt5AdIat%2bLRj2ZvGrlzeObRNvIHEcy62FDfQ%2boIImkvxiIyCd9QIklChsWI2qjINWL5DdBKYMZ71JGBsgoVjEXYjdw1rWDHu45I%2bNugmP4pbtdgvhUf884FcXhI1tqTCeHOobtdLSzpfA7h3MiSCx5rf8AdOH0uOhUuvYFxLUOx0oD6KGdMI%3bJ7wwpyq2YPDBfbwAqENYGA8GKWnFXYc1dIR5LuUNwKNYfZKtn2ufQSBXaOy%2fJuok5A10Hmp70CM%2bH4jRSUeLe8OOEOwSG5o1tvO4rx%2fTjNoq%2fbM2d6QYkUKtXL0XTX8nREubTh%2bPugiWdGxX3hARJpanE0qULw%3d%3d; uidal=6100112247957528goutou; vtpst=|; '
}

rturl = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._DEBT_%s_Z&sty=FCOIATA&sortType=C&sortRule=-1&page=%d&pageSize=80&js=quote_123={rank:[(x)],pages:(pc)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c'
rturl = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._DEBT_%s_Z&sty=FCOIATA&sortType=C&sortRule=-1&page=%d&pageSize=80&js=quote_123={rank:[(x)],pages:(pc)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c'
rt_headers = {
'Host': 'nufm.dfcfw.com',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
'Accept': '*/*',
'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
'Accept-Encoding': 'gzip, deflate',
'Referer': 'http://quote.eastmoney.com/center/list.html',
'DNT': '1'
}

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

def getKZZRt(market, page):
	global content
	LOOP_COUNT=0
	urllink = rturl % (market, page)
	res_data = None
	while LOOP_COUNT<3:
		try:
			#print urllink
			req = urllib2.Request(urllink,headers=rt_headers)
			res_data = urllib2.urlopen(req)
		except:
			print "Exception kzz urlopen"
			LOOP_COUNT += 1
		else:
			break
	#print res_data
	if res_data is None:
		print "Error: Fail to get request"
		content = ''
		return
	content = res_data.read()
	respInfo = res_data.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")) :
		content = zlib.decompress(content, 16+zlib.MAX_WBITS);
	print content.decode('utf8')
	#content = res_data.read().decode('gbk')
	#print content[:2]
	return

#['BONDCODE','SNAME','ZQNEW','YJL','ZGJZGJJZ','ZGJ_HQ','SWAPSCODE','SECURITYSHORTNAME','ZGJZGJ']
def output(kdf):
	fmt = "%2d %6s %8s	%5.2f	%5.2f	%5.2f	%5.2f	%5.2f"
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

		ZQNEW = (float(items['ZQNEW']))
		YJL = float(items['YJL'])
		ZGJZ = float(items['ZGJZGJJZ'])
		ZGJ_HQ = float(items['ZGJ_HQ'])
		ZGJZGJ = float(items['ZGJZGJ'])
		str = fmt % (rank+1, items[0],items[1],ZQNEW,YJL,ZGJZ,ZGJ_HQ,ZGJZGJ)
		rank += 1
		print str
	return

getKZZRt('SH', 1)
getKZZRt('SZ', 1)
exit()

#Main
if __name__=="__main__":
	req_count=0
	curpage = 1
	dfkzz = None
	kzzlist = []
	content=''
	totalpage = 0
	while 1:
		req_count += 1
		if req_count>10:
			break

		getKZZConnect(curpage)
		if content=='':
			break
		dataObj = re.match('^iGeILSKk={pages:(\d+),data:\[(.*)\]}', content)
		if dataObj is None:
			print "Content format not match"
			break
		if totalpage < 1:
			totalpage = int(dataObj.group(1))
		if curpage>totalpage:
			break
		curpage += 1
		#分析具体的每一项数据
		getFilterZhai(dataObj.group(2), 1, kzzlist)
		#print curpage, totalpage
		#break

	if len(kzzlist)==0:
		print "Not find data"
		exit()
	print datetime.datetime.now()
	keylist = ["STARTDATE", "QSCFJ", "TEXCH", "AISSUEVOL", "ISSUEPRICE", "DELISTDATE",
	"BCODE", "SWAPSCODE", "CORRESNAME", "BONDCODE", "PB", "SNAME", "PARVALUE", "MarketType",
	"LISTDATE", "HSCFJ", "SECURITYSHORTNAME", "GDYX_STARTDATE", "LUCKRATE", "ZGJZGJJZ",
	"LIMITBUYIPUB", "MEMO", "ZGJ", "ZQHDATE", "YJL", "FSTPLACVALPERSTK", "ZQNEW",
	"CORRESCODE", "SWAPPRICE", "ZGJ_HQ", "ZGJZGJ"]
	keylist = ['BONDCODE','SNAME','ZQNEW','YJL','ZGJZGJJZ','ZGJ_HQ','SWAPSCODE','SECURITYSHORTNAME','ZGJZGJ']

	kzzdf = pd.DataFrame(kzzlist, columns=keylist)
	output(kzzdf)
	#print kzzdf
