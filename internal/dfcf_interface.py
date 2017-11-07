#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import os
import re
import datetime
import urllib2

urlall = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._BKGN&sty=FPGBKI&st=c&sr=-1&p=1&ps=5000&cb=&token=7bc05d0d4c3c22ef9fca8c2a912d779c&v=0.2694706493189898"
send_headers = {
 'Host':'nufm.dfcfw.com',
 'User-Agent':'User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
 'Accept':'*/*',
 'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
 'DNT':'1',
 'Connection':'keep-alive'
}

class bkStatInfo:
	increase = 0
	fall = 0
	s_zthl = 0
	zt_count = 0
	zt_list = []
	dt_count = 0
	dt_list = []

def query_gainianbankuai(listobj, bkInfo):
	try:
		req = urllib2.Request(urlall,headers=send_headers)
		res_data = urllib2.urlopen(req)
	except:
		print "Error fupai urlopen"
		#LOOP_COUNT = LOOP_COUNT+1

	if res_data is None:
		print "Open URL fail"
		return

	content = res_data.read()
	line = content.decode('utf8')
	obj = re.match('.*\(\[(.*)\]\)',line)
	line = obj.group(1)
	#这个if可能判断多余，强行左右匹配引号里的内容""
	if line is None:
		pos = line.find('"')
		if pos == -1:
			print "NOT Find Left"
			return
		rpos = line.rfind('"')
		if rpos==-1:
			print "NOT Find Right"
			return
		if rpos<=pos:
			print "Invalid result"
			return
		line = line[pos:rpos+1]
	#排名	板块名称	相关资讯	最新价	涨跌额	涨跌幅	总市值(亿)	换手率	上涨家数	下跌家数	领涨股票	涨跌幅
	#1	昨日涨停	行情股吧 资金流	9541.65	379.05	4.14%	304	9.66%	9	0	阿石创	10.00%
	#2	国产芯片	行情股吧 资金流	1240.10	30.68	2.54%	4929	2.14%	34	5	聚灿光电	10.03%

	#Flag(0)板块号 板块名称(2)涨幅 总市值 换手率 上涨家数|平盘家数|下跌家数|停牌家数(6),个股代码(7)Flag 个股名称(9)价格 涨幅(11),个股代码(12)Flag 个股名称(14)价格 跌幅(16),Flag 最新值(18)涨跌额(19) 
	#1,BK0891,国产芯片,2.53,493268904578,2.28,35|1|4|1,300708,2,聚灿光电,17.01,10.03,300613,2,富瀚微,206.99,-2.31,3,1239.97,30.55
	#1,BK0706,人脑工程,-0.15,70185675359,0.28,4|1|3|0,300238,2,冠昊生物,24.18,1.00,300244,2,迪安诊断,27.20,-2.30,3,1667.64,-2.57

	rank = 0
	strline = u'排名,板块名称,板块涨幅,家数,领涨个股,涨幅,领跌个股,跌幅'
	while 1:
		obj = re.match(r'"(.*?)",?(.*)', line)
		if obj is None:
			break
		line = obj.group(2)
		#print obj.group(1)
		str_arr = obj.group(1).split(',')
		bk_code = str_arr[1]
		bk_name = str_arr[2]
		left = 10-len(bk_name.encode('gbk'))
		for i in range(0, left):
			bk_name += ' '
		bk_change = str_arr[3]
		if str_arr[3]=='-':
			bk_change_f = 0
		else:
			bk_change_f = float(str_arr[3])
		bk_stat = str_arr[6]
		lz_code = str_arr[7]
		lz_name = str_arr[9]
		left = 10-len(lz_name.encode('gbk'))
		for i in range(0, left):
			lz_name += ' '
		lz_change = str_arr[11]
		lz_change_f = float(lz_change)
		if lz_change_f>=9.9:
			lz_change = '##' + lz_change
			if lz_code not in bkInfo.zt_list:
				bkInfo.zt_count += 1
				bkInfo.zt_list.append(lz_code)
		else:
			lz_change = '  ' + lz_change
		ld_code = str_arr[12]
		ld_name = str_arr[14]
		left = 10-len(ld_name.encode('gbk'))
		for i in range(0, left):
			ld_name += ' '
		ld_change = str_arr[16]
		ld_change_f = float(ld_change)
		if ld_change_f<=-9.9:
			ld_change = '**' + ld_change
			if ld_code not in bkInfo.dt_list:
				bkInfo.dt_count += 1
				bkInfo.dt_list.append(ld_code)
		else:
			ld_change = '  ' + ld_change
		bk_price = str_arr[18]
		bk_value = str_arr[19]

		rank += 1
		fmt = "%4d %-s %6s  %-16s %-s %-8s %-s %-8s"
		str = fmt % (rank, bk_name, bk_change, bk_stat, lz_name, lz_change, ld_name, ld_change)
		#print str
		listobj.append(str)
		
		if bk_change_f>0:
			bkInfo.increase += 1
		elif bk_change_f<0:
			bkInfo.fall += 1
