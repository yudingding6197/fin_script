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

	lists = [[]] * 3
	print lists
	lists[0].append(3)
	print lists
	# 3列数组的值同时更新 [[3], [3], [3]]

	lists = [[] for i in range(3)]
	lists[0].append(3)
	print lists
	lists[1].append(7)
	print lists
	
	#二维数组创建方式修改为
	myList = [([0] * 3) for i in range(4)]
	print myList
	
	num_list = [0,1,2,3,4,5,6,7,8,9]
	num_list_new = [str(x) for x in num_list]
	print ",".join(num_list_new)

	num_list = ['aa','cc',1,2,3,4,5,6,7,8,9]
	num_list_new = map(lambda x:str(x), num_list)
	print ",".join(num_list_new)	