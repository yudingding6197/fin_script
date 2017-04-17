#!/usr/bin/env python
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
#得到索引，转为list
dfidx=df1.index
df_list = list(dfidx)
# df = df.reindex(list(df.index) + [ 'c', 'd', 'e' ])
	
print "4) ____________________"
ascid=65
#w1=''
w2=32
w3=245
w4=23
df = pd.DataFrame()
for i in range(0, 8):
	w1 = chr(ascid+i)
	w2 += 2
	w3 -= 3
	w4 *= 2
	s1 = [w1,w2,w3,w4]
	#df1 = pd.DataFrame([s1], columns=list('TBCD'))
	#df1 = df1.set_index('T')
	df = df.append(pd.DataFrame([s1], columns=list('TBCD')))
	#df = df.append(s1)

df = df.set_index('T')
#print df.describe()

#通过切片组成新的dataFrame
df = df[2:5]
print df

#df1 = pd.DataFrame(s1, columns=list('ABCD'))
#df1 = df1.set_index('A')
#print df1
#print df1.ix['f']['C']

'''
df2 = df1.sort_values(['A'], 0, False)
print df2
df2 = df1.sort_values(['B'], 0, False)
print df2
df2 = df1.sort_values(['C'], 0, False)
print df2

'''
print "____________________"

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

# filter "isin", "==", "contain"
df = pd.DataFrame({'date': ['2017-04-05', '2017-01-05', '2017-02-05', '2017-03-05', '2017-04-02'],
                    'B': [23, 34, 12, 314, 56],
                    'C': ['C0', 'C1', 'C2', 'C3', 'C4'],
                    'D': ['D0', 'D1', 'D2', 'D3', 'D4'],
                    'E': ['E0', 'E1', 'E2', 'E3', 'E4']
					}, index=[0, 1, 2, 3, 4])

#df2 = df.loc[df['date'].str.contains('2017-04')]
print df
print "Filter:"
df1 = df.loc[df['date'].str.contains('2017-04')]
print df1

#print df.loc[df['B']]
df2 = df.loc[df['B']>30]
print df2

# df['date'] = df['date'].map(lambda x : x[:5] )

'''
pd.set_option('display.height',1000)
pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)
pd.set_option('max_colwidth', 200)

不显示索引 index
print df.to_string(index=False)
'''