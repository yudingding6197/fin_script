#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import string
import datetime
import urllib
import urllib2
#��������

'''
0����DAQIN_TL���� ���֣�
1����27.55�壬���տ��̼ۣ�
2����27.25�壬�������̼ۣ�
3����26.91�壬��ǰ�۸�
4����27.55�壬������߼ۣ�
5����26.20�壬������ͼۣ�
6����26.91�壬����ۣ�������һ�����ۣ�
7����26.92�壬�����ۣ�������һ�����ۣ�
8����22114263�壬�ɽ��Ĺ�Ʊ�������ڹ�Ʊ������һ�ٹ�Ϊ������λ��������ʹ��ʱ��ͨ���Ѹ�ֵ����һ�٣�
9����589824680�壬�ɽ�����λΪ��Ԫ����Ϊ��һĿ��Ȼ��ͨ���ԡ���Ԫ��Ϊ�ɽ����ĵ�λ������ͨ���Ѹ�ֵ����һ��
10����4695�壬����һ������4695�ɣ���47�֣�
11����26.91�壬����һ�����ۣ�
12����57590�壬�������
13����26.90�壬�������
14����14700�壬��������
15����26.89�壬��������
16����14300�壬�����ġ�
17����26.88�壬�����ġ�
18����15100�壬�����塱
19����26.87�壬�����塱
20����3100�壬����һ���걨3100�ɣ���31�֣�
21����26.92�壬����һ������
(22,
23), (24, 25), (26,27), (28,
29)�ֱ�Ϊ���������������ĵ������
30����2008-01-11�壬���ڣ�
31����15:05:32�壬ʱ�䣻
'''


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
		print "�Ƿ�����:" +code+ "\n"
		exit(1);

urllink = url + code
#֧��ͬʱ��ѯ���
urllink = url + "sz000001,sh600006,sz000520"
#print("url=" + urllink)
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
		sobj = stockObj[i].decode('gbk')
		print u"%02d:	%s" % (i, sobj)
