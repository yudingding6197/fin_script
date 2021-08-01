#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import string
import urllib
import urllib2
import datetime
import shutil

#遍历目录下的所有子目录和文件
path = "."
for (dirpath, dirnames, filenames) in os.walk(path):
	print len(filenames)
	file_list = filenames

#仅仅列出目录下的子目录和文件
for f in os.listdir(path):
	print f

#判断是文件还是目录
if(os.path.isdir(path + '/' + f)):
	pass
if(os.path.isfile(path + '/' + f)):
	pass
if(not os.path.exists(path + '/' + f)):
	#os.makedirs(y_folder)
	pass
	

#得到文件内容以后，可以通过sort or reverse 进行顺序/倒序
objs = os.listdir(path)
objs.sort()
objs.reverse()
#将排序结果传给b
b = sorted(objs)

#拷贝文件
filetxt = "a.txt"
file2 = "file2.txt"
shutil.copy(filetxt, file2)

#执行其它python文件
os.system("simpleTest.py")
#可以加上参数
#os.system("simpleTest.py  para1 para2")

'''
#假如在同一目录下,则只需
import B
if __name__ == "__main__":
    B.C(x,y)

#若只需调用单个函数，也可以
from B import C
if __name__ == "__main__":
    C(x,y)

#若A.py和B.py位于不同的目录下，可以用以下方法
#(假设B.py位于D盘的根目录下)
#1.引用所在路径
import sys
sys.path.append('D:/')
import B
if __name__=="__main__":
    print B.pr(x,y)

#2.使用imp
import imp
B=imp.load_source('B','D:/B.py')
import B
if __name__=="__main__":
    print B.pr(x,y)
'''
