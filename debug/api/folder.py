#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import string
import datetime
import shutil

#����Ŀ¼�µ�������Ŀ¼���ļ�
path = "."

'''
1.��������������ĸ��������/�����������Զ�����
2.�����һ�������һ������·����������֮ǰ������������ᱻ����
3.������һ�����Ϊ�գ������ɵ�·����һ����/���ָ�����β
'''

Path1 = 'home'
Path2 = 'develop'
Path3 = 'code'

Path10 = Path1 + Path2 + Path3
Path20 = os.path.join(Path1,Path2,Path3)
print ('Path10 = ',Path10)
print ('Path20 = ',Path20)

Path1 = '/home'
Path2 = 'develop'
Path3 = 'code'

Path10 = Path1 + Path2 + Path3
Path20 = os.path.join(Path1,Path2,Path3)
print ('Path10 = ',Path10)
print ('Path20 = ',Path20)

Path10 = os.path.join("a/c","d/w",'fil.txt')
print ('Path10 = ',Path10)
