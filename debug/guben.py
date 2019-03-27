#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import string
import urllib2
import datetime
import getopt
import bs4
from bs4 import BeautifulSoup
sys.path.append(".")
#sys.path.append("..")
from internal.common_inf import *

def handle_guben(code, src):
	content = get_guben_change(code, src)
	#print(content)
	if content is None:
		return

	predir = "..\data\entry\ore_mine"
	folder = os.path.join(predir, code)
	if not os.path.exists(folder):
		os.makedirs(folder)

	location = os.path.join(folder, '_guben.txt')
	f = open(location, 'w+')
	#写入最新更新日期 和 飞线数量
	f.write(content[0][0] + '\n')
	f.write(str(content[1][0]) + '\n')
	for item in content:
		for val in item:
			f.write(str(val) + ' ')
		f.write('\n')
	f.close()

def usage_help():
	pm = ' [-c code] [-f file] [-s source]'
	print("Usage: " + os.path.basename(sys.argv[0]) + pm)
	print("   -f: get code list from file")
	print("   -s: Choose source from server, include sn, qq, 163")

param_config = {
	"Code":'',	#
	"File":0,	#
	"Source":'',#
	"LogTP":0	#写日志
}


if __name__=="__main__":
	if len(sys.argv)==1:
		usage_help()
		exit()

	optlist, args = getopt.getopt(sys.argv[1:], '?c:f:s:')
	for option, value in optlist:
		if option in ["-c","--code"]:
			param_config['Code'] = value
		elif option in ["-f","--file"]:
			param_config['File'] = value
		elif option in ["-s","--source"]:
			param_config['Source'] = value
		elif option in ["-?","--??"]:
			usage_help()
			exit()
	#end for

	src = param_config['Source']
	if param_config['Code']!='':
		code = param_config['Code']
		handle_guben(code, src)
	elif param_config['File']!='':
		codeList = []
		for code in codeList:
			handle_guben(code, src)
	else:
		print("Need parameter, -? for help")