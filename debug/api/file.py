# -*- coding:gbk -*-
import sys
import re
import os
import string
import urllib
import urllib2
import datetime
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook

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

