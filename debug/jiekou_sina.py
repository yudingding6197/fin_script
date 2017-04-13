#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import string
import datetime
import urllib
import urllib2
#包含中文

# Main
url = "http://hq.sinajs.cn/list="
code = ''
pindex = len(sys.argv)
if pindex==1:
	code = '000001'
elif pindex==2:
	code = sys.argv[1]
	if (len(code) != 6):
		sys.stderr.write("Len should be 6\n")
		exit(1);
else:
	sys.stderr.write("Too much param\n")
	exit(1)

head3 = code[0:3]
result = (cmp(head3, "000")==0) or (cmp(head3, "002")==0) or (cmp(head3, "300")==0) or (cmp(head3, "131")==0)
if result is True:
	code = "sz" + code
else:
	result = (cmp(head3, "600")==0) or (cmp(head3, "601")==0) or (cmp(head3, "603")==0) or (cmp(head3, "204")==0)
	if result is True:
		code = "sh" + code
	else:
		print "非法代码:" +code+ "\n"
		exit(1);

urllink = url + code
try:
	#print urllink
	req = urllib2.Request(urllink)
	stockData = urllib2.urlopen(req, timeout=2).read()
except:
	print "URL timeout"
else:
	stockObj = stockData.split(',')
	stockLen = len(stockObj)
	if stockLen<10:
		print "Not find data"
		exit(0)

	for i in range(0, stockLen):
		print "%02d:	%s" % (i, stockObj[i])