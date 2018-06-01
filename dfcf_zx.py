#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import re
import urllib2
import json
import zlib
import pandas as pd
import numpy as np

command = 'cmd='+'0026072,3000622,6033651'
prestr = 'getStockFullInfo'
urlall = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?ps=500&token=580f8e855db9d9de7cb332b3990b61a3&type=CT&'+ command +'&\
sty=CTALL&cb='+ prestr +'&js=[(x)]&0.7330375684596748'

send_headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'DNT': 1,
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.8'
}

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

print res_data
if res_data is None:
	print "Open URL fail"
	exit(0)

content = res_data.read()
respInfo = res_data.info()
if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
	print "Content compressed"
	content = zlib.decompress(content, 16+zlib.MAX_WBITS);
else:
	print "Content not zip"

obj = re.match(r'^'+ prestr +'(.*)', content)
stkobj = json.loads(obj.group(1))

df = pd.DataFrame()
print df
line = []
column=['']
act_col = [0,1,2,4,7,9]
col_name = []
for item in stkobj:
	line_arr = item.split(',')
	line.append(line_arr)
df = pd.DataFrame(line)

print df

