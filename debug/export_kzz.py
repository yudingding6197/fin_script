#!/usr/bin/env python
# -*- coding:gbk -*-
#��תծ
import sys
import re
import urllib2
import datetime
import zlib
import json
import getopt
import pandas as pd
sys.path.append(".")
sys.path.append("..")
from internal.dfcf_interface import *

'''
urlall = "http://data.eastmoney.com/kzz/default.html"

http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=KZZ_LB&token=70f12f2f4f091e459a279469fe49eca5&cmd=&st=STARTDATE&sr=-1&p=2&ps=50&js=var%20fnhOGnNf={pages:(tp),data:(x)}&rt=50462432
curl 'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=KZZ_LB&token=70f12f2f4f091e459a279469fe49eca5&cmd=&st=STARTDATE&sr=-1&p=2&ps=50&js=var%20ShTNyQGa=\{pages:(tp),data:(x)\}&rt=50462435' -H 'Referer: http://data.eastmoney.com/kzz/default.html' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2986.0 Safari/537.36' --compressed ;
curl 'http://datapic.eastmoney.com/img/loading.gif' -H 'Referer: http://data.eastmoney.com/kzz/default.html' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2986.0 Safari/537.36' --compressed
==========
[STARTDATE]='2017-12-04T00:00:00'		�깺����
[QSCFJ]='7.31'				ǿ�괥����
[TEXCH]='CNSESZ'			����������
[AISSUEVOL]='10.0'			���й�ģ
[ISSUEPRICE]='100.0'		���м�
[DELISTDATE]='-'			ժ������
[BCODE]='17270600001JBV'	��������
[SWAPSCODE]='002284'		���ɴ���
[CORRESNAME]='��̫��ծ'		ծȯ��������
[BONDCODE]='128023'			ծȯ����
[PB]='2.36'					PB
[SNAME]='��̫תծ'			ծȯ����
[PARVALUE]='100.0'			����
[MarketType]='2'			�г����� 1���Ͻ���2���
[LISTDATE]='2017-12-26T00:00:00'		���н�������
[HSCFJ]='13.57'				���۴�����
[SECURITYSHORTNAME]='��̫�ɷ�'			��������
[GDYX_STARTDATE]='2017-12-01T00:00:00'	��Ȩ�Ǽ���
[LUCKRATE]='0.0245376003'	��ǩ��
[ZGJZGJJZ]='81.6091954023'	��ǰת�ɼ�ֵ
[LIMITBUYIPUB]='100.0'		����깺����
[MEMO]=''					��ע
[ZGJ]='8.52'				ת�ɼ�
[ZQHDATE]='2017-12-06T00:00:00'			��ǩ�ŷ�����
[YJL]='22.5352112676'		�����
[FSTPLACVALPERSTK]='1.3558'	ÿ�����۶�
[ZQNEW]='100.0'				ծȯ���¼۸�
[CORRESCODE]='072284'		�깺����
[SWAPPRICE]='10.44'			������ʼת�ɼ�
[ZGJ_HQ]='8.52'				���ɼ�
[ZGJZGJ]='10.44'			��ǰת�ɼ�
'''

urlfmt = 'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=KZZ_LB&token=70f12f2f4f091e459a279469fe49eca5&cmd=&st=STARTDATE&sr=-1&p=%d&ps=50&js=iGeILSKk={pages:(tp),data:(x)}&rt=50463927'
send_headers = {
'Host':'dcfm.eastmoney.com',
'Connection':'keep-alive',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
'Accept':'*/*',
'DNT': '1',
'Referer': 'http://data.eastmoney.com/kzz/default.html',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.8',
'Cookie': 'st_pvi=33604263703666; emstat_bc_emcount=300285734935048278; \
pi=6100112247957528%3byudingding6197%3bgoutou%3bcUC1rQLS6GFOJIpJ%2b0I6Wt5AdIat%2bLRj2ZvGrlzeObRNvIHEcy62FDfQ%2boIImkvxiIyCd9QIklChsWI2qjINWL\
5DdBKYMZ71JGBsgoVjEXYjdw1rWDHu45I%2bNugmP4pbtdgvhUf884FcXhI1tqTCeHOobtdLSzpfA7h3MiSCx5rf8AdOH0uOhUuvYFxLUOx0oD6KGdMI%3bJ7wwpyq2YPDBfbw\
AqENYGA8GKWnFXYc1dIR5LuUNwKNYfZKtn2ufQSBXaOy%2fJuok5A10Hmp70CM%2bH4jRSUeLe8OOEOwSG5o1tvO4rx%2fTjNoq%2fbM2d6QYkUKtXL0XTX8nREubTh%2bPugi\
WdGxX3hARJpanE0qULw%3d%3d; \
uidal=6100112247957528goutou; vtpst=|; '
}

def export_ebk(kdf):
	kzzebk = "../data/kzz.EBK"
	file = open(kzzebk, 'w')
	for index,items in kdf.iterrows():
		code = items[0]
		str = ''
		if code[:2]=='11':
			str = '1%s\n'%(code)
		elif code[:2]=='12':
			str = '0%s\n'%(code)
		if str!='':
			file.write(str)
	file.close()
	return

#Main
if __name__=="__main__":
	req_count=0
	curpage = 1
	kzzlist = []
	content=''
	totalpage = 0
	while 1:
		req_count += 1
		if req_count>10:
			break

		content = getKZZConnect(urlfmt, send_headers, curpage)
		if content=='':
			break
		dataObj = re.match('^iGeILSKk={pages:(\d+),data:\[(.*)\]}', content)
		if dataObj is None:
			print "Content format not match"
			break
		if totalpage < 1:
			totalpage = int(dataObj.group(1))
		if curpage>totalpage:
			break
		curpage += 1
		#���������ÿһ������
		getFilterZhai(dataObj.group(2), 1, kzzlist)
		#print curpage, totalpage
		#break

	if len(kzzlist)==0:
		print "Not find data"
		exit()

	keylist = ['BONDCODE','SNAME','ZQNEW','YJL','ZGJZGJJZ','ZGJ_HQ','SWAPSCODE','SECURITYSHORTNAME','ZGJZGJ']
	kzzdf = pd.DataFrame(kzzlist, columns=keylist)
	export_ebk(kzzdf)
