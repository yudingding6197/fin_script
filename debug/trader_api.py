# -*- coding:gbk -*-
import os
import tushare as ts

#ts.get_today_all()

ts.set_broker('zxjt', user='40092000', passwd='test1234')
brk = ts.get_broker()
print brk

csc = ts.TraderAPI('zxjt')
csc.login()

baseinfo = csc.baseinfo()
print baseinfo