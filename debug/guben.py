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
sys.path.append(".")
#sys.path.append("..")
from internal.common_inf import *

def digit_full_with_space(digit, length):
	#fmt = "%" + ("%d"%(length)) + "d"
	fmt = "%%%dd"%(length)
	d_v = fmt%(digit)
	return d_v
def full_with_space(digit, length):
	fmt = "%" + ("%d"%(length)) + "d"
	d_v = fmt%(digit)
	return d_v

def handle_guben(code, src):
	title = ['变动日期','总股本','流通A股','高管股','限售A股']
	content = get_guben_change(code, src)
	#print(content)
	if content is None:
		return

	predir = "..\data\entry\ore_mine"
	folder = os.path.join(predir, code)
	if not os.path.exists(folder):
		os.makedirs(folder)

	s_folder = os.path.join(predir, '_summar')
	if not os.path.exists(s_folder):
		os.makedirs(s_folder)

	location = os.path.join(folder, '_guben.txt')
	f = open(location, 'w+')
	#写入最新更新日期 和 飞线数量
	value = "%s,%d\n"%(content[0][0], content[1][0])
	f.write(value)

	#count = len(content[0])
	#line_fmt = '10% '
	#for i in range(0, count):
	#	line_fmt += '12% '
	line_idx = 0
	date_len = len(content[0][0]) + 1
	for line_obj in content:
		b_first = 1
		for item in line_obj:
			if line_idx==0:
				if b_first:
					value = '%-6s %11s'%(title[line_idx].decode('gbk'), item)
					b_first = 0
				else:
					value = ' ' + item
			else:
				if b_first:
					value = '%-6s %12d'%(title[line_idx].decode('gbk'), item)
					l = value.encode('gbk')
					b_first = 0
				else:
					value = digit_full_with_space(item, date_len)
			f.write(value.encode('gbk'))
		f.write('\n')
		line_idx += 1
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