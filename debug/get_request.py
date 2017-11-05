#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import urllib2
import json
from bs4 import BeautifulSoup

#urlall = "http://quote.eastmoney.com/center/list.html#33"
#urlall = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._A&sty=FCOIATA&sortType=C&sortRule=-1&page=1&pageSize=20&js=var%20quote_123%3d{rank:[(x)],pages:(pc)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.6295543580707108"
#urlall = "http://www.cninfo.com.cn/cninfo-new/disclosure/szse/fulltext"

#这是巨潮网的查询
#url = "http://www.cninfo.com.cn/cninfo-new/memo-2"
#urlall = url + "?queryDate=2017-09-08"

#东财关于概念排行
#urlall = "http://quote.eastmoney.com/center/BKList.html#notion_0_0?sortRule=0"
urlall = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._BKGN&sty=FPGBKI&st=c&sr=-1&p=1&ps=5000&cb=&token=7bc05d0d4c3c22ef9fca8c2a912d779c&v=0.2694706493189898"
# -H "Host: nufm.dfcfw.com" -H "User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0" -H "Accept: */*" 
#-H "Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3" --compressed -H "Referer: http://quote.eastmoney.com/center/BKList.html" -H "DNT: 1" -H "Connection: keep-alive""
send_headers = {
 'Host':'nufm.dfcfw.com',
 'User-Agent':'User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
 'Accept':'*/*',
 'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
 'DNT':'1',
 'Connection':'keep-alive'
}
#print urlall

filename = 'debug/_html.txt'

res_data = None
tf_fl = open(filename, 'w+')
try:
	#方法1
	#res_data = urllib2.urlopen(urlall)

	#方法2
	req = urllib2.Request(urlall,headers=send_headers)
	res_data = urllib2.urlopen(req)
except:
	print "Error fupai urlopen"
	#LOOP_COUNT = LOOP_COUNT+1

print res_data
if res_data is None:
	print "Open URL fail"
	exit(0)

content = res_data.read()
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

