# -*- coding:gbk -*-
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

def list_stock_news_sum(codeArray, curdate, file):
	codeLen = len(codeArray)
	for j in range(0, codeLen):
		df = ts.get_notices(codeArray[j],curdate)
		if file is None:
			continue
		for index,row in df.iterrows():
			file.write("%s,%s"%(row['date'],row['title'].encode('gbk') ))
			file.write("\r\n")
		file.write("\r\n")

prepath = "..\\Data\\"
prepath1 = "..\\Data\\entry\\fupai\\"
pindex = len(sys.argv)
today = datetime.date.today()
curdate = ''
if (pindex == 1):
	curdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)
	edate = datetime.datetime.strptime(curdate, '%Y-%m-%d').date()
	#如果是当日的数据通过history链接目前不能得到，所以暂时得到前一天的数据
	#今日数据通过getToday获取
	#edate = edate - delta1
else:
	curdate = sys.argv[1]
	if curdate=='.':
		curdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)
	else:
		ret,curdate = parseDate(sys.argv[1], today)
		if ret==-1:
			exit(1)
#print curdate

url = "http://www.cninfo.com.cn/information/memo/jyts_more.jsp?datePara="

totalline = 0
lasttime = ''
filename = prepath + 'fupai' + '_detail'
filetxt = filename + '.txt'
fl = open(filetxt, 'w')

urlall = url + curdate
req = urllib2.Request(urlall)
res_data = urllib2.urlopen(req)

flag = 0
count = 0
ignore = 0
line = res_data.readline()
checkStr = '复牌日'
stockCode = []
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
		#读取每一行，首先得到ST代码
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

		#解析完此行，继续下一行
		line = res_data.readline()
		continue
	key = re.match(r'(.+)(</a></td>)', line)
	if key:
		#print key.groups()
		#再读取代码对应的名字
		if ignore==0:
			codename = key.group(1)
			fl.write(codename)
			fl.write("\n")
			print stockCode[stockIdx],codename
			list_stock_news(stockCode[stockIdx], curdate, fl)
			totalline += 1
		count = 0
		ignore = 0
		line = res_data.readline()
		continue
	count += 1
	if (count>2):
		break;
	line = res_data.readline()

#将所有的数据汇总输出
fl.write("\n====================================================================================\n")
list_stock_rt(stockCode, curdate, fl)
list_stock_news_sum(stockCode, curdate, fl)

fl.close()
if (totalline==0):
	print "No Matched Record"
	os.remove(filetxt)
else:
	shutil.copy(filetxt, prepath1)