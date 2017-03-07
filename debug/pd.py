# -*- coding:gbk -*-
import sys
import re
import os
import time
import string
import datetime
import pandas as pd

yzzt_list = ['603345','603238','000520','300613','300608','300553','603615']

#创建Series and pandas
a = pd.Series([11,34,54,89,39,20,25])
b = pd.Series(['aa','cc','asd','ew','asd','ew','ce',])
#df = pd.DataFrame([a,b])
df = pd.DataFrame({'code':a, 'name':b})

df1 = df[df.code>40]['name']
#print a
#print type(a)
print type(df1)
print df1
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
