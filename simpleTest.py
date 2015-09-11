# -*- coding:gbk -*-
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook
import sys
import re

s0 = '2012-12-13'
s1 = '	<tr ><th>11:29:48</th><td>14.57</td><td>-3.06%</td><td>+0.01</td><td>16</td><td>23,312</td><th><h1>中性盘</h1></th></tr>'
s2 = '<tr ><th>11:29:36</th><td>1000.56</td><td>-3.13%</td><td>--</td><td>9</td><td>13,104</td><th><h6>买盘</h6></th></tr>'
s3 = '<tr ><th>11:29:21</th><td>14.56</td><td>-3.13%</td><td>-0.02</td><td>10</td><td>14,560</td><th><h6>卖盘</h6></th></tr>'
s4 = '	<tr class="huge"><th>15:00:35</th><td>14.37</td><td>-4.39%</td><td>--</td><td>2437</td><td>3,503,320</td><th><h1>中性盘</h1></th></tr>'
s5 = '<tr class="medium"><th>14:56:59</th><td>14.37</td><td>-4.39%</td><td>--</td><td>136</td><td>195,432</td><th><h6>卖盘</h6></th></tr>'
s6 = '<tr class="medium"><th>14:56:59</th><td>14.37</td><td>4.39%</td><td>--</td><td>136</td><td>195,432</td><th><h6>卖盘</h6></th></tr>'

dateObj = re.match(r'^(\d{4})-(\d+)-(\d+)', s0)
if (dateObj is None):
	print "非法日期格式：" +qdate+ ",期望格式:YYYY-MM-DD"
	exit(1);

qdate = dateObj.group(1)
if len(dateObj.group(2))==1:
	qdate = qdate+ "-0" +dateObj.group(2)
else:
	qdate = qdate+ "-" +dateObj.group(2)
if len(dateObj.group(3))==1:
	qdate = qdate+ "-0" +dateObj.group(3)
else:
	qdate = qdate+ "-" +dateObj.group(3)
print "_____" + qdate

pattern = re.compile(r'heldlo')
match = pattern.match('hello world!')
if match:
	print match.group()

'''
m = re.match(r'(\w+) (\w+)(?P<sign>.*)', 'hello world!')
print "m.string:", m.string
print "m.re:", m.re
print "m.pos:", m.pos
print "m.endpos:", m.endpos
print "m.lastindex:", m.lastindex
print "m.lastgroup:", m.lastgroup

print "m.group(1,2):", m.group(1, 2, 3)
print "m.groups():", m.groups()
print "m.groupdict():", m.groupdict()
print "m.start(2):", m.start(2)
print "m.end(2):", m.end(2)
print "m.span(2):", m.span(2)
print r"m.expand(r'\2 \1\3'):", m.expand(r'\2 \1\3')
print "\n"
'''

fl = open('ts.txt', 'w')
fl.write("abcd\n")
fl.write("1234\n")
pos = fl.tell()
fl.close()
fl = open('ts.txt', 'a+')
fl.seek(0,0)
#x = fl.readline()
#print x
fl.write("start line\n")
fl.close()
print pos

dateObj = re.match(r'\D+(\d{2}:\d{2}:\d{2})\D+(\d+.\d{1,2})</td><td>\+?-?(\d+.\d+)\D+(--|\+\d+.\d+|-\d+.\d+)\D+(\d+)</td><td>([\d,]+)</td><th><h\d+>(卖盘|买盘|中性盘)\D', s3)
#dateObj = re.match(r'(\d{4}-\d{1,2}-\d{1,2})', s0)
if (dateObj):
	print dateObj.groups()
	print dateObj.group(1)
else:
	print "NO MATCH"
	
dateObj = re.match(r'\D+(\d{2}:\d{2}:\d{2})\D+(\d+.\d{1,2})</td><td>\+?-?(\d+.\d+)\D+(--|\+\d+.\d+|-\d+.\d+)\D+(\d+)</td><td>([\d,]+)</td><th><h\d+>(卖盘|买盘|中性盘)\D', s2)
#dateObj = re.match(r'(\d{4}-\d{1,2}-\d{1,2})', s0)
if (dateObj):
	print dateObj.groups()
	print dateObj.group(1)
else:
	print "NO MATCH"