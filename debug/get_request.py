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
urlall = 'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=KZZ_LB&token=70f12f2f4f091e459a279469fe49eca5&cmd=&st=STARTDATE&sr=-1&p=1&ps=50&js=var%20iGeILSKk={pages:(tp),data:(x)}&rt=50463927'

# -H "Host: nufm.dfcfw.com" -H "User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0" -H "Accept: */*" 
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

