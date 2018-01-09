#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import os
import datetime
import getopt
import shutil
sys.path.append(".")
sys.path.append("..")
from internal.ts_common import *

#选择文件，拷贝到指定位置

# Main
param_config = {
	"Date":'',	#
	"Code":''	#
}
if __name__=="__main__":
	td = ''
	nowToday = datetime.date.today()
	optlist, args = getopt.getopt(sys.argv[1:], '?c:d:')
	for option, value in optlist:
		if option in ["-d","--date"]:
			ret,stdate = parseDate(value, nowToday, ai=1)
			if ret==-1:
				exit()
			param_config['Date'] = stdate
			td = stdate
		elif option in ["-c","--code"]:
			param_config['Code'] = value
		elif option in ["-?","--??"]:
			print "Usage:", os.path.basename(sys.argv[0]), " -c code [-d MMDD/YYYYMMDD]"
			exit()


	code = param_config['Code']
	td = param_config['Date']
	if code=='':
		print "Need code"
		exit()
	sfolder = '../data/entry/resp/'
	sfolder1 = sfolder + code + '/'
	dfolder = '../data/'
	if td=='':
		for (dirpath, dirnames, filenames) in os.walk(sfolder1):  
			print('dirpath = ' + dirpath)
			for filename in filenames:
				shutil.copy(sfolder1+filename, dfolder+filename)
		pass
	else:
		name = code +"_"+ td + '.csv'
		shutil.copy(sfolder1+name, dfolder+name)

