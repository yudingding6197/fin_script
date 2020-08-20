#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
dump 和 dumps 都实现了序列化, 将json格式的字符转换为dict
load 和 loads 都实现反序列化, 将dict类型转换为json字符串格式

变量从内存中变成可存储或传输的过程称之为序列化
序列化是将对象状态转化为可保存或可传输格式的过程。

变量内容从序列化的对象重新读到内存里称之为反序列化
反序列化是流转换为对象
'''

import os
import json

#1. json.loads( dict or list 格式的字符串)

#2. file = open('1.json','r',encoding='utf-8')
#   info = json.load(file)

#3. json_info = json.dumps(dict or list 对象) 

#4. json_info = {'age': '12'}
#   file = open('1.json','w',encoding='utf-8')
#   json.dump(json_info,file)

#json 通过load能够加载为 dict or list
str = '{"aa":"c1","bb":"c2"}'
dic = json.loads(str);
print (type(dic), dic)
print (dic['aa'])
#整个解析为list, 每一个list里面是 dict
str = '[{"day":"2020-07-09 13:05:00","open":"22.870","high":"22.950","low":"22.870","close":"22.890","volume":"220000"},{"day":"2020-07-09 13:10:00","open":"22.890","high":"22.910","low":"22.850","close":"22.870","volume":"224878"}]'
dic = json.loads(str);
print (type(dic), type(dic[0]))
print (dic[0]['open'])

print("\n============== dumps =================")
str1 = json.dumps(dic)
print (str1)


json_info = {'age': '12', 'name':'sn'}
file = open('_tjson.txt','w')
json.dump(json_info,file)
