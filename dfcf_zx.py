#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import re
import urllib2
import json
import zlib
import getopt
import pandas as pd
import numpy as np
from internal.dfcf_inf import *

def getStockObjects(command):
	head = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?ps=500&token=580f8e855db9d9de7cb332b3990b61a3&type=CT&'
	prestr = 'getStockFullInfo'
	urlall = head + command +'&sty=CTALL&cb='+ prestr +'&js=[(x)]&0.7330375684596748'

	send_headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'DNT': 1,
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.8'
	}

	res_data = None
	try:
		req = urllib2.Request(urlall,headers=send_headers)
		res_data = urllib2.urlopen(req)
	except:
		print "Error",sys._getframe().f_code.co_name

	if res_data is None:
		print ("Open URL fail",sys._getframe().f_code.co_name)
		return None

	content = res_data.read()
	respInfo = res_data.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
		#print "Content compressed"
		content = zlib.decompress(content, 16+zlib.MAX_WBITS);
	else:
		#print "Content not zip"
		pass

	#print content
	obj = re.match(r'^'+ prestr +'(.*)', content)
	#print obj.group(1)
	object = json.loads(obj.group(1))
	return object

#Main Start
param_config = {
	"Code":0,
	"Name":0,
	"Range":0,
	"Price":0,
	"Title":0,
}

optlist, args = getopt.getopt(sys.argv[1:], 'cnrpt')
for option, value in optlist:
	if option in ["-c","--code"]:
		param_config["Code"] = 1
	elif option in ["-n","--name"]:
		param_config["Name"] = 1
	elif option in ["-r","--range"]:
		param_config["Range"] = 1
	elif option in ["-p","--price"]:
		param_config["Price"] = 1
	elif option in ["-t","--title"]:
		param_config["Title"] = 1
#print param_config

command = 'cmd='
#command = 'cmd='+'0026072,3000622,6033651'
#print command

#首先得到自选股
stock_array = []
getSelfDefStock(stock_array)
if len(stock_array)==0:
	print "Fail to get self defined from DFCF"
	exit()
self_code = ','.join(i[:6] + i[8:9] for i in stock_array)
command += self_code

#得到自选股的所有信息
stkobj = getStockObjects(command)
#print stkobj

#0       1        2        3        4        5        6        7        8        9
column_name = [\
'市场',  '代码',  '名称',  '最新价','涨跌幅','涨跌额','总手',  '现手',  '买入价','卖出价',\
'涨速',  '换手',  '金额',  '市盈率','最高',  '最低',  '开盘',  '昨收',  '振幅',  '量比',  \
'委比',  '委差',  '均价',  '内盘',  '外盘',  '内外比','买一量','卖一量','市净率','总股本',\
'总市值','流通股','流通市','3日涨', '6日涨', '3日换', '6日换']
#只需要其中一部分，不用全部
col_array = []
act_col = [1,2,3,4,8,9,14,15,16,17]
line = []
for item in stkobj:
	line_arr = item.split(',')
	#for v in line_arr: print v,
	col_array = [line_arr[i] for i in act_col]
	#print col_array
	line.append(col_array)

#测试打印列名称
if param_config['Title']==1:
	column = [column_name[i] for i in act_col]
	for v in column:
		print ("%5s"%(v.decode('utf8'))),
	print ''

#print 
df = pd.DataFrame(line)
	
if param_config['Range']==1:
	df = df.sort_values([3], 0, True)
elif param_config['Price']==1:
	df = df.sort_values([2], 0, True)
#print  df.sort_values([3], 0, True)
#print  df.sort_values([3], 0, False)
print df

