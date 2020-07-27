#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import time
import string
import datetime

yzzt_list = ['603345','603238','000520','300613','300608','300553','603615']
add_list = ['002815','300291']

if __name__=="__main__":
	#通过extend方法追加，不能使用append
	yzzt_list.extend(add_list)

	list = yzzt_list
	print '\n遍历列表方法2：'
	# 方法2
	for i in range(len(list)):
		print ("序号：%s   值：%s" % (i + 1, list[i]))

	# 方法3
	print '\n遍历列表方法3：'
	for i, val in enumerate(list):
		print ("序号：%s   值：%s" % (i + 1, val))

	# 方法3
	print '\n遍历列表方法3 （设置遍历开始初始位置，只改变了起始序号）：'
	for i, val in enumerate(list, 2):
		print ("序号：%s   值：%s" % (i + 1, val))
