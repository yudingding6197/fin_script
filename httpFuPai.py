# -*- coding:gbk -*-
import urllib
import urllib2

url = "http://www.cninfo.com.cn/search/memo.jsp?datePara=2015-09-07"
url = "http://www.cninfo.com.cn/information/memo/jyts_more.jsp?datePara=2015-09-07"

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


