#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import urllib
import urllib2
import json
import zlib

#from global_var import g_shcd
#from global_var import g_szcd

'''
#
{u'obModtime0111': 1595424980000L, 
u'obIsvalid0111': u'1', 
u'obRectime0111': 1595424980000L, 
u'f010v0111': u'Delisting Risk Warning Removal Announcement/Delisting Risk Warning Removal/Risk Warning', 
u'obSeqId': 6115954884L, 
u'lastMtime': 1595424984000L, 
u'obSeccode0111': u'000611', 
u'f004v0111': u'\u505c\u724c1\u5929', 
u'f001d0111': 1595467800000L, 
u'f006v0111': u'A\u80a1', 
u'f002d0111': 1595554200000L, 
u'tradeType': None, 
u'f005v0111': u'\u64a4\u9500\u9000\u5e02\u98ce\u9669\u8b66\u793a\u516c\u544a', 
u'f009v0111': u'Trading Suspension for 1 Day', u'obMemo0111': None, 
u'obSecname0111': u'*ST\u5929\u9996', 
u'f007v0111': u'001001', 
u'obObjectId': 1001126068
}
{
"date":"2020-07-24",
"error":null,
"szshSRTbTrade0111":
	{
	"suspensionTbTrades":[
		{"f001d0111":1595554200000,"obSeccode0111":"002473","obSecname0111":"圣莱达","f002d0111":1595813400000,"f004v0111":"停牌1天","f005v0111":"实行其他风险警示","obMemo0111":null,"obRectime0111":1595513775000,"obModtime0111":1595513775000,"obIsvalid0111":"1","obObjectId":1002380879,"f006v0111":"A股","f007v0111":"001001","obSeqId":6123826506,"f009v0111":"Trading Suspension for 1 Day","f010v0111":"Risk Warning","lastMtime":1595513778000,"tradeType":null},
		{"f001d0111":1595554201000,"obSeccode0111":"300853","obSecname0111":"N申昊","f002d0111":1595556002000,"f004v0111":null,"f005v0111":"盘中临时停牌","obMemo0111":null,"obRectime0111":1595555057000,"obModtime0111":1595555057000,"obIsvalid0111":"1","obObjectId":1002792209,"f006v0111":"A股","f007v0111":"001001","obSeqId":6127218036,"f009v0111":null,"f010v0111":null,"lastMtime":1595555062000,"tradeType":null},
	"resumptionTbTrades":[
		{
		"f001d0111":1595467800000,
		"obSeccode0111":"000611",
		"obSecname0111":"*ST天首",
		"f002d0111":1595554200000,
		"f004v0111":"停牌1天",
		"f005v0111":"撤销退市风险警示公告",
		"obMemo0111":null,
		"obRectime0111":1595424980000,
		"obModtime0111":1595424980000,
		"obIsvalid0111":"1",
		"obObjectId":1001126068,
		"f006v0111":"A股",
		"f007v0111":"001001",
		"obSeqId":6115954884,
		"f009v0111":"Trading Suspension for 1 Day",
		"f010v0111":"Delisting Risk Warning Removal Announcement/Delisting Risk Warning Removal/Risk Warning",
		"lastMtime":1595424984000,
		"tradeType":null
		}
		],
	"keepSuspensionTbTrades":null
	},
'''
jc_headers = {
'Host': 'www.cninfo.com.cn',
'Content-Length': 0,
'Accept': 'application/json, text/plain, */*',
'Accept-Encoding': 'gzip, deflate',
'Origin': 'http://www.cninfo.com.cn',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
'Referer': 'http://www.cninfo.com.cn/new/commonUrl?url=disclosure/tradingTips',
'Accept-Language': 'zh-CN,zh;q=0.8',
'Cookie': 'JSESSIONID=B9E1E85A37F271B92760CF1FCD7ED182; _sp_ses.2141=*; \
UC-JSESSIONID=340076282D503D578A949A08D2C2E1E4; \
_sp_id.2141=e928beb2-1d59-40f9-92d7-b8405ba01a70.1555939861.43.1596898781.1596870082.83e1d89f-5881-4648-a7f9-47e7150b6197',
}
def get_trade_tips(curdate):
	url = "http://www.cninfo.com.cn/new/information/memoQuery?queryDate="
	urlall = url + curdate
	dict = {}
	data = urllib.urlencode(dict)

	LOOP_COUNT = 0
	res_data=None
	#print('tingfup', urlall)
	#这是POST请求
	while LOOP_COUNT<3:
		try:
			req = urllib2.Request(urlall, data, headers=jc_headers)
			res_data = urllib2.urlopen(req)
		except:
			print "Error fupai urlopen"
			LOOP_COUNT = LOOP_COUNT+1
		else:
			break
	if res_data is None:
		return None

	content = res_data.read()
	respInfo = res_data.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
		#print "Content compressed"
		content = zlib.decompress(content, 16+zlib.MAX_WBITS)
	#print content
	return content

def get_tingfupai_res(curdate):
	url = "http://www.cninfo.com.cn/new/information/getSuspensionResumptions?queryDate="
	urlall = url + curdate
	dict = {}
	data = urllib.urlencode(dict)

	LOOP_COUNT = 0
	res_data=None
	#print('tingfup', urlall)
	#这是POST请求
	while LOOP_COUNT<3:
		try:
			req = urllib2.Request(urlall, data)
			res_data = urllib2.urlopen(req)
		except:
			#print "Error fupai urlopen"
			LOOP_COUNT = LOOP_COUNT+1
		else:
			break
	content = res_data.read()
	return content

if __name__=="__main__":
	cnt = get_trade_tips('2020-08-05')
	dict = json.loads(cnt)
	#print dict['clusterSRTbTrade0112']['queryDate']
	#print dict['clusterSRTbTrade0112']['srTbTrade0112s']
	
	file = open("_test.log", 'w')
	json.dump(dict['clusterSRTbTrade0112']['srTbTrade0112s'], file)
	file.close()
