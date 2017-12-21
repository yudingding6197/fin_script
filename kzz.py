#!/usr/bin/env python
# -*- coding:gbk -*-
#可转债
import sys
import re
import os
import string
import urllib
import urllib2
import datetime
import binascii
import shutil
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook
from internal.common import *
from internal.ts_common import *

'''
urlall = "http://data.eastmoney.com/kzz/default.html"

http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=KZZ_LB&token=70f12f2f4f091e459a279469fe49eca5&cmd=&st=STARTDATE&sr=-1&p=2&ps=50&js=var%20fnhOGnNf={pages:(tp),data:(x)}&rt=50462432
curl 'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=KZZ_LB&token=70f12f2f4f091e459a279469fe49eca5&cmd=&st=STARTDATE&sr=-1&p=2&ps=50&js=var%20ShTNyQGa=\{pages:(tp),data:(x)\}&rt=50462435' -H 'Referer: http://data.eastmoney.com/kzz/default.html' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2986.0 Safari/537.36' --compressed ;
curl 'http://datapic.eastmoney.com/img/loading.gif' -H 'Referer: http://data.eastmoney.com/kzz/default.html' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2986.0 Safari/537.36' --compressed


GET /em_mutisvcexpandinterface/api/js/get?type=KZZ_LB&token=70f12f2f4f091e459a279469fe49eca5&cmd=&st=STARTDATE&sr=-1&p=2&ps=50&js=var%20AgXbfCEA={pages:(tp),data:(x)}&rt=50462437 HTTP/1.1
Host: dcfm.eastmoney.com
Connection: keep-alive
User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2986.0 Safari/537.36
Accept: */*
Referer: http://data.eastmoney.com/kzz/default.html
Accept-Encoding: gzip, deflate, sdch
Accept-Language: zh-CN,zh;q=0.8
Cookie: st_pvi=58966067871551; emstat_bc_emcount=3865031455203490824; _ga=GA1.2.489496839.1490373062; Hm_lvt_557fb74c38569c2da66471446bbaea3f=1490369131,1491722493; HAList=a-sz-000856-%u5180%u4E1C%u88C5%u5907%2Ca-sh-600806-*ST%u6606%u673A; em_hq_fls=old; emstat_ss_emcount=4_1502572827_1781470105; st_si=41212368779108; qgqp_b_id=ecd1ebeb62127dedf2441c0dd9c1b689
'''


#Main
if __name__=="__main__":
	curdate = ''
	bLast = 0
	curdate, bLast = get_date_with_last()
	print curdate, bLast

