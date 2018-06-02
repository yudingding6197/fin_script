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

def getSelfStock():
	h_cook=\
'st_pvi=04247319295955; qgqp_b_id=867a67ca83c13fbd622d079314b267df; \
HAList=a-sz-002278-%u795E%u5F00%u80A1%u4EFD%2Ca-sz-002413-%u96F7%u79D1%u9632%u52A1%2Ca-sz-300291-%u534E%u5F55%u767E%u7EB3%2Ca-sh-603179\
-%u65B0%u6CC9%u80A1%u4EFD%2Ca-sz-300032-%u91D1%u9F99%u673A%u7535%2Ca-sz-002527-%u65B0%u65F6%u8FBE%2Ca-sh-603721-%u4E2D%u5E7F%u5929%u62E9%2Ca-\
sz-300255-%u5E38%u5C71%u836F%u4E1A%2Ca-sz-002806-%u534E%u950B%u80A1%u4EFD%2Ca-sz-002622-%u878D%u94B0%u96C6%u56E2%2Ca-sh-601360-%u4E09%u516D%u96F6; \
em_hq_fls=js; showpr3guide=1; ct=TlsXdMMkpaEgtaF4NkDFMKJ66FLGGD8j881eoI_rHG_gUf1D0kHm_vec7-r0MZwvzVPf-WbNGnCzTHpuJDJDFcFW56FJYLgxt0qHlb12xz4MuaUISb8zb\
QwhF-Ua7eBDIqSEOLU_bgJDP4uXESnnLnGamF5EW00XEE_gYWgoSz4; ut=FobyicMgeV54OLFNgnrRk4dDkedquoSDr4ZAchNmAQHspWgUetdlESwn-ua44Ed4lpZY6csVsuiCle5qZxAuS8v-Inu\
Fsm6TqHork_ycRSlV9xr-cxt2xU1WX-5dGcddr3_iauTIqMU26t7S1C8NNwQXAxsO9Dh_d1K9L5zZ8nXh9CQBC3s8LvRYENJG1g1rFBx1KTEQNNCjPGLCm4ELqpjOaxKCplgbSn7xxlvCROQZjpRD\
cX1jLYzoIWnH4xbtc46ZBXyHKUKtSbyTZl6tnfhM49ukU31U; pi=6100112247957528%3byudingding6197%3bgoutou%3bk%2fYEChP6YGOVSiilXgkLUt7nPMUXog7ouaSWIqPFsIX0QZ0GrZ\
V7TTysPbsXBELhUkb0jQX%2fkYiMwNTiTgKPnwe74xcogQI0ApV2140UQgeLzrliHuE4%2f3PRNnse9Ik1leQunYyxGxON4Pa9uSqQXVXS298RmzwZdPAPCmPMvNseTcAdHMiU0UzmrRDojkiwYuj\
QtteO%3bfxWqv2yFNBeyKBtxLe7p0sWpBIj5jFARE8ErkhEMufyzRh05yHGLgzo5pXWxdE5lTzacI7b0QYG9AM69NtQy535QrVH%2fh2wYI9LU0IGcmOSFiM5qXRRh4TfmCJDwKl2HRUpqZ6tacDa\
FLmeuZLUBzGdnNAJb%2bQ%3d%3d; uidal=6100112247957528goutou; sid=4725419; vtpst=|; em-quote-version=topspeed; EMSTtokenId=95b8128937a565c39526c705960e3be8;\
 st_si=96019977790553'
	 
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
		return ''

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

	codes = ','.join(i[:6] + i[8:9] for i in strstr.split(','))
	return codes

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
		print "Error fupai urlopen"

	if res_data is None:
		print "Open URL fail"
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
self_code = getSelfStock()
if self_code=='':
	print "Fail to get self defined from DFCF"
	exit()
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

