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
	get_guben_change(code, src)

	predir = "..\data\entry\ore_mine"
	folder = os.path.join(predir, code)
	if not os.path.exists(folder):
		os.makedirs(folder)

param_config = {
	"Code":'',	#
	"File":0,	#
	"Source":'',#
	"LogTP":0	#写日志
}

if __name__=="__main__":
	optlist, args = getopt.getopt(sys.argv[1:], '?c:f:s:')
	for option, value in optlist:
		if option in ["-c","--code"]:
			param_config['Code'] = value
		elif option in ["-f","--file"]:
			param_config['File'] = value
		elif option in ["-s","--source"]:
			param_config['Source'] = value
		elif option in ["-?","--??"]:
			pm = ' [-c code] [-f file] [-s source]'
			print("Usage: " + os.path.basename(sys.argv[0]) + pm)
			print("   -f: get code list from file")
			print("   -s: Choose source from server, include sn, qq, 163")
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