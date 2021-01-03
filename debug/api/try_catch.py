#!/usr/bin/env python
# -*- coding:gbk -*-
import os
#import urllib2

if __name__=='__main__':
	LOOP_COUNT = 0
	while LOOP_COUNT<3:
		try:
			req = urllib2.Request(urlall,headers=send_headers1)
			res_data = urllib2.urlopen(req, timeout=1)
		except Exception as e:
			if LOOP_COUNT==2:
				print "Error:", e
			LOOP_COUNT = LOOP_COUNT+1
		else:
			break
		
