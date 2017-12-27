#!/usr/bin/env python
# -*- coding:utf8 -*-

#数组长度10，每一个元素值为2
array = [2] * 10
array[3] = 56
print array

# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
a = range(0, 15)
print a

#定义18个值为1的数组, 此定义等同 array = [2] * 10
a = [1 for x in range(0, 18)]
print a

#二维数组 3*5,每一个元素仍然是一个数组[]
#注意此时1个数组更新，其它都会更新，这样不太好
array = [[[]]*3]*5
print array
for i in range(0,5):
	for j in range(0,3):
		print array[i][j]
	print '===='

#定义长度为6的数组，每一个元素仍是数组[]
#等同手写 [[], [], [], [], [], []]
a = [[] for x in range(6)]
print a
b = []
b.append('b1')
b.append('b2')
a[0].append(b)
print a[0]
print a[1]

c=[]
c.append('c1')
c.append('c2')
a[1].append(c)
print a[0]
print a[1]


#这个空数组，没有意义
array = [] * 10
print array


