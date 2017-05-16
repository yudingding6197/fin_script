#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import time
import datetime
import tushare as ts

'''
    获取k线数据
    ---------
    Parameters:
      code:string
                  股票代码 e.g. 600848
      start:string
                  开始日期 format：YYYY-MM-DD 为空时取上市首日
      end:string
                  结束日期 format：YYYY-MM-DD 为空时取最近一个交易日
      ktype：string
                  数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
      autype:string
                  复权类型，qfq-前复权 hfq-后复权 None-不复权，默认为qfq
      index:bool
                  True or False 是否是指数
      retry_count : int, 默认 3
                 如遇网络等问题重复执行的次数 
      pause : int, 默认 0
                重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
    return
    -------
      DataFrame
          date 交易日期 (index)
          open 开盘价
          high  最高价
          close 收盘价
          low 最低价
          volume 成交量
          amount 成交额
          turnoverratio 换手率
          code 股票代码
'''
	
pindex = len(sys.argv)
code='300611'
if pindex==2:
	code = sys.argv[1]

LOOP_COUNT=0
while LOOP_COUNT<3:
	try:
		df = ts.get_k_data(code)
	except:
		LOOP_COUNT += 1
		time.sleep(0.5)
	else:
		break;
if df is None:
	print "Timeout to get hist data"
	exit(0)

print df.head(10)

df1 = df.sort_index(ascending=False)
print "\nReverse:"
print df1.head(10)
