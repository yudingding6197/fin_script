#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import urllib2
import json
import zlib
import random
import getopt
import datetime
from bs4 import BeautifulSoup
sys.path.append(".")
from internal.common import *

#沪深市场每日信息统计，还需要不断完善

def http_req(urlall, send_headers1, tp, qdate):
	#print (urlall)
	#print (send_headers1)
	fd = ''
	index = 0
	if tp=='h0':
		print("Not implement:", tp)
		return
	elif tp=='s0':
		fd = '0total'
	elif tp=='s1':
		fd = '1zhb'
		index = 1
	elif tp=='s2':
		fd = '2zxb'
		index = 2
	elif tp=='s3':
		fd = '3cyb'
		index = 3
	else:
		print("Unknow:", tp)
		return

	res_data = None
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
		print("Open URL fail", qdate)
		return

	content = res_data.read()
	respInfo = res_data.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
		#print "Content compressed"
		content = zlib.decompress(content, 16+zlib.MAX_WBITS);
	#else:
	#	print "Content not zip"
	#print content.decode('utf8')
	
	#进行数据处理，过滤非JYR
	data = json.loads(content)
	if len(data)!=4:
		print("Content not match ", qdate)
		return
	if 'data' not in data[index].iterkeys():
		print("No key : data ", qdate)
		return
	item = data[index]['data']
	if len(item)==0:
		# No JY data, return
		return

	filename = '../data/entry/index/sz/'+fd+'/sz_'+fd+'_'+qdate+'.txt'
	tf_fl = open(filename, 'w+')
	tf_fl.write(content)
	tf_fl.close()

def genRand(length):
	r1 = random.random()

	fmt = "%." + str(length) + "f"
	r1 = float(fmt % r1)

	sr1 = repr(r1)
	return sr1

def formatRand(length=16):
	sr1 = genRand(length)
	rlen = len(sr1)
	while rlen<3:
		print("Warning: too short", sr1);
		sr1 = genRand(length)
		rlen = len(sr1)
	rlen -= 2

	if (rlen>length):
		print ("Warning: Great", rlen, sr1)
		sr1 = sr1[0:length+2]
	elif (rlen<length):
		delta = length-rlen
		while delta>0:
			sr1 += random.choice('123456789')
			delta -= 1
		#print ("Less", sr1)
	return sr1
	
#Main
#for i in range(0,1000):
#	formatRand()

param_config = {
	"Start":'',		#开始时间
	"End":'',		#结束时间
	"Type":'',		#获取的板块，总体,Main,ZX,CY
	"Force":0,		#是否强制刷新
}

optlist, args = getopt.getopt(sys.argv[1:], 's:e:t:f:')
for option, value in optlist:
	if option in ["-s","--start"]:
		param_config["Start"] = value
	elif option in ["-e","--end"]:
		param_config["End"] = value
	elif option in ["-t","--type"]:
		param_config["Type"] = value
	elif option in ["-f","--force"]:
		param_config["Force"] = int(value)

today = datetime.date.today()
str_end = ''
if param_config["End"]=='':
	str_end = '%04d-%02d-%02d' %(today.year, today.month, today.day)
else:
	ret,str_end = parseDate(param_config["End"], today)
	if ret==-1:
		exit(1)
ed_date = datetime.date(*map(int, str_end.split('-')))

str_start = ''
if param_config["Start"]=='':
	str_start = '%04d-%02d-%02d' %(today.year, today.month, today.day)
else:
	ret,str_start = parseDate(param_config["Start"], today)
	if ret==-1:
		exit(1)
st_date = datetime.date(*map(int, str_start.split('-')))

urlstr = 'http://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&CATALOGID=1803&TABKEY=%s&txtQueryDate=%s&random=%s'
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

tab = 'tab4'
tp = param_config["Type"]
if tp=='':
	tp = 's3'

if tp=='h0':
	tab = tab
elif tp=='s0':
	tab = 'tab1'
elif tp=='s1':
	tab = 'tab2'
elif tp=='s2':
	tab = 'tab3'
elif tp=='s3':
	tab = 'tab4'

cur_date = st_date
while (ed_date - cur_date).days>=0:
	#print(cur_date)
	qdate = '%04d-%02d-%02d' %(cur_date.year, cur_date.month, cur_date.day)
	rand = formatRand()

	urlall = urlstr %(tab, cur_date, rand)
	http_req(urlall, send_headers, tp, qdate)

	delta1=datetime.timedelta(days=1)
	cur_date = cur_date + delta1
