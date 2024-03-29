#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
dump 和 dumps 都实现了序列化, 将dict/list对象转换为字符串输出
load 和 loads 都实现反序列化, 将dict/list格式的'字符串'转换为dict/list对象
dump() load 参数是file(通过open()打开)
dumps loads 参数是dict/list对象
唯独dump()带有两个参数 dump(dict/list对象, file)

变量从内存中变成可存储或传输的过程称之为序列化
序列化是将对象状态转化为可保存或可传输格式的过程。

变量内容从序列化的对象重新读到内存里称之为反序列化
反序列化是流转换为对象

对于dict/list对象中包含中文，通过json.dumps(dictObj, ensure_ascii=False)
'''

import os
import json
from collections import OrderedDict

#1. json.loads( dict or list 格式的字符串)

#python2 not support args 'encoding'
#2. file = open('1.json','r'/*,encoding='utf-8'*/)
#   info = json.load(file)
#   info = json.load(file,encoding='utf-8')

#3. json_info = json.dumps(dict or list 对象) 

#4. json_info = {'age': '12'}
#   file = open('1.json','w',encoding='utf-8')
#   json.dump(json_info,file)

#json 通过load能够加载为 dict or list
str = '{"aa":"c1","bb":"c2"}'
dic = json.loads(str);
print (type(dic), dic)
print (dic['aa'])

#str = '{"aa":1,"bb":2,"Data":["a1","a2","a3]}'
str = '["aa","cc","dk"]'
ll = json.loads(str)
print(len(ll))

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
print ("=====2")
print (json.dump(json_info,file))

#处理汉字
#json.dumps(stoday.lst_dt,ensure_ascii=False)

#保持顺序
#json.loads(content,object_pairs_hook=OrderedDict)

'''
#如果将要写入的list, dict对象中包含中文，在python2中按照json.dump(listItem, file)
#文件的中文是unicode模式。如果期望改为中文显示，通过codecs进行写入
import codecs
fp = codecs.open(filename, 'w+', 'utf-8')
fp.write(json.dumps(listItem,ensure_ascii=False))
fp.close()

#如果list, dict对象包含中文，通过json.load(file)进行加载
#期望在控制台输出中文，而不是unicode，可以通过
json.dump(list/dict, encoding="UTF-8", ensure_ascii=False)
#或者转为str后，处理为：(这种在utf-8的中文文件中，似乎不行)
str(list).decode('string_escape')
'''