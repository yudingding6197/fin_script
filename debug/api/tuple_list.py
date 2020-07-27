#!/usr/bin/env python
# -*- coding:utf8 -*-
'''
1.相对于 list 而言，tuple 是不可变的，这使得它可以作为 dict 的 key，或者扔进 set 里，而 list 则不行。
2.tuple 放弃了对元素的增删（内存结构设计上变的更精简），换取的是性能上的提升：创建 tuple 比 list 要快，
存储空间比 list 占用更小。所以就出现了“能用 tuple 的地方就不用 list”的说法。
3.多线程并发的时候，tuple 是不需要加锁的，不用担心安全问题，编写也简单多了

不可变类型:tuple ,constant
可变类型：list dict set
同理字典的key也不能为不可变类型
'''

if __name__ == "__main__":
	temp = ()
	print (type(temp))
	#元组里只有一个元素的时候，逗号（，）非常重要
	print (8 * (8,))
	
	list = [1, 2, 3, 4]
	tuple = (5, 6, 7)
	for i in list:
		print(i)
	#print ("\n")
	for j in tuple:
		print(j)
