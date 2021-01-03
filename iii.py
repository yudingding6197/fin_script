#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import os
import json
import datetime

#Main Start:
if __name__=='__main__':
	location='internal/db/sh000001_json.txt'
	fl = open(location, 'r')
	data = json.load(fl)
	#print data
	info = json.loads(data)
	fl.close()

	print type(info)
	print info['times'][0]
	print info['times'][-2]
	print info['times'][-1]
	
	print "====="
	info['times'].append('22220101')
	print info['times'][0]
	print info['times'][-2]
	print info['times'][-1]
	