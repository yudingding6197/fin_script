#!/usr/bin/env python
# -*- coding:gbk -*-
#可转债
import sys
import re
import os
import string
import urllib
import urllib2
import datetime
import binascii
import shutil
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook
from internal.common import *
from internal.ts_common import *

'''
urlall = "http://data.eastmoney.com/kzz/default.html"

http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=KZZ_LB&token=70f12f2f4f091e459a279469fe49eca5&cmd=&st=STARTDATE&sr=-1&p=2&ps=50&js=var%20fnhOGnNf={pages:(tp),data:(x)}&rt=50462432
curl 'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=KZZ_LB&token=70f12f2f4f091e459a279469fe49eca5&cmd=&st=STARTDATE&sr=-1&p=2&ps=50&js=var%20ShTNyQGa=\{pages:(tp),data:(x)\}&rt=50462435' -H 'Referer: http://data.eastmoney.com/kzz/default.html' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2986.0 Safari/537.36' --compressed ;
curl 'http://datapic.eastmoney.com/img/loading.gif' -H 'Referer: http://data.eastmoney.com/kzz/default.html' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2986.0 Safari/537.36' --compressed
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

#Main
content=''
totalpage = 1
def getKZZConnect(page):
	global content
	LOOP_COUNT=0
	urllink = urlfmt % (page)
	res_data = None
	while LOOP_COUNT<3:
		try:
			print urllink
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

if __name__=="__main__":
	req_count=0
	curpage = 1
	while 1:
		req_count += 1
		if req_count>10:
			break
		if curpage>totalpage:
			break

		getKZZConnect(curpage)
		print content[:64]
		if content=='':
			break
		dataObj = re.match('^iGeILSKk={pages:(\d+),data:\[(.*)\]}', content)
		if dataObj is None:
			print "Content format not match"
			break
		if totalpage < 1:
			totalpage = int(dataObj.group(1))
		curpage += 1
