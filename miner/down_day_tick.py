#!/usr/bin/env python
# -*- coding:gbk -*-

import sys
import re
import os
import time
import getopt
import datetime
sys.path.append(".")
sys.path.append("..")
from internal.ts_common import *
import tushare as ts

#下载每一天item的每笔交易数据
#将停牌的排除，只选择指定日期进行交易的items

'''  
{ #3个可用数据源
'tt': 'http://stock.gtimg.cn/data/index.php?appn=detail&action=download&c=sz300553&d=20180102', 
'nt': 'http://quotes.money.163.com/cjmx/2018/20180102/1300553.xls', 
'sn': 'http://market.finance.sina.com.cn/downxls.php?date=2018-01-02&symbol=sz300553'
}
'''

urlall = 'http://market.finance.sina.com.cn/downxls.php?date=%s&symbol=%s'
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

def fetch_tick_resource_sn(entry, code, trdate, ds, feedback_list):
	shcd = ['600', '601', '603']
	szcd = ['000','001','002','300']
	head3 = code[0:3]
	if head3 in szcd:
		ncode = "sz" + code
	elif head3 in shcd:
		ncode = "sh" + code
	else:
		print "非法代码:" +code+ "\n"
		return

	urllink = urlall %(trdate, ncode)
	print urllink
	try:
		#proxy = {'http':'http://122.114.31.177:808'}
		#proxy = None
		#req = urllib2.Request(urllink, headers=send_headers, proxies=proxy)
		req = urllib2.Request(urllink, headers=send_headers)
		res_data = urllib2.urlopen(req)
	except Exception as e:
		print "Error:", urllink
		print e
		#LOOP_COUNT = LOOP_COUNT+1
		return
	content = res_data.read()
	respInfo = res_data.info()
	print content[:32]
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
		print "Content compressed"
		content = zlib.decompress(content, 16+zlib.MAX_WBITS);
	#print content.decode('utf8')

	cdpath = entry + '/' + code
	fpath = cdpath + '/' + code + '_' + trdate +'.csv'
	if content[:7]=='<script':
		return
	file = open(fpath, 'w')
	file.write(content)
	file.close()
	return

#TODO: 增加股票代码合法性检查，sn, tt, nt下载的文件格式不一样，sn错误的时候，输出日志取消
def fetch_tick_resource(entry, code, trdate, ds, feedback_list):
	tickdf = None
	i = 0
	bclear = 0
	for item in ds:
		try:
			tickdf = ts.get_tick_data(code, trdate, src=item)
		except IOError:
			if item=='sn':
				ds.remove(item)
			print "Error: get data", code, ds
		else:
			if tickdf is None:
				print code, trdate, ds, "is None"
				continue
			if tickdf.empty:
				continue
			#检查sina的数据
			elif item=='sn':
				tm = tickdf.ix[0][0]
				tmObj = re.match('(\d+):(\d+):(\d+)', tm)
				if tmObj is None:
					continue
			break
	if tickdf is None:
		print code, trdate, "is None"
		return
	elif tickdf.empty:
		feedback_list.append(code)
		print code, trdate, "EMPTY"
		return

	cdpath = entry + '/' + code
	fpath = cdpath + '/' + code + '_' + trdate +'.csv'
	if item=='tt' or item=='nt':
		tickdf = tickdf.iloc[::-1]
	tickdf.to_csv(fpath, encoding="gbk", index=False)
	return

#检查文件是否存在，已经存在不需要再次下载了
def check_code_path(entry, code, trdate):
	cdpath = entry + '/' + code
	if not os.path.exists(cdpath):
		os.makedirs(cdpath)

	fpath = cdpath + '/' + code + '_' + trdate +'.csv'
	if not os.path.exists(fpath):
		return 0
	if not os.path.isfile(fpath):
		print "Error: check file:", fpath
	return 1

def check_matched_stock(fpath, stock_list):
	if not os.path.isfile(fpath):
		print "Not find file to store matched item:", fpath
		return -1

	file = open(fpath, 'r')
	line=file.readline()
	while (line):
		code = line[:6]
		if len(code)==6:
			stock_list.append(code)
		else:
			print "Not correct code", line
		line=file.readline()
	file.close()
	return 0
	
def separate_bid_or_not(folder, trade_dt, tdx_chk, codes_list, not_trade_list):
	if tdx_chk==0:
		#通过文件得到当天没有交易的item
		fpath = folder + "stock_" + trade_dt + ".txt"
		ret = check_matched_stock(fpath, not_trade_list)
		if ret==-1:
			return -1

		#首先从 A文件中获取分离信息，如果失败，尝试laster_stk
		preName = '沪深Ａ股'
		ntd = ''.join(trade_dt.split('-'))
		fpath = '../data/entry/tdx_history/' + preName + ntd + ".txt"
		ret = check_matched_stock(fpath, codes_list)
		if ret==0:
			return 0
		#通过latest_stock得到所有的代码
		fpath = folder + "latest_stock.txt"
		ret = check_matched_stock(fpath, codes_list)
		if ret==-1:
			return -1
		return 0

	fpath = folder + "latest_stock.txt"
	file = open(fpath, 'r')
	line=file.readline()
	df = None
	LOOP_COUNT = 0
	tdxcn = ts.get_apis()
	while (line):
		if LOOP_COUNT>3:
			print "Too many error, retry"
			break
		code = line[:6]
		try:
			df = ts.bar(code, tdxcn)
		except:
			print "ERROR:"
			ts.close_apis(tdxcn)
			print "Re-connect"
			tdxcn = ts.get_apis()
		if df is None:
			print code, "get bar is None"
			#line=file.readline()
			LOOP_COUNT += 1
			continue
		LOOP_COUNT = 0
		if not df[td].empty:
			ncode = df[td]['code'][0]
			print ncode
			codes_list.append(ncode)
		line=file.readline()

	file.close()
	ts.close_apis(tdxcn)
	return 0
#Main 
# 
param_config = {
	"Date":'',
	"Code":'',
	"File":0
}

if __name__=='__main__':
	beginTm = datetime.datetime.now()
	init_trade_obj()
	td = ''
	nowToday = datetime.date.today()
	optlist, args = getopt.getopt(sys.argv[1:], '?fc:d:')
	for option, value in optlist:
		if option in ["-d","--date"]:
			ret,stdate = parseDate(value, nowToday, ai=1)
			if ret==-1:
				exit()
			param_config['Date'] = stdate
			td = stdate
		elif option in ["-c","--code"]:
			param_config['Code'] = value
		elif option in ["-f","--file"]:
			param_config['File'] = 1
		elif option in ["-?","--??"]:
			print "Usage:", os.path.basename(sys.argv[0]), " [-d MMDD/YYYYMMDD]"
			exit()

	if td=='':
		td = str(get_last_trade_dt())
	if chk_holiday(td):
		print td, "is holiday, Quit"
		exit()

	entry = '../data/entry/resp'
	if not os.path.exists(entry):
		os.makedirs(entry)

	codes_list = []
	not_td_list = []
	if param_config['Code']!='':
		codes_list.append(param_config['Code'])
	elif param_config['File']==1:
		file = open('../data/entry/miner/filter.txt', 'r')
		line = file.readline()
		while line:
			if len(line)>=6:
				line = line[:6]
				if line.isdigit():
					codes_list.append(line)
			line = file.readline()
	else:
		folder = '../data/entry/market/'
		ret = separate_bid_or_not(folder, td, 0, codes_list, not_td_list)
		if ret==-1:
			print "Error: Verify bid code fail"
			exit()
	#codes_list = ['603680']
	#codes_list = codes_list[:2]

	print "Start to add tick data", td
	ds = ['sn', 'tt', 'nt']
	feedbac_list = []
	#print codes_list
	for code in codes_list:
		if code in not_td_list:
			#print "Not in list", code
			continue
		result = check_code_path(entry, code, td)
		if result!=0:
			#print "Exist data", code
			continue
		#print "Fetch data=", code
		fetch_tick_resource(entry, code, td, ds, feedbac_list)
	endTm = datetime.datetime.now()
	print "END ", (endTm-beginTm)