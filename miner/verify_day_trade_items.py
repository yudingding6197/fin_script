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

#获取指定日期的数据，检查个股内容是否正确

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

#验证前2行数据
def check_tick_content(fpath):
	bok = 0
	file = open(fpath, 'r')
	line = file.readline()
	if len(line)<20:
		print "Error: Invalid format1", fpath
		return -1
	if line[:10]!='time,price':
		print line[:10]
		print "Error: Invalid format2", fpath
		return -1

	line = file.readline()
	tmObj = re.match('(\d+):(\d+):(\d+),(.*)', line)
	if tmObj is None:
		print "Error: Invalid format3", fpath
		return -1
	file.close()

	hour=tmObj.group(1)
	minute=tmObj.group(2)
	if (hour=="15" and minute=='00') or (hour=="14" and minute=='59'):
		return 0
		
	#校验不能通过的，再详细一些检查
	df = pd.read_csv(fpath)
	#YZZT
	llen = len(df['price'].unique())
	if llen==1:
		if df['price'].count()<100:
			return 0
	#New stock
	elif llen==2:
		if df['price'].count()>100:
			return 0
	if hour=="14" and minute<="55":
		print "Warning: check value", hour, minute, fpath
	return 0

def get_stock_bid_status(trade_dt, codesDict):
	folder = '../data/entry/tdx_history/'
	fname = '沪深Ａ股'
	fpath = folder + fname + ntd + '.txt'
	if not os.path.isfile(fpath):
		print "Error: " +fpath+ " not exists"
		return -1

	file = open(fpath, 'r')
	line = file.readline()
	while line:
		if len(line)<6:
			line = file.readline()
			continue
		item = line[0:6]
		if not item.isdigit():
			line = file.readline()
			continue
		props = line.split('\t')
		if len(props)<6:
			print "Invalid line:", line
			line = file.readline()
			continue
		if props[3]=='' or props[4]=='0':
			#print "%s,'%s'" % (item, props[3])
			codesDict[item] = 0
		else:
			codesDict[item] = 1
		line = file.readline()
	file.close()
	return 0

#Main 
# 
param_config = {
	"Date":'',
	"All":0		#TODO:通过All验证，过滤整过文件夹，找出匹配日期的文件，再进行校验
}

if __name__=='__main__':
	beginTm = datetime.datetime.now()
	init_trade_obj()
	td = ''
	nowToday = datetime.date.today()
	optlist, args = getopt.getopt(sys.argv[1:], '?ad:')
	for option, value in optlist:
		if option in ["-d","--date"]:
			ret,stdate = parseDate(value, nowToday, ai=1)
			if ret==-1:
				exit()
			param_config['Date'] = stdate
			td = stdate
		elif option in ["-a","--all"]:
			param_config['All'] = 1
			print "Is building..."
			exit()
		elif option in ["-?","--??"]:
			print "Usage:", os.path.basename(sys.argv[0]), " [-d MMDD/YYYYMMDD]"
			exit()

	if td=='':
		days = 5
		tradeList = []
		get_pre_trade_date(tradeList, days)
		if len(tradeList)!=days:
			print "Fail to get trade date"
			exit()
		td = str(tradeList[0])

	if chk_holiday(td):
		print td, "is holiday, Quit"
		exit()

	sarry = td.split('-')
	ntd=''.join(sarry)
	codesDict = {}
	ret = get_stock_bid_status(td, codesDict)
	if ret==-1:
		exit()
	print "Get all data in", td
	#codesDict = {'603680':1, '000520':0}
	#print codesDict

	folder = '../data/entry/resp/'
	for key in codesDict.keys():
		code = key
		fname = code + '_' + td + '.csv'
		fpath = folder + code + '/' + fname
		if codesDict[code]==0:
			if os.path.isfile(fpath):
				print "Error: exist file", fpath
			continue
		if not os.path.isfile(fpath):
			print "Error: Not exist file", fpath
			continue
		check_tick_content(fpath)
	endTm = datetime.datetime.now()
	print "Verify %d data" %(len(codesDict))
	print "END ", (endTm-beginTm)