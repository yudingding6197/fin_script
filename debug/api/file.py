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

#����Ŀ¼�µ�������Ŀ¼���ļ�
path = "."
for (dirpath, dirnames, filenames) in os.walk(path):
	print len(filenames)
	file_list = filenames

#�����г�Ŀ¼�µ���Ŀ¼���ļ�
for f in os.listdir(path):
	print f

#�ж����ļ�����Ŀ¼
if(os.path.isdir(path + '/' + f)):
	pass
if(os.path.isfile(path + '/' + f)):
	pass
if(not os.path.exists(path + '/' + f)):
	#os.makedirs(y_folder)
	pass
	

#�õ��ļ������Ժ󣬿���ͨ��sort or reverse ����˳��/����
objs = os.listdir(path)
objs.sort()
objs.reverse()
#������������b
b = sorted(objs)

#�����ļ�
filetxt = "a.txt"
file2 = "file2.txt"
shutil.copy(filetxt, file2)

#ִ������python�ļ�
os.system("simpleTest.py")
#���Լ��ϲ���
#os.system("simpleTest.py  para1 para2")

'''
#������ͬһĿ¼��,��ֻ��
import B
if __name__ == "__main__":
    B.C(x,y)

#��ֻ����õ���������Ҳ����
from B import C
if __name__ == "__main__":
    C(x,y)

#��A.py��B.pyλ�ڲ�ͬ��Ŀ¼�£����������·���
#(����B.pyλ��D�̵ĸ�Ŀ¼��)
#1.��������·��
import sys
sys.path.append('D:/')
import B
if __name__=="__main__":
    print B.pr(x,y)

#2.ʹ��imp
import imp
B=imp.load_source('B','D:/B.py')
import B
if __name__=="__main__":
    print B.pr(x,y)
'''
