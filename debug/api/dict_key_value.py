# -*- coding:gbk -*-
import sys
import re
import os
import string
import urllib
import urllib2
import datetime

#通过字典处理
d1 = {'name':'Bob', 'age':40}
print d1

#动态增加
d = {}
if '000520' in d.iterkeys():
	print "AAA1"
else:
	print "NNN1"
d['000520']=300
d['603098']=400
print d

if '000520' in d.iterkeys():
	print "AAA2"
else:
	print "NNN2"

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
#如果键的值没提供的话，默认为None
d5 = dict.fromkeys(['A','B'])
print d5
