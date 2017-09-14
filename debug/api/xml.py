#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import os
import time
import urllib2
from urllib2 import urlopen, Request
try: 
  import xml.etree.cElementTree as ET 
except ImportError: 
  import xml.etree.ElementTree as ET 

'''
<?xml version="1.0"?> 
<data> 
  <country name="Singapore"> 
    <rank>4</rank> 
    <year>2011</year> 
    <gdppc>59900</gdppc> 
    <neighbor name="Malaysia" direction="N"/> 
  </country> 
  <country name="Panama"> 
    <rank>68</rank> 
    <year>2011</year> 
    <gdppc>13600</gdppc> 
    <neighbor name="Costa Rica" direction="W"/> 
    <neighbor name="Colombia" direction="E"/> 
  </country> 
</data>
'''

try:
	tree = ET.parse("country.xml")     #打开xml文档 
	#root = ET.fromstring(country_string) #从字符串传递xml 
	root = tree.getroot()         #获得root节点  
except Exception, e: 
	print "Error:cannot parse file:country.xml."
	sys.exit(1) 
print root.tag, "---", root.attrib  
for child in root: 
	print child.tag, "---", child.attrib 

print "*"*10
print root[0][1].text   #通过下标访问 
print root[0].tag, root[0].text 
print "*"*10

for country in root.findall('country'): #找到root节点下的所有country节点 
	rank = country.find('rank').text   #子节点下节点rank的值 
	name = country.get('name')      #子节点下属性name的值 
	print name, rank 

#修改xml文件 
for country in root.findall('country'): 
	rank = int(country.find('rank').text) 
	if rank > 50: 
		root.remove(country) 

tree.write('output.xml')



from xml.etree import ElementTree
def print_node(node):
    '''打印结点基本信息'''
    print "=============================================="
    print "node.attrib:%s" % node.attrib
    if node.attrib.has_key("age") > 0 :
        print "node.attrib['age']:%s" % node.attrib['age']
    print "node.tag:%s" % node.tag
    print "node.text:%s" % node.text
def read_xml(text):
    '''读xml文件'''
    # 加载XML文件（2种方法,一是加载指定字符串，二是加载指定文件）    
    # root = ElementTree.parse(r"D:/test.xml")
    root = ElementTree.fromstring(text)
    
    # 获取element的方法
    # 1 通过getiterator 
    lst_node = root.getiterator("person")
    for node in lst_node:
        print_node(node)
        
    # 2通过 getchildren
    lst_node_child = lst_node[0].getchildren()[0]
    print_node(lst_node_child)
        
    # 3 .find方法
    node_find = root.find('person')
    print_node(node_find)
    
    #4. findall方法
    node_findall = root.findall("person/name")[1]
    print_node(node_findall)
    
if __name__ == '__main__':
     read_xml(open("test.xml").read())


#encoding=utf-8
from xml.etree import ElementTree as ET
#要找出所有人的年龄
per=ET.parse('test.xml')
p=per.findall('/person')
for x in p:
    print x.attrib
print
for oneper in p:  #找出person节点
    for child in oneper.getchildren(): #找出person节点的子节点
        print child.tag,':',child.text

    print 'age:',oneper.get('age')
    print '############'
