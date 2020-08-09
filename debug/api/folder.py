#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import string
import datetime
import shutil

#遍历目录下的所有子目录和文件
path = "."

'''
1.如果各组件名首字母不包含’/’，则函数会自动加上
2.如果有一个组件是一个绝对路径，则在它之前的所有组件均会被舍弃
3.如果最后一个组件为空，则生成的路径以一个’/’分隔符结尾
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
