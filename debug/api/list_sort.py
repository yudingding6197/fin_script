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
	
	#key������ֵΪһ���������˺���ֻ��һ�������ҷ���һ��ֵ�������бȽϡ�
	#��������ǿ��ٵ���Ϊkeyָ���ĺ�����׼ȷ�ض�ÿ��Ԫ�ص��á�
	#���㷺��ʹ��������ø��Ӷ����ĳЩֵ���Ը��Ӷ������������
	print sorted(student_tuples, key=lambda student: student[2])

	#Operator ģ�麯��
	#�����key������ʹ�÷ǳ��㷺�����python�ṩ��һЩ����ĺ�����ʹ�÷��ʷ����������׺Ϳ��١�
	#operatorģ����itemgetter��attrgetter����2.6��ʼ��������methodcaller������
	#ʹ����Щ����������Ĳ�������ø��Ӽ��Ϳ��٣�
	print sorted(student_tuples, key=itemgetter(2))
	print sorted(student_objects, key=attrgetter('age'))

	#operatorģ�黹����༶���������磬����grade��Ȼ������age������
	print sorted(student_tuples, key=itemgetter(1,2))
	print sorted(student_objects, key=attrgetter('grade', 'age'))

	#list.sort()��sorted()������һ������reverse��True or False������ʾ�����������
	print sorted(student_tuples, key=itemgetter(2), reverse=True)
	print sorted(student_objects, key=attrgetter('age'), reverse=True)
	
	#���ӵ�����Թ���������������и����ӵ����������student��������grade�������У�Ȼ������age�������С�
	s=sorted(student_objects, key=attrgetter('age'))     # sort on secondary key
	print sorted(s, key=attrgetter('grade'), reverse=True)       # now sort on primary key, descending

