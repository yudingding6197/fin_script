#!/usr/bin/env python
# -*- coding:gbk -*-
#可转债
import sys
import re
import urllib2
import datetime
import zlib
import json
import getopt
import pandas as pd
sys.path.append(".")
sys.path.append("..")
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
'Cookie': 'st_pvi=33604263703666; emstat_bc_emcount=300285734935048278; \
pi=6100112247957528%3byudingding6197%3bgoutou%3bcUC1rQLS6GFOJIpJ%2b0I6Wt5AdIat%2bLRj2ZvGrlzeObRNvIHEcy62FDfQ%2boIImkvxiIyCd9QIklChsWI2qjINWL\
5DdBKYMZ71JGBsgoVjEXYjdw1rWDHu45I%2bNugmP4pbtdgvhUf884FcXhI1tqTCeHOobtdLSzpfA7h3MiSCx5rf8AdOH0uOhUuvYFxLUOx0oD6KGdMI%3bJ7wwpyq2YPDBfbw\
AqENYGA8GKWnFXYc1dIR5LuUNwKNYfZKtn2ufQSBXaOy%2fJuok5A10Hmp70CM%2bH4jRSUeLe8OOEOwSG5o1tvO4rx%2fTjNoq%2fbM2d6QYkUKtXL0XTX8nREubTh%2bPugi\
WdGxX3hARJpanE0qULw%3d%3d; \
uidal=6100112247957528goutou; vtpst=|; '
}

def export_ebk(kdf):
	kzzebk = "../data/kzz.EBK"
	file = open(kzzebk, 'w')
	for index,items in kdf.iterrows():
		code = items[0]
		str = ''
		if code[:2]=='11':
			str = '1%s\n'%(code)
		elif code[:2]=='12':
			str = '0%s\n'%(code)
		if str!='':
			file.write(str)
	file.close()
	return

#Main
if __name__=="__main__":
	req_count=0
	curpage = 1
	kzzlist = []
	content=''
	totalpage = 0
	while 1:
		req_count += 1
		if req_count>10:
			break

		content = getKZZConnect(urlfmt, send_headers, curpage)
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

	keylist = ['BONDCODE','SNAME','ZQNEW','YJL','ZGJZGJJZ','ZGJ_HQ','SWAPSCODE','SECURITYSHORTNAME','ZGJZGJ']
	kzzdf = pd.DataFrame(kzzlist, columns=keylist)
	export_ebk(kzzdf)
