#!/usr/bin/env python
# -*- coding:utf8 -*-
#1.没有星号的可变参数
#2.通过inspect模块

import sys
#没有星号，位置可以变动
def func1(a, b=5, c=10, src='sn'):
	print('a is', a, 'and b is', b, 'and c is', c, 'source=', src)

#可变参数原来是list、tuple、输出效果还不一样
def func2(a, *args):
	print('a is', a, "args type", type(args))
	for i in args:
		print(i)

#可变参数原来是list、tuple、输出效果还不一样
def func3(a, **kwargs):
	print('*kwargs:{0}'.format(kwargs))
	for k,val in kwargs.items():
		print(k,val)
		
if __name__ == "__main__":
	func1(src='qq', a=3, c=6, b=7)
	func1(25, c=24)
	func1(c=50, src='wy', a=100)

	list = [1, 2, 4]
	func2("aa", list)
	tuple = (11, 12, 13)
	func2("aa", tuple)

	#参数传入时候，字典类型加上两个 **
	dict={'name':'ganin','age':18}
	func3("aa", **dict)
	func3("bb", k1=1,k2='123',k3=12.4)
	