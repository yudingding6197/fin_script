#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import string
import urllib
import urllib2
import datetime

#ͨ���ֵ䴦��
d1 = {'name':'Bob', 'age':40}
print d1

#��̬����
d = {}
if '000520' in d.iterkeys():
	print "AAA1"
else:
	print "NNN1"
d['000520']=300
d['603098']=400
d['603987']=400
#����
print len(d), d 
print "for .. in dict:"
for item in d:
	print item
print "for .. in d.keys:"
for k in d.keys():
	print k

if '000520' in d.iterkeys():
	print "AAA2"
else:
	print "NNN2"

dict1 = d
#������ key
for i in dict1.keys():
	print(i)  #�����
	print(dict1[i]) #���ֵ
  
#������ values
for i in dict1.values():
	print(i)
  
#��������ֵ
for key,value in dict1.items():
	print(key+": "+str(value))
 

#3
d3 = dict(name='Bob',age=45)
print d3

#4.
d4 = dict([('name','Bob'),('age',40)])
print d4
d4 = dict(zip(('name','bob'),('age',40)))
print d4

#5
d5 = dict.fromkeys(['A','B'],0)
print d5
#�������ֵû�ṩ�Ļ���Ĭ��ΪNone
d5 = dict.fromkeys(['A','B'])
print d5
