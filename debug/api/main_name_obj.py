#!/usr/bin/env python
# -*- coding:utf8 -*-

'''
__name__ 是python的内置变量，是有值的
main_name可以作为模块被导入，其它模块可以使用它的方法
'''


def f1():
	print "Main_Name_Obj call function f1()"
	pass

print "Main_Name_Obj Always be called, __name__=", __name__
if __name__=="__main__":
#	print "__name__ is a variable: ", __name__
	print "Main_Name_Obj called by self"
