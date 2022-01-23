#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import string
import urllib2
import datetime
import bs4
from bs4 import BeautifulSoup
sys.path.append(".")
sys.path.append("..")
from internal.ts_common import *

'''
html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
<script lang="javascript"></script>
</body>
</html>
"""

#通过class(.) 或者 id(#) 查找,用'.' or '#'
#print soup.select('.sister') 
#print soup.select('#link1')

print soup.select("head title")
print soup.select("head > title")

#查找 Tag
soup.find("<script>") 
#通过id查找
soup.find(id="link3")
#属性查找
print soup.select('a[href="http://example.com/elsie"]')
print soup.select('p a[href="http://example.com/elsie"]')


'''

def list_stock_news_sum(codeArray, curdate, file):
	codeLen = len(codeArray)
	for j in range(0, codeLen):
		if file is None:
			continue
		df = None
		try:
			df = ts.get_notices(codeArray[j],curdate)
		except:
			pass
		if df is None:
			df = ts.get_notices(codeArray[j])
		for index,row in df.iterrows():
			file.write("%s,%s"%(row['date'],row['title'].encode('gbk') ))
			file.write("\r\n")
		file.write("\r\n")

prepath = "../data/"
filetxt = prepath + 'tingpai.txt'

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

url = "http://www.cninfo.com.cn/cninfo-new/memo-2"
urlall = url + "?queryDate="+curdate

tf_fl = open(filetxt, 'w+')
LOOP_COUNT = 0
res_data=None
while LOOP_COUNT<3:
	try:
		#req = urllib2.Request(urlall)
		res_data = urllib2.urlopen(urlall)
	except:
		print "Error",sys._getframe().f_code.co_name
		LOOP_COUNT = LOOP_COUNT+1
	else:
		break
if res_data is None:
	exit(0)

content = res_data.read()
#print content
#content1 = content.decode('utf-8', 'ignore')
#soup = BeautifulSoup(content, 'lxml', from_encoding='utf8')
soup = BeautifulSoup(content, 'lxml')
#print (soup.title.string)
#print soup.head
#print soup.head.contents
#整个数据
print(soup.prettify())
#  Tag，BeautifulSoup，NavigableString，comment

stockCode = []
#首先找到此节点
item = soup.find(id='suspensionAndResumption1')
if item is None:
	print "Not find node suspensionAndResumption1"
	exit(0)
item = item.find(class_='column2')
if item is None:
	print "Not find node column2"
	exit(0)
#将 column2 下的节点遍历
for child in item.children:
	#推荐使用isinstance， 代替 type
	#if type(child)==bs4.element.NavigableString:
	#	continue
	#if type(child)!=bs4.element.Tag:
	#	continue

	#过滤非Tag节点
	if isinstance(child, bs4.element.Tag) is False:
		continue
	#child['class'],如果没有'class'属性就会出错
	clslist = child.get('class')
	if clslist is None:
		continue

	clsattr = ''.join(clslist)
	if clsattr=='list-a' or clsattr=='list-b':
		#for lidesc in child.descendants:
		#	print type(lidesc), lidesc
		#	print type(lidesc), lidesc
		#print child.descendants, type(child.children)
		info = ''
		for liitem in child.find_all('li'):
			lilist = liitem.get('class')
			if lilist is None:
				continue
			liattr = ''.join(lilist)
			value = liitem.string
			if liattr=='ta-1':
				stockCode.append(value)
			elif liattr=='ta-2':
				value = "%-8s"%(value)
			elif liattr=='ta-4':
				if value=='&nbsp':
					value = "%16s"%(" ")
			elif liattr=='ta-5':
				value = "%-8s"%(value)

			#print liitem.string
			info += value
			info += "\t"
		tf_fl.write(info.encode('utf8'))
		tf_fl.write('\n')
		print info

#将所有的数据汇总输出
tf_fl.write("\n====================================================================================\n")
list_stock_news_sum(stockCode, curdate, tf_fl)

tf_fl.close()


'''
item = soup.select('div.transaction')
n = 0
while n<len(item):
	#print item[n].text.encode('utf8')
	str = item[n].text
	tf_fl.write( item[n].text.encode('utf8') )
	tf_fl.write( '\n' )

	tfp = u'深沪停复牌'
	print n, item[n].encode('gbk')
	if str.find(tfp) == -1:
		print n
		n += 1
		continue
	item1 = item[n].div
	print n, item1
	#break
	n += 1


#item = soup.find_all('div', id='suspensionAndResumption1')
#print "suppppppppppppppp1:"
#chd = item[0].children
#for child in  item[0].children:
#	print '==========='
#	print child

n = 0
item = soup.find('div', class_='column2')
#print item
for divitem in item:
	#print item[n].text.encode('utf8')
	#str = item[n].text
	#tf_fl.write( item[n].text.encode('utf8') )
	#tf_fl.write( '\n' )
	if n>0:
		print "BRKKKKK", n
		break

	#item1 = item[n].find('div')
	print "<<<", divitem, ">>>"
	str = divitem.stripped_strings
	print "str:::", str, ":>"
	if str is None or str=='':
		n += 1
		print "CCCCCCCC", n
		continue
	n += 1
	print "ccc",n
	continue
	
	
	tfp = u'今起停牌'
	if str.find(tfp) == 0:
		print 111111
	#print divitem
	#break
	n += 1
'''

'''
flag = 0
count = 0
ignore = 0
line = res_data.readline()
checkStr = '复牌日'
stockCode = []
stockIdx = -1
while line:
	try:
		l = line.decode('utf8')
		print "============",l
		tf_fl.write(line)
		#tf_fl.write(line)
	except:
		print "?????????????",line.decode('utf8')
		#l = line.decode('gbk', 'ignore')
		#tf_fl.write(l)
	#else
	#print line.decode('utf8')
	line = res_data.readline()
	continue
'''


tf_fl.close()
exit(0)
