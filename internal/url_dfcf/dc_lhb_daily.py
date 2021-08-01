#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import urllib2
import httplib2
import json
import zlib
import random

def get_lhb_dfcf(urllink, send_headers1):
	#print (urllink)
	#print (send_headers1)
	res_data = None
	#tf_fl = open(filename, 'w+')
	LOOP_COUNT = 0
	while LOOP_COUNT<3:
		try:
			#访问该站点时间比较长，加大timeout
			req = urllib2.Request(urllink,headers=send_headers1)
			res_data = urllib2.urlopen(req, timeout=10)
		except Exception as e:
			if LOOP_COUNT==2:
				print "Error:", e
				#print "Error get_lhb_dc urlopen"
			LOOP_COUNT = LOOP_COUNT+1
		else:
			break

	#print res_data
	if res_data is None:
		print "Open get_lhb_dc URL fail"
		return ""

	content = res_data.read()
	respInfo = res_data.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
		#print "Content compressed"
		content = zlib.decompress(content, 16+zlib.MAX_WBITS);
	#else:
	#	print "Content not zip"
	#print content.decode('utf8')
	#print content[:10]
	content = content[len(jsPre)+1:-1]

	#tf_fl.write(content)
	#tf_fl.close()
	return content

def get_lhb_dfcf_http(urllink, send_headers1):
	#print (urllink)
	#print (send_headers1)
	res_data = None
	#tf_fl = open(filename, 'w+')
	LOOP_COUNT = 0
	
	while LOOP_COUNT<3:
		try:
			ghttp = httplib2.Http()
			#httplib2.debuglevel=1
			res_data,page= ghttp.request(urllink,headers=send_headers1)
		except Exception as e:
			print "Error:", e
			if LOOP_COUNT==2:
				print "Error get_lhb_dc urlopen"
			LOOP_COUNT = LOOP_COUNT+1
			break
		else:
			break

	#print res_data
	if res_data is None:
		print "Open get_lhb_dc URL fail"
		return ""
	#print res_data
	content = page
	#print page[:30]
	return content

def get_lhb_dtl_dfcf(urllink, send_headers1):
	#print (urllink)
	res_data = None
	LOOP_COUNT = 0
	while LOOP_COUNT<3:
		try:
			req = urllib2.Request(urllink,headers=send_headers1)
			res_data = urllib2.urlopen(req, timeout=2)
		except Exception as e:
			if LOOP_COUNT==2:
				print "Error:", e
				#print "Error get_lhb_dc urlopen"
			LOOP_COUNT = LOOP_COUNT+1
		else:
			break

	#print res_data
	if res_data is None:
		print "Open get_lhb_dc detail URL fail"
		return ""

	content = res_data.read()
	respInfo = res_data.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
		#print "Content compressed"
		content = zlib.decompress(content, 16+zlib.MAX_WBITS);
	#else:
	#	print "Content not zip"
	content = content[len(jsPre)+1:-1]
	#print content[20:100]
	return content


'''
排序通过 'sortColumn',默认可以不需要参数 'sortColumn=&...', 可以通过 ClosePrice,Chgradio,sMoney等多个项进行排序

GET /EM_DataCenter_V3/api/LHBGGDRTJ/GetLHBGGDRTJ?js=jQuery112302601345365016676_1625841072203&sortColumn=&sortRule=1&pageSize=500&pageNum=1&tkn=eastmoney&dateNum=&cfg=lhbggdrtj&mkt=0&startDateTime=2021-07-08&endDateTime=2021-07-08 HTTP/1.1
Host: datainterface3.eastmoney.com
Connection: keep-alive
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: qgqp_b_id=015901ad7a28161a23978a92c401c684; intellpositionL=1010.67px; ct=Hix2I46MjD-xnmnI4-FCwZtlm5aiY1FBlVVkT7hOyl0TrTZ23_P-NSbz7tjzNGFcdtZVweKOFhs109FLlfBUIa0XtIl5Q0PXaBV_-B02KIKIODNMb1wdXDJqTn-39GOCfSJexm78mmU_Q6OVkDWXjDUNq5seZcMyJ4x19tU41h4; ut=FobyicMgeV5FJnFT189SwAVHQcnCViDRQ6qT5n733e5mQvT0mDaLePCeFbDolrGSKi3hwCSAahpSz-9o-uWSUURwMsE4COV3J8u-9lNP0B9y_vM8VfNcIoVDJwgTsAAMiS6EDF7G931Ufsf7yna4BxRT8PvpqyDJmEYFVZ6OrR9Qo5wyrY-K3kqmQhEuiZU3blfrQjQtq3sr2o3Q7EhIHKs7XmlceEdFwalMKr56-2Xnoe0NnTxujr_UJj_verPA1EWM4fwxPQgfGyKz4WaqoVu7E1ivgErznh9PHJIi7iGqcobX5hEwIFhkZkReVrho9nwPzSEe4OGVTKMK8n95d9W4pwL49san; pi=6100112247957528%3byudingding6197%3bgoutou%3bn1OcxrtieBSLqyWvw85AOiXce1VZjUBvwowTmZcB8bRYti0XAQXSBHObfm4O12CNyigFTNhD6tcK10sF9Nn6JofAUoFKHyl0hTz%2b1kRniVtMwwSvAqlj3iRBvcDHwOoECmbgaPXWxnAWHCwB7gM4GN1mi52gb%2fr0w5IyTc%2bFNVzViAUmDzo1C5heIlF8EMTnBxX4puWK%3btn0B6oPKj3z%2f%2b%2fgTpxkuIxkH18QRRvoHNB0%2b4sqCss74EDlbalkr0YWYKv114pgEVgiin86M%2bnpAp20XFtlaYZyXfS5mWccW9FW1nM%2fY1xYro6%2b1y90wMu3Nz9uVXcoeTlL7cYWuiJCVthC5xL6Z%2fnCLncaD1w%3d%3d; uidal=6100112247957528goutou; sid=4725419; vtpst=|; em_hq_fls=js; em-quote-version=topspeed; cowCookie=true; HAList=a-sz-300291-%u534E%u5F55%u767E%u7EB3%2Ca-sh-603987-%u5EB7%u5FB7%u83B1%2Cf-0-399006-%u521B%u4E1A%u677F%u6307%2Cf-0-399001-%u6DF1%u8BC1%u6210%u6307%2Cf-0-000001-%u4E0A%u8BC1%u6307%u6570%2Ca-sz-300553-%u96C6%u667A%u80A1%u4EFD%2Ca-sz-002247-%u805A%u529B%u6587%u5316%2Ca-sz-002679-%u798F%u5EFA%u91D1%u68EE%2Ca-sh-603958-%u54C8%u68EE%u80A1%u4EFD%2Ca-sh-600760-%u4E2D%u822A%u6C88%u98DE%2Ca-sh-603324-%u76DB%u5251%u73AF%u5883%2Ca-sz-300432-%u5BCC%u4E34%u7CBE%u5DE5; cowminicookie=true; intellpositionT=655px; st_pvi=92457965025484; st_inirUrl=https%3A%2F%2Fpassport2.eastmoney.com%2Fpub%2Flogin; st_sp=2021-06-14%2014%3A12%3A01

'DNT': 1,
'Cache-Control': 'max-age=0',
'Cookie': 'qgqp_b_id=015901ad7a28161a23978a92c401c684; intellpositionL=1010.67px; ct=Hix2I46MjD-xnmnI4-FCwZtlm5aiY1FBlVVkT7hOyl0TrTZ23_P-NSbz7tjzNGFcdtZVweKOFhs109FLlfBUIa0XtIl5Q0PXaBV_-B02KIKIODNMb1wdXDJqTn-39GOCfSJexm78mmU_Q6OVkDWXjDUNq5seZcMyJ4x19tU41h4; ut=FobyicMgeV5FJnFT189SwAVHQcnCViDRQ6qT5n733e5mQvT0mDaLePCeFbDolrGSKi3hwCSAahpSz-9o-uWSUURwMsE4COV3J8u-9lNP0B9y_vM8VfNcIoVDJwgTsAAMiS6EDF7G931Ufsf7yna4BxRT8PvpqyDJmEYFVZ6OrR9Qo5wyrY-K3kqmQhEuiZU3blfrQjQtq3sr2o3Q7EhIHKs7XmlceEdFwalMKr56-2Xnoe0NnTxujr_UJj_verPA1EWM4fwxPQgfGyKz4WaqoVu7E1ivgErznh9PHJIi7iGqcobX5hEwIFhkZkReVrho9nwPzSEe4OGVTKMK8n95d9W4pwL49san; pi=6100112247957528%3byudingding6197%3bgoutou%3bn1OcxrtieBSLqyWvw85AOiXce1VZjUBvwowTmZcB8bRYti0XAQXSBHObfm4O12CNyigFTNhD6tcK10sF9Nn6JofAUoFKHyl0hTz%2b1kRniVtMwwSvAqlj3iRBvcDHwOoECmbgaPXWxnAWHCwB7gM4GN1mi52gb%2fr0w5IyTc%2bFNVzViAUmDzo1C5heIlF8EMTnBxX4puWK%3btn0B6oPKj3z%2f%2b%2fgTpxkuIxkH18QRRvoHNB0%2b4sqCss74EDlbalkr0YWYKv114pgEVgiin86M%2bnpAp20XFtlaYZyXfS5mWccW9FW1nM%2fY1xYro6%2b1y90wMu3Nz9uVXcoeTlL7cYWuiJCVthC5xL6Z%2fnCLncaD1w%3d%3d; uidal=6100112247957528goutou; sid=4725419; vtpst=|; em_hq_fls=js; em-quote-version=topspeed; cowCookie=true; st_si=05905368457166; HAList=a-sz-300291-%u534E%u5F55%u767E%u7EB3%2Ca-sh-603987-%u5EB7%u5FB7%u83B1%2Cf-0-399006-%u521B%u4E1A%u677F%u6307%2Cf-0-399001-%u6DF1%u8BC1%u6210%u6307%2Cf-0-000001-%u4E0A%u8BC1%u6307%u6570%2Ca-sz-300553-%u96C6%u667A%u80A1%u4EFD%2Ca-sz-002247-%u805A%u529B%u6587%u5316%2Ca-sz-002679-%u798F%u5EFA%u91D1%u68EE%2Ca-sh-603958-%u54C8%u68EE%u80A1%u4EFD%2Ca-sh-600760-%u4E2D%u822A%u6C88%u98DE%2Ca-sh-603324-%u76DB%u5251%u73AF%u5883%2Ca-sz-300432-%u5BCC%u4E34%u7CBE%u5DE5; st_asi=delete; intellpositionT=755px; st_pvi=92457965025484; st_sp=2021-06-14%2014%3A12%3A01; st_inirUrl=https%3A%2F%2Fpassport2.eastmoney.com%2Fpub%2Flogin; st_sn=14; st_psi=20210709121141172-113300301653-6394390871'
'Upgrade-Insecure-Requests':1,
'Connection':'keep-alive',
'''

jsPre = "jQuery112302601345365016676_1625841072203"
urlfmt="http://datainterface3.eastmoney.com/EM_DataCenter_V3/api/LHBGGDRTJ/GetLHBGGDRTJ?\
js=%s&sortColumn=%s&sortRule=1&pageSize=500&pageNum=1&tkn=eastmoney&dateNum=&cfg=lhbggdrtj&mkt=0&startDateTime=%s&endDateTime=%s"
send_headers = {
'Host':'datainterface3.eastmoney.com',
'Cache-Control':'max-age=0',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cookie':'qgqp_b_id=015901ad7a28161a23978a92c401c684; intellpositionL=1010.67px; ct=Hix2I46MjD-xnmnI4-FCwZtlm5aiY1FBlVVkT7hOyl0TrTZ23_P-NSbz7tjzNGFcdtZVweKOFhs109FLlfBUIa0XtIl5Q0PXaBV_-B02KIKIODNMb1wdXDJqTn-39GOCfSJexm78mmU_Q6OVkDWXjDUNq5seZcMyJ4x19tU41h4; ut=FobyicMgeV5FJnFT189SwAVHQcnCViDRQ6qT5n733e5mQvT0mDaLePCeFbDolrGSKi3hwCSAahpSz-9o-uWSUURwMsE4COV3J8u-9lNP0B9y_vM8VfNcIoVDJwgTsAAMiS6EDF7G931Ufsf7yna4BxRT8PvpqyDJmEYFVZ6OrR9Qo5wyrY-K3kqmQhEuiZU3blfrQjQtq3sr2o3Q7EhIHKs7XmlceEdFwalMKr56-2Xnoe0NnTxujr_UJj_verPA1EWM4fwxPQgfGyKz4WaqoVu7E1ivgErznh9PHJIi7iGqcobX5hEwIFhkZkReVrho9nwPzSEe4OGVTKMK8n95d9W4pwL49san; pi=6100112247957528%3byudingding6197%3bgoutou%3bn1OcxrtieBSLqyWvw85AOiXce1VZjUBvwowTmZcB8bRYti0XAQXSBHObfm4O12CNyigFTNhD6tcK10sF9Nn6JofAUoFKHyl0hTz%2b1kRniVtMwwSvAqlj3iRBvcDHwOoECmbgaPXWxnAWHCwB7gM4GN1mi52gb%2fr0w5IyTc%2bFNVzViAUmDzo1C5heIlF8EMTnBxX4puWK%3btn0B6oPKj3z%2f%2b%2fgTpxkuIxkH18QRRvoHNB0%2b4sqCss74EDlbalkr0YWYKv114pgEVgiin86M%2bnpAp20XFtlaYZyXfS5mWccW9FW1nM%2fY1xYro6%2b1y90wMu3Nz9uVXcoeTlL7cYWuiJCVthC5xL6Z%2fnCLncaD1w%3d%3d; uidal=6100112247957528goutou; sid=4725419; vtpst=|; em_hq_fls=js; em-quote-version=topspeed; cowCookie=true; HAList=a-sz-300291-%u534E%u5F55%u767E%u7EB3%2Ca-sh-603987-%u5EB7%u5FB7%u83B1%2Cf-0-399006-%u521B%u4E1A%u677F%u6307%2Cf-0-399001-%u6DF1%u8BC1%u6210%u6307%2Cf-0-000001-%u4E0A%u8BC1%u6307%u6570%2Ca-sz-300553-%u96C6%u667A%u80A1%u4EFD%2Ca-sz-002247-%u805A%u529B%u6587%u5316%2Ca-sz-002679-%u798F%u5EFA%u91D1%u68EE%2Ca-sh-603958-%u54C8%u68EE%u80A1%u4EFD%2Ca-sh-600760-%u4E2D%u822A%u6C88%u98DE%2Ca-sh-603324-%u76DB%u5251%u73AF%u5883%2Ca-sz-300432-%u5BCC%u4E34%u7CBE%u5DE5; cowminicookie=true; intellpositionT=655px; st_pvi=92457965025484; st_inirUrl=https%3A%2F%2Fpassport2.eastmoney.com%2Fpub%2Flogin; st_sp=2021-06-14%2014%3A12%3A01'
}

def fetch_dfcf_lhb_summary(sdate, edate, sortKey):
	if sdate!=edate:
		print("%s %s date not the same")
		return ''
	urlall = urlfmt % (jsPre, sortKey, sdate, edate)
	return get_lhb_dfcf(urlall, send_headers)

jsPreDtl="jQuery112309774114609775966_1625968390626"
urlfmt_dtl="http://datainterface3.eastmoney.com/EM_DataCenter_V3/api/LHBMMMX/GetLHBMXKZ?\
tkn=eastmoney&Code=%s&dateTime=%s&pageNum=1&pageSize=50&cfg=lhbmxkz&js=%s&_=1625968390628"
def fetch_lhb_stk_detail(scode, curDate):
	urlall = urlfmt_dtl % (scode, curDate, jsPreDtl)
	return get_lhb_dtl_dfcf(urlall, send_headers)
	
#Main
if __name__=='__main__':
	dt = '2021-07-06'
	urlall = urlfmt % (jsPre, '', dt, dt)
	get_lhb_dfcf(urlall, send_headers)

