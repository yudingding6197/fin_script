#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import urllib2
import json
import zlib
import random

def http_req(urlall, send_headers1):
	#print (urlall)
	#print (send_headers1)
	filename = 'debug/_html.txt'
	res_data = None
	tf_fl = open(filename, 'w+')
	LOOP_COUNT = 0
	while LOOP_COUNT<3:
		try:
			#方法1
			#res_data = urllib2.urlopen(urlall)

			#方法2
			req = urllib2.Request(urlall,headers=send_headers1)
			res_data = urllib2.urlopen(req, timeout=1)
		except:
			if LOOP_COUNT==2:
				print "Error fupai urlopen"
			LOOP_COUNT = LOOP_COUNT+1
		else:
			break
		
	#print res_data
	if res_data is None:
		print "Open URL fail"
		exit(0)

	content = res_data.read()
	respInfo = res_data.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
		print "Content compressed"
		content = zlib.decompress(content, 16+zlib.MAX_WBITS);
	#else:
	#	print "Content not zip"
	#print content.decode('utf8')

	tf_fl.write(content)


	'''
	line = res_data.readline()
	while line:
		try:
			tf_fl.write(line)
		except:
			#print "?????????????",line.decode('utf8')
			tf_fl.write(line)
		line = res_data.readline()
	'''
	tf_fl.close()


#urlall = "http://quote.eastmoney.com/center/list.html#33"
#urlall = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._A&sty=FCOIATA&sortType=C&sortRule=-1&page=1&pageSize=20&js=var%20quote_123%3d{rank:[(x)],pages:(pc)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.6295543580707108"
#urlall = "http://www.cninfo.com.cn/cninfo-new/disclosure/szse/fulltext"

#这是巨潮网的查询
#url = "http://www.cninfo.com.cn/cninfo-new/memo-2"
#urlall = url + "?queryDate=2017-09-08"

#东财关于概念排行
#urlall = "http://quote.eastmoney.com/center/BKList.html#notion_0_0?sortRule=0"
#urlall = 'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=KZZ_LB&token=70f12f2f4f091e459a279469fe49eca5&cmd=&st=STARTDATE&sr=-1&p=1&ps=50&js=var%20iGeILSKk={pages:(tp),data:(x)}&rt=50463927'
#urlall = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._DEBT_SH_Z&sty=FCOIATA&sortType=C&sortRule=-1&page=1&pageSize=70&js=quote_123{rank:[(x)],pages:(pc)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c'
urlall='http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeDataSimple?page=1&num=80&sort=symbol&asc=1&node=hskzz_z&_s_r_a=page'

# -H "Host: nufm.dfcfw.com" -H "User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0" -H "Accept: */*" 
'''
send_headers = {
'Host':'dcfm.eastmoney.com',
'Connection':'keep-alive',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
'Accept':'*/*',
'DNT': '1',
'Referer': 'http://data.eastmoney.com/kzz/default.html',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.8',
'Cookie': 'st_pvi=33604263703666; emstat_bc_emcount=300285734935048278; pi=6100112247957528%3byudingding6197%3bgoutou%3bcUC1rQLS6GFOJIpJ%2b0I6Wt5AdIat%2bLRj2ZvGrlzeObRNvIHEcy62FDfQ%2boIImkvxiIyCd9QIklChsWI2qjINWL5DdBKYMZ71JGBsgoVjEXYjdw1rWDHu45I%2bNugmP4pbtdgvhUf884FcXhI1tqTCeHOobtdLSzpfA7h3MiSCx5rf8AdOH0uOhUuvYFxLUOx0oD6KGdMI%3bJ7wwpyq2YPDBfbwAqENYGA8GKWnFXYc1dIR5LuUNwKNYfZKtn2ufQSBXaOy%2fJuok5A10Hmp70CM%2bH4jRSUeLe8OOEOwSG5o1tvO4rx%2fTjNoq%2fbM2d6QYkUKtXL0XTX8nREubTh%2bPugiWdGxX3hARJpanE0qULw%3d%3d; uidal=6100112247957528goutou; '
}
'''
#'Connection': 'keep-alive',

'''
send_headers = {
'Host': 'vip.stock.finance.sina.com.cn',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
'Content-type': 'application/x-www-form-urlencoded',
'Accept': '*/*',
'DNT': 1,
'Referer': 'http://vip.stock.finance.sina.com.cn/mkt/',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.8',
'Cookie': 'U_TRS1=0000000e.db0f67d9.58743532.0ab3855e; UOR=www.baidu.com,blog.sina.com.cn,; vjuids=-4f7e5f1b8.15985efc8ab.0.b0009b04a9d3a; SINAGLOBAL=114.243.223.213_1484010803.467733; SGUID=1490330513641_6143460; SCF=ApQZBkYNx5ED9eRh4x7RWZjDJZfZGEsCEcgqoaFHnaP7DqJZQpUkYRbUtwv1spWbrMvv9eU5YBJ8U5RXwjUggcc.; FINA_V_S_2=sz300648,sh603600,sh603987,sz300168,sz300029,sz300033,sz300518,sz002570,sz300609,sh600295,sh600083,sh600846,sz002881,sh603801,sz000916,sz200512,sz002797,sz002342,sz002334,sz000877; vjlast=1504425305; Apache=10.13.240.35_1513310793.422171; U_TRS2=00000016.b8c612f7.5a3398c2.608c14c5; SessionID=oe6kbh7j9v4usqdkigqe4inb71; ULV=1513330875049:56:5:3:10.13.240.35_1513310793.422171:1513225944670; sso_info=v02m6alo5qztbmdlpGpm6adpJqWuaeNo4S5jbKZtZqWkL2Mk5i1jaOktYyDmLOMsMDA; SUB=_2A253Rcj3DeThGedI7lQY9S7KyD-IHXVUMr0_rDV_PUNbm9AKLWTjkW9NVwM9cn_D0fMlGi8-URaLNK3j_mTGomwb; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5.n90RO.U79QHoy5Rk17Op5NHD95QpSo-c1K-7Soe0Ws4Dqcjdi--NiKyFiK.Ni--4i-zpi-ihi--fi-2Xi-zX; ALF=1545792551; rotatecount=2; SR_SEL=1_511; lxlrttp=1513341002; FINANCE2=8d5626b3132364178ca15d9e87dc4f27; SINA_FINANCE=yudingding6197%3A1656950633%3A4'
}
'''

urlall = 'http://market.finance.sina.com.cn/downxls.php?date=2018-01-03&symbol=sz000520'
#Connection: keep-alive
#Upgrade-Insecure-Requests: 1
send_headers = {
'Host': 'market.finance.sina.com.cn',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'DNT': 1,
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.8',
'Cookie': 'U_TRS1=0000000e.db0f67d9.58743532.0ab3855e; UOR=www.baidu.com,blog.sina.com.cn,; vjuids=-4f7e5f1b8.15985efc8ab.0.b0009b04a9d3a; SINAGLOBAL=114.243.223.213_1484010803.467733; \
SGUID=1490330513641_6143460; SCF=ApQZBkYNx5ED9eRh4x7RWZjDJZfZGEsCEcgqoaFHnaP7DqJZQpUkYRbUtwv1spWbrMvv9eU5YBJ8U5RXwjUggcc.; \
vjlast=1504425305; Apache=10.13.240.35_1513310793.422171; U_TRS2=00000016.b8c612f7.5a3398c2.608c14c5; SessionID=oe6kbh7j9v4usqdkigqe4inb71; \
ULV=1513330875049:56:5:3:10.13.240.35_1513310793.422171:1513225944670; sso_info=v02m6alo5qztbmdlpGpm6adpJqWuaeNo4S5jbKZtZqWkL2Mk5i1jaOktYyDmLOMsMDA; \
SUB=_2A253Rcj3DeThGedI7lQY9S7KyD-IHXVUMr0_rDV_PUNbm9AKLWTjkW9NVwM9cn_D0fMlGi8-URaLNK3j_mTGomwb; \
SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5.n90RO.U79QHoy5Rk17Op5NHD95QpSo-c1K-7Soe0Ws4Dqcjdi--NiKyFiK.Ni--4i-zpi-ihi--fi-2Xi-zX; ALF=1545792551; rotatecount=2; SR_SEL=1_511; \
lxlrttp=1513341002; FINANCE2=8d5626b3132364178ca15d9e87dc4f27; SINA_FINANCE=yudingding6197%3A1656950633%3A4'
}

urlall = 'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=KZZ_LB&token=70f12f2f4f091e459a279469fe49eca5&cmd=&st=STARTDATE&sr=-1&p=%d&ps=50&js=iGeILSKk={pages:(tp),data:(x)}&rt=50463927'
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

r1 = random.random()
r2 = random.random()
#r1 = 0.854310854310854310854310122

print (r1, r2)
r3 = float('%.16f' % r1)
s = '%f' % r1
print len(repr(r3))
print repr(r3)

urlall = 'http://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&CATALOGID=1803&TABKEY=tab1&txtQueryDate=2019-08-12&random=0.7978766476031434'
urlall = 'http://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&CATALOGID=1803_sczm&TABKEY=tab1&txtQueryDate=2020-09-15&random=0.4542097358059886'
send_headers = {
'Host': 'www.szse.cn',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': 1,
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
'DNT': 1,
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9'
}

#print urlall

#Main
http_req(urlall, send_headers)

#print random.uniform(0, 1)
#exit(0)

'''
codes = ['601311', '601010', '002437', '600864', '300539', '000810', '600375', '600589', '603083', '600613', '603629', 
'601319', '300278', '000711', '300249', '002600', '300538', '603032', '603000', '300279', '600651', '601608', '300085']
url = 'http://ifzq.gtimg.cn/appstock/app/kline/mkline?param=%s,m5,,60&_var=m5_today&r=%.16f'
send_headers = {
'Host':'ifzq.gtimg.cn',
'Connection':'keep-alive',
'Cache-Control': 'max-age=0',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
'DNT': '1',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.8'
}

for code in codes:
	head3 = code[0:3]
	if head3 in szcd:
		ncode = 'sz' + code
	elif head3 in shcd:
		ncode = 'sh' + code
	f1 = random.uniform(0, 1)
	f2 = random.uniform(0, 1)
	f3 = f1 * f2
	urlall = url % (ncode, f3)
	print urlall
	http_req(urlall, send_headers)
'''