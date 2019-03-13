#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import time
import string
import datetime
import getopt
import tushare as ts
from internal.ts_common import *
from internal.dfcf_inf import *

def getSelfDefStock1(stk_arr):
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
	urlall = 'http://myfavor1.eastmoney.com/mystock?f=gs&cb='+ prestr +'&g=41446251&0.2978216698687475'
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
		return

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
	stk_arr.extend(stk_obj)

def list_realtime_info(basic, codeArray):
	if len(codeArray)==0:
		return
	df = ts.get_realtime_quotes(codeArray)
	#print df
	#c = df[['name','price','bid','ask','volume','amount','time']]
	#name    open pre_close   price    high     low     bid     ask     volume 
	#amount   ...      a2_p  a3_v    a3_p  a4_v    a4_p  a5_v    a5_p  date      time    code
	print ''
	for index,row in df.iterrows():
		stname = row['name']
		stlen=len(stname.encode('gbk'))
		maxlen=10
		if len(stname)<maxlen:
			left=maxlen-stlen
			while left>0:
				stname += ' '
				left-=1
		open = row['open']
		pre_close = row['pre_close']
		price = row['price']
		high = row['high']
		low = row['low']
		volume = int(row['volume'])
		if basic is None:
			turnover_rt = 0
		else:
			total_vol = float(basic.ix[codeArray[index]]['outstanding'])
			turnover_rt = ((volume/10000) / (total_vol*100))
			
		price_f = float(price)
		pre_close_f = float(pre_close)
		if float(price)==0 or float(high)==0:
			change = '-'
			change_l = '-'
			change_h = '-'
			change_o = '-'
		else:
			change = '%02.02f'%( ((price_f-pre_close_f)/pre_close_f)*100 )
			change_l = '%02.02f'%( ((float(low)-pre_close_f)/pre_close_f)*100 )
			change_h = '%02.02f'%( ((float(high)-pre_close_f)/pre_close_f)*100 )
			change_o = '%02.02f'%( ((float(open)-pre_close_f)/pre_close_f)*100 )

		if basic is None:
			str_fmt = "%6s %s %8s(%6s%%)    %8s(%6s) %8s(%6s)"
			print str_fmt%(codeArray[index], stname, price, change, low, change_l, high, change_h)
		else:
			str_fmt = "%6s %s %8s(%6s%%) (%4.02f%%)     %8s(%6s) %8s(%6s)"
			print str_fmt%(codeArray[index], stname, price, change, turnover_rt, low, change_l, high, change_h)
	return
	
#Main
curdate = ''
data_path = "debug/_self_define.txt"
exclude = 0
optlist, args = getopt.getopt(sys.argv[1:], '?fe')
for option, value in optlist:
	if option in ["-f","--file"]:
		data_path='../data/entry/miner/filter.txt'
	elif option in ["-e","--exclude"]:
		exclude = 1
	elif option in ["-?","--???"]:
		print "Usage:", os.path.basename(sys.argv[0]), " [-f filename]"
		exit()

stockCode = []
today = datetime.date.today()
curdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)
#print curdate

#说明show_flag
#0：不获得每一只的流通盘，不会计算换手率
#1：获得每一只的流通盘，并且计算换手率
#2：显示每一只最新的新闻，当天的新闻全部显示，当天没有只显示一条news
pindex = len(sys.argv)
show_flag = 0
if pindex==2:
	if sys.argv[1]=='1':
		show_flag=1
	elif sys.argv[1]=='2':
		show_flag=2

if not os.path.isfile(data_path):
	print "No file:",data_path
	exit(0)

file = open(data_path, 'r')
if '_self_define' in data_path:
	flag=0
	lines = file.readlines(100000)
	for line in lines:
		line=line.strip()
		if line=='STK':
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
		stockCode.append(code)
		#print code
else:
	line = file.readline()
	while line:
		if len(line)>=6:
			code = line[0:6]
			if code.isdigit():
				stockCode.append(code)
		line = file.readline()
	pass
file.close()

if show_flag==1:
	list_latest_news(stockCode, curdate)
	exit(0)

show_idx = ['000001', '399001', '399005', '399006']
idx_df=ts.get_index()
show_index_info(idx_df, show_idx)

codeArray = ['399678']
show_extra_index(codeArray)

st_bas = None
if show_flag==2:
	st_bas=ts.get_stock_basics()
#list_realtime_info(st_bas, stockCode)

if exclude==0:
	stock_array = []
	getSelfDefStock1(stock_array)
	if len(stock_array)==0:
		print "Fail to get self defined from DFCF"
		exit()
	stockCode = []
	for i in  stock_array:
		stockCode.append(i[:6])
	if len(stockCode)==0:
		print ("No self defined item")
		exit(0)
	list_realtime_info(None, stockCode)
