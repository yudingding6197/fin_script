#!/usr/bin/env python
# -*- coding:utf8 -*-

import re

#正则默认是贪婪，非贪婪添加'?'
if __name__=="__main__":
	#贪婪和非贪婪
	s="This is a number 234-235-22-423"
	r=re.match(".+(\d+-\d+-\d+-\d+)",s)
	print(r.group(1))
	#'4-235-22-423'
	r=re.match(".+?(\d+-\d+-\d+-\d+)",s)
	print(r.group(1))
	#'234-235-22-423'

	print re.match(r"aa(\d+)","aa2343ddd").group(1)
	#'2343'
	print re.match(r"aa(\d+?)","aa2343ddd").group(1)
	#'2'
	print re.match(r"aa(\d+)ddd","aa2343ddd").group(1) 
	#'2343'
	print re.match(r"aa(\d+?)ddd","aa2343ddd").group(1)
	#'2343'

	#使用两次非贪婪匹配
	line = u'甘李药业(13, DT), 康华生物(20, DT), '
	cond = '(.*?)\((\d+),(.*?)\),(.*)'
	obj = re.match(cond, line)
	while obj:
		left = obj.group(4)
		name = obj.group(1).strip()
		print name, obj.group(2), obj.group(3)
		obj = re.match(cond, left)
	