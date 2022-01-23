#!/usr/bin/env python
# -*- coding:utf8 -*-

'''
#两种方法获取函数名称：
#1.通过系统函数
#2.通过inspect模块

获取当前文件名:

'''

import os
import sys
import inspect
from datetime import *

##############################1.
def a():
	print "_____",sys._getframe().f_code.co_name,":",sys._getframe().f_lineno


################################# 2. inspect模块
def get__function_name():
    '''获取正在运行函数(或方法)名称'''
    return inspect.stack()[1][3]

def yoyo():
    print("function name: %s"%get__function_name())

class Yoyo():
    def yoyoketang(self):
        print("Get class and function: %s.%s" % (self.__class__.__name__, get__function_name()))

def get_head_info():
	try:
		raise Exception
	except:
		f = sys.exc_info()[2].tb_frame.f_back
	return '%s, %s, %s, %s, ' % (str(datetime.now()), f.f_code.co_filename, f.f_code.co_name, str(f.f_lineno))

def call_func():
	print '%s --> skdkjzz' % (get_head_info())

if __name__ == "__main__":
	yoyo()
	Yoyo().yoyoketang()

	#外部获取
	print(a.__name__)
	a()
	
	call_func()
	
	print ("获取当前文件名".decode('utf8'))
	name=os.path.basename(__file__)
	print(name)

	print ("去掉文件后缀，只要文件名称".decode('utf8'))
	name=os.path.basename(__file__).split(".")[0]
	print(name)