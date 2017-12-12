#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import urllib2
import datetime
from ts_common import *

def get_date_with_last():
	today = datetime.date.today()
	curdate = ''
	bLast = 0

	pindex = len(sys.argv)
	lastdt = get_last_trade_dt()
	if (pindex == 1):
		curdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)
		edate = datetime.datetime.strptime(curdate, '%Y-%m-%d').date()
		#����ǵ��յ�����ͨ��history����Ŀǰ���ܵõ���������ʱ�õ�ǰһ�������
		#��������ͨ��getToday��ȡ
		#edate = edate - delta1
		
		#Ŀǰͨ�������ս��м��ж�
		#ts.is_holiday()  or chk_holiday()
		today = datetime.datetime.strptime(curdate, '%Y-%m-%d')
		if today.isoweekday() in [6, 7]:
			curdate = lastdt
		bLast = 1
	else:
		curdate = sys.argv[1]
		if curdate=='.':
			curdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)
		else:
			ret,curdate = parseDate(sys.argv[1], today)
			if ret==-1:
				exit(1)
			if curdate==lastdt:
				bLast = 1
	return curdate, bLast

def get_tingfupai_res(curdate):
	url = "http://www.cninfo.com.cn/information/memo/jyts_more.jsp?datePara="
	urlall = url + curdate

	LOOP_COUNT = 0
	res_data=None
	while LOOP_COUNT<3:
		try:
			req = urllib2.Request(urlall)
			res_data = urllib2.urlopen(req)
		except:
			print "Error fupai urlopen"
			LOOP_COUNT = LOOP_COUNT+1
		else:
			break
	return res_data

def get_all_fupai_data(res_data, fl, detail, curdate, stockCode, stockName):
	totalline = 0
	flag = 0
	count = 0
	ignore = 0
	line = res_data.readline()
	checkStr = '������'
	stockIdx = -1
	while line:
	#	print line
		if flag==0:
			index = line.find(checkStr)
			if (index>=0):
				flag = 1
			line = res_data.readline()
			continue

		key = re.match(r'.+fulltext.+\'(\d+)\',\'(\d+)\'', line)
		if key:
			#print key.groups()
			#��ȡÿһ�У����ȵõ�ST����
			code = key.group(1)
			if (len(code) == 6):
				head3 = code[0:3]
				result = (cmp(head3, "000")==0) or (cmp(head3, "002")==0) or (cmp(head3, "300")==0)
				if result is True:
					stockCode.append(code)
					stockIdx += 1
					fl.write(code + ' ')
				else:
					result = (cmp(head3, "600")==0) or (cmp(head3, "601")==0) or (cmp(head3, "603")==0)
					if result is True:
						stockCode.append(code)
						stockIdx += 1
						fl.write(code + ' ')
					else:
						ignore = 1
			else:
				print "Invalid code:" +code

			#��������У�������һ��
			line = res_data.readline()
			continue
		key = re.match(r'(.+)(</a></td>)', line)
		if key:
			#print key.groups()
			#�ٶ�ȡ�����Ӧ������
			if ignore==0:
				codename = key.group(1)
				fl.write(codename)
				fl.write("\n")
				print "====",stockCode[stockIdx],codename.decode('gbk')
				stockName.append(codename)
				if detail==1:
					list_stock_news(stockCode[stockIdx], curdate, None)
				totalline += 1
			count = 0
			ignore = 0
			line = res_data.readline()
			continue
		count += 1
		if (count>2):
			break;
		line = res_data.readline()
	return totalline
