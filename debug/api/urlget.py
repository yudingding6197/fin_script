#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import os
import time
import urllib2
from urllib2 import urlopen, Request

if __name__ == '__main__':
	#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
	#req = urllib.request.Request(url = uurl, headers = headers)
	#html = urllib.request.urlopen(req).read()
	headers = {
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language':'zh-CN,zh;q=0.8',
           'User-Agent': "Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Cookie": "Hm_lvt_1db88642e346389874251b5a1eded6e3=1494144055,1494249821,1494260397,1494341723; s=6g1zme2dl3; bid=538fbe5da1256c6f563b0b17f085a4dd_ivgwipkx; __utma=1.1121673574.1479057278.1494005316.1494341725.115; __utmz=1.1489846134.62.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; webp=0; xq_a_token=3190c4006bf03f3a7b7d0fbf575da4e9a89af050; xq_r_token=38ed7ebde6f04cac70cd3506ab5a15ce34238abd; u=9211149269; remember=1; remember.sig=K4F3faYzmVuqC0iXIERCQf55g2Y; xq_a_token.sig=DR4DNLY4JXEaZICv1SOw3vbGr6g; xq_r_token.sig=rl-HGGCCi-Qr9ffevkCwp1vYBA8; xq_is_login=1; xq_is_login.sig=J3LxgPVPUzbBg3Kee_PquUfih7Q; u.sig=dqKk2-xAcVY7PcHekAZ_iHyDTck; aliyungf_tc=AQAAAH127GlatAUAkz5HebRBlGAJovqj; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1494341723; __utmc=1",
           "Cache-Control": "no-cache"}
	uurl = 'https://xueqiu.com/stock/get_div_history_by_symbol.json?symbol=02328&_=1494321133983'
	req = urllib2.Request(uurl, headers=headers)
	res_data = urllib2.urlopen(req)

	line = res_data.readline()
	while line:
		print line
		line = res_data.readline()

	request = Request("https://www.baidu.com/")
	text = urlopen(request,timeout=10).read()
	print "==================== GET LINK FROM:", request.get_full_url()
	print text

