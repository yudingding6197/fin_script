# -*- coding:gbk -*-
import sys
import re
import os
import time
import string
import datetime
import pandas as pd
import numpy as np

yzzt_list = ['603345','603238','000520','300613','300608','300553','603615']

#创建Series and pandas
a = pd.Series([11,34,54,89,39,20,25])
b = pd.Series(['aa','cc','asd','ew','asd','ew','ce',])
#df = pd.DataFrame([a,b])
df = pd.DataFrame({'code':a, 'name':b})
print df

print "2222 ____________________"
s1=np.array(['a',32,33,4])
s2=np.array(['f',6,47,118])
s3=np.array(['g',26,723,32])
s4=np.array(['v',61,27,38])
s5=np.array(['r',32,45,66])
df1 = pd.DataFrame([s1, s2, s3, s4, s5],columns=list('ABCD'))
print df1

df2 = df1.sort_values(['B'], 0, False)
print df2

print "3) ____________________"
s1=[]
s1.append(['a',32,33,4])
s1.append(['f',6,47,118])
s1.append(['g',26,723,32])
print s1
df1 = pd.DataFrame(s1, columns=list('ABCD'))
df1 = df1.set_index('A')
#print df1
print df1.ix['f']['C']
for idx,row in df1.iterrows():
	print idx

print "4) ____________________"
ascid=65
#w1=''
w2=32
w3=245
w4=23
df = pd.DataFrame()
for i in range(0, 3):
	w1 = chr(ascid+i)
	w2 += 2
	w3 -= 3
	w4 *= 2
	s1 = [w1,w2,w3,w4]
	df1 = pd.DataFrame([s1], columns=list('TBCD'))
	#df1 = df1.set_index('T')
	#df = df.append(pd.DataFrame([s1], columns=list('TBCD')))
	df = df.append(s1)

#df = df.set_index('T')
print df
#df1 = pd.DataFrame(s1, columns=list('ABCD'))
#df1 = df1.set_index('A')
#print df1
#print df1.ix['f']['C']

df2 = df1.sort_values(['A'], 0, False)
print df2
df2 = df1.sort_values(['B'], 0, False)
print df2
df2 = df1.sort_values(['C'], 0, False)
print df2

print "____________________"
for i in df1:
	print i

#切片 slice 方式合并list，NB
L1 = [1,2,4,5,6]
L2 = [22,44,55,22,443,56]
L1[len(L1):len(L1)] = L2
print L1

L1 = [1,2,4,5,6]
L2 = [22,44,55,22,443,56]
L1[0:2] = L2
print L1

L1 = [1,2,4,5,6]
L2 = [22,44,55,22,443,56]
L1[4:4] = L2
print L1
