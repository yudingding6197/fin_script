# -*- coding:gbk -*-
import urllib
import urllib2

#url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php?symbol=sz300001"
url = "http://market.finance.sina.com.cn/transHis.php?symbol=sz300001&date=2015-9-11&page=1"

req = urllib2.Request(url)
#print req

res_data = urllib2.urlopen(req)

flag = 0
line = res_data.readline()
checkStr = '成交时间'
while line:
	index = line.find(checkStr)
	if (index>=0):
		if flag==0:
			checkStr = '<th>'
			flag = 1
		else:
#			re.compile(r'\d{2}:\d{2}:\d{2}</th><td>\d{1-5}.\d{2}*')
#			print line
			pass
	print line
	line = res_data.readline()


