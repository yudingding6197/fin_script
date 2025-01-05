#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import time
import string
import datetime
from operator import itemgetter, attrgetter

class Student:
	def __init__(self, name, grade, age):
		self.name = name
		self.grade = grade
		self.age = age
	def __repr__(self):
		return repr((self.name, self.grade, self.age))
				
if __name__=="__main__":
	student_tuples = [
        ('john', 'C', 15),
		('jane', 'B', 12),
		('dave', 'B', 10),
		('jeep', 'B', 13),
	]

	student_objects = [
        Student('john', 'A', 15),
        Student('jane', 'B', 12),
        Student('dave', 'B', 10),
	]
	
	#key参数的值为一个函数，此函数只有一个参数且返回一个值用来进行比较。
	#这个技术是快速的因为key指定的函数将准确地对每个元素调用。
	#更广泛的使用情况是用复杂对象的某些值来对复杂对象的序列排序
	print sorted(student_tuples, key=lambda student: student[2])

	#Operator 模块函数
	#上面的key参数的使用非常广泛，因此python提供了一些方便的函数来使得访问方法更加容易和快速。
	#operator模块有itemgetter，attrgetter，从2.6开始还增加了methodcaller方法。
	#使用这些方法，上面的操作将变得更加简洁和快速：
	print sorted(student_tuples, key=itemgetter(2))
	print sorted(student_objects, key=attrgetter('age'))

	#operator模块还允许多级的排序，例如，先以grade，然后再以age来排序：
	print sorted(student_tuples, key=itemgetter(1,2))
	print sorted(student_objects, key=attrgetter('grade', 'age'))

	#list.sort()和sorted()都接受一个参数reverse（True or False）来表示升序或降序排序
	print sorted(student_tuples, key=itemgetter(2), reverse=True)
	print sorted(student_objects, key=attrgetter('age'), reverse=True)
	
	#复杂地你可以构建多个步骤来进行更复杂的排序，例如对student数据先以grade降序排列，然后再以age升序排列。
	s=sorted(student_objects, key=attrgetter('age'))     # sort on secondary key
	print sorted(s, key=attrgetter('grade'), reverse=True)       # now sort on primary key, descending

