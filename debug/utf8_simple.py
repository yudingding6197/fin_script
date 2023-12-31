#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import re

#支持中文
param_config = {
	"Date":''
}

if __name__ == '__main__':
	file = open("score.txt")
	nfile = open("_order.csv","w")
	line = file.readline()
	num = ''
	while line:
		line=line.strip()
		if line=='':
			line = file.readline()
			continue
		if line[0]=='X':
			num = line
		else:
			if line=="缺考":
				st = "%s,%s\n"%(num,"缺考")
				#st = st.decode('utf8')
			else:
				st = "%s,%s\n"%(num,line)
			nfile.write(st)
		line = file.readline()
	file.close()
	nfile.close()
	
