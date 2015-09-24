# -*- coding:gbk -*-
import urllib
import urllib2
import re

url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php?date=2015-09-18&symbol=sz300001"
url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php?date=2015-09-01&symbol=sz300001&page=1"
url = "http://market.finance.sina.com.cn/transHis.php?symbol=sh600401&date=2015-06-18&page=1"
#url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php?symbol=sz300001"
#url = "http://finance.sina.com.cn/realstock/company/sz300001/nc.shtml"


req = urllib2.Request(url)
#print req

res_data = urllib2.urlopen(req)

flag = 0
line = res_data.readline()
'''
checkStr = '收盘价'
while line:
	index = line.find(checkStr)
	if (index<0):
		line = res_data.readline()
		continue
	else:
		flag = 1
		break;
'''

#找到关键字后，查找新的关键字
i = 0
keyw='收盘价|涨跌幅|前收价|开盘价|最高价|最低价|成交量|成交额'
dtlRe = re.compile(r'\D+('+keyw+').*>(\d+\.\d+)')
while line:
	#print "s='"+ line + "'"
	#dtlRe = re.compile(r'\D+前收价\D+(\d+\.\d+)')
	print line
	#obj = dtlRe.match(line)
	#if obj:
	#	print "FD---", obj.group(2)
	#else:
	#	print "NNNNNNNNNNNN"
	i += 1
	if (i>1000):
		break
	line = res_data.readline()


