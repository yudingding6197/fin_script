#!/usr/bin/env python
# -*- coding: gbk -*-
import sys
import os
from internal.tingfupai import * 
from internal.url_juchao.tips_res import *
from internal.url_dfcf.dc_hq_push import *
from internal.trade_date import *

kLine='kline_dayhfq'
def fetch_kday_page_qq(url):  #获取页面数据
	req=urllib2.Request(url,headers={
		'Connection': 'Keep-Alive',
		'Accept': 'text/html, application/xhtml+xml, */*',
		'Accept-Language':'zh-CN,zh;q=0.8',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
	})
	LOOP_COUNT = 0
	opener = None
	while LOOP_COUNT<3:
		try:
			opener=urllib2.urlopen(req)
		except:
			LOOP_COUNT += 1
			time.sleep(1)
		else:
			break
	if opener is None:
		return None
	
	content = opener.read()
	respInfo = opener.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
		#print "Content compressed"
		content = zlib.decompress(content, 16+zlib.MAX_WBITS);
	return content


def get_index_history_byQQ(location, index_temp):
	"""
	:param index_temp: for example, 'sh000001' 上证指数
	:return:
	"""
	index_type=index_temp[0:2]
	index_id=index_temp[2:]
	if index_type=='sh':
		index_id='0'+index_id
	if index_type=="sz":
		index_id='1'+index_id
	#url='http://quotes.money.163.com/service/chddata.html?code=%s&start=19900101&
	#end=%s&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER'%(index_id,time.strftime("%Y%m%d"))
	#url='http://img1.money.126.net/data/hs/kline/day/times/%s.json'%(index_id)
	url = 'https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayhfq&param=sh000001,day,,,30,hfq&r=0.9860043111257255'
	#print('netease js', url)

	page=fetch_kday_page_qq(url)
	#print page[:300]
	#print "pp", type(page)
	if page is None:
		return -1
	page = page[len(kLine)+1:]
	#print page[0:100]
	#print page[-50:]
	dictObj = json.loads(page);
	#print dictObj['data']
	#print "\n\n"
	shDayData = dictObj['data']['sh000001']['day']

	#print page
	#json.dumps(page.encode('gbk'))
	shDayList = []
	for item in reversed(shDayData):
		shDayList.append(item[0])
	file = open('_test.json','w')
	json.dump(shDayList, file)
	file.close()
	
	file = open('_test.json','r')
	info = json.load(file)
	file.close()
	
	print type(info)
	print info[0]
	print info[-1]
	
	#with open("./internal/db/"+index_temp+"_json.txt", "wb") as code:     
	#	code.write(page)
	#page.to_csv('_a.csv')
	return 0


#Main Start:
if __name__=='__main__':
	#pre_day = read_preday_json(days, cur_day)
	dt= get_preday(0)
	print dt;
	location = '_cur_json.txt'
	index_temp = 'sh000001'
	get_index_history_byQQ(location, index_temp)
	
	