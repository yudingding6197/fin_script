#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import re
import os
import math
import urllib
import urllib2
import json
import codecs
import zlib

'''
POST /new/hisAnnouncement/query HTTP/1.1
Host: www.cninfo.com.cn
Connection: keep-alive
Content-Length: 199
Accept: */*
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Origin: http://www.cninfo.com.cn
Referer: http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search&lastPage=index
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: JSESSIONID=55ACA1E2D6CA94716DC12354256B03AC; _sp_ses.2141=*; routeId=.uc2; _sp_id.2141=0f67e811-5fd8-439a-90ed-6ad30ab84d28.1623653028.14.1627789761.1627743326.1579e706-beab-4e2d-b3ff-64e77cacb2b6

'Cookie': 'JSESSIONID=B9E1E85A37F271B92760CF1FCD7ED182; _sp_ses.2141=*; \
UC-JSESSIONID=340076282D503D578A949A08D2C2E1E4; \
_sp_id.2141=e928beb2-1d59-40f9-92d7-b8405ba01a70.1555939861.43.1596898781.1596870082.83e1d89f-5881-4648-a7f9-47e7150b6197',
'''

jc_headers = {
'Host': 'www.cninfo.com.cn',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Accept': 'application/json, text/plain, */*',
'Accept-Encoding': 'gzip, deflate',
'Origin': 'http://www.cninfo.com.cn',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
'Referer': 'http://www.cninfo.com.cn/new/commonUrl?url=disclosure/tradingTips',
'Accept-Language': 'zh-CN,zh;q=0.8',
'Cookie': 'JSESSIONID=55ACA1E2D6CA94716DC12354256B03AC; _sp_ses.2141=*; routeId=.uc2; _sp_id.2141=0f67e811-5fd8-439a-90ed-6ad30ab84d28.1623653028.14.1627789761.1627743326.1579e706-beab-4e2d-b3ff-64e77cacb2b6',
}
urlall = "http://www.cninfo.com.cn/new/hisAnnouncement/query"

def filter_hecha_item(listItem, listObj):
	word1 = u"<em>停牌</em><em>核查</em>的公告"
	word2 = u"<em>停牌</em><em>核查</em>公告"
	word3 = u"<em>核查</em>的<em>停牌</em>公告"
	word4 = u"<em>核查</em>及<em>停牌</em>"
	for item in listObj:
		#print item['secCode'],item['secName'],item['adjunctUrl'],item['announcementTitle']
		if item['announcementTitle'].find(word1)>0 or \
			item['announcementTitle'].find(word2)>0 or \
			item['announcementTitle'].find(word3)>0 or \
			item['announcementTitle'].find(word4)>0 :
			#print "FFFFFFFFFF"
			#print item['secCode'],item['secName'],item['adjunctUrl'],item['announcementTitle']
			listItem.append(item)
	
def fetch_yidong_byPage(curDict):
	data = urllib.urlencode(curDict)
	LOOP_COUNT = 0
	res_data=None
	#print('tingfup', urlall)
	while LOOP_COUNT<3:
		try:
			req = urllib2.Request(urlall, data)
			res_data = urllib2.urlopen(req)
		except:
			LOOP_COUNT = LOOP_COUNT+1
			if LOOP_COUNT==3:
				print("Error yidong",urlall)
		else:
			break
	if res_data is None:
		print("Invalid data", urlall, curDict["pageNum"])
		return None

	content = res_data.read()
	respInfo = res_data.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
		print "Content compressed"
		content = zlib.decompress(content, 16+zlib.MAX_WBITS)
	return content
	
def fetch_yidong_hecha(filename, searchkey, startDate, endDate):
	#pageNum=1&pageSize=20&column=szse&tabName=fulltext&plate=&stock=&
	#	searchkey=%E5%81%9C%E7%89%8C%E6%A0%B8%E6%9F%A5&secid=&category=&trade=&seDate=2018-01-01~2020-12-31&
	#	sortName=&sortType=&isHLtitle=true
	pSize = 30	
	hcDict = {'pageNum':1,'pageSize':pSize,'column':'szse','tabName':'fulltext','plate':'','stock':'',
		'secid':'','category':'','trade':'',
		'sortName':'time','sortType':'asc','isHLtitle':'true'}
	hcDict['searchkey'] = searchkey
	seDt = "%s~%s"%(startDate,endDate)
	hcDict['seDate'] = seDt
	content = fetch_yidong_byPage(hcDict)
	if content is None:
		return

	obj = json.loads(content)
	listItem = []
	filter_hecha_item(listItem, obj["announcements"])
	totalLen = obj["totalRecordNum"]
	maxPage=totalLen/pSize + 1 if totalLen%pSize>0 else 0
	for page in range(1,maxPage):
		hcDict['pageNum'] = page+1
		content = fetch_yidong_byPage(hcDict)
		obj = json.loads(content)
		filter_hecha_item(listItem, obj["announcements"])
		#print ( len(listItem) )

	fp = codecs.open(filename, 'w+', 'utf-8')
	fp.write(json.dumps(listItem,ensure_ascii=False))
	fp.close()

if __name__=="__main__":
	plen=len(sys.argv)
	if plen<=1:
		td = '2020-08-16'
	else:
		td = sys.argv[1]
	print "tradate", td
	
	cnt = get_trade_tips(td)
	print cnt
	dict = json.loads(cnt)
	print dict['clusterSRTbTrade0112']['queryDate']
	print dict['clusterSRTbTrade0112']['srTbTrade0112s']
	
	#file = open("_test.log", 'w')
	#json.dump(dict['clusterSRTbTrade0112']['srTbTrade0112s'], file)
	#file.close()
