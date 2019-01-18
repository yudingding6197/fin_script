#!/usr/bin/env python
# -*- coding:gbk -*-

import sys
import os
import getopt


def fun1():
    print "we are in %s"%__name__ 

def handle_init_c(prj_name):
    fname = "C:\\使用说明.txt"
    wrt_fl = "h.txt"
    b_handle = 0
    if os.path.exists(fname.decode('utf8')):
        file = open(fname.decode('utf8'), "r")
        line = file.readline()
        while line:
            if b_handle==0:
                if len(line) < 8:
                    line = file.readline()
                    continue
                pre_text = (line.decode('utf8'))[:8]
                if pre_text=="#include":
                    fw = open(wrt_fl, "w")
                    b_handle = 1
                    fw.write(line)
            else:
                fw.write(line)
            line = file.readline()
        if b_handle == 1:
        	fw.close()
        file.close()
    else:
        print("Not file")
    '''
    src_fl = "C:\\Tornado\\target\\proj\\Project1\\usrAppInit.c"
    dest_fl = os.path.join(WORK_SPACE, prj_name, 'usrAppInit.c')
    cmd = "cp " + src_fl + " " + dest_fl
    os.system(cmd)
    '''

if __name__ == '__main__':
	param_config = {
		"Code":'',
		"Time":0,
		"Delta":0,
		"Analyze":0,
	}
	'''
	-c bsp_name  -l
	-d bsp_name 
	-s src_name  -l
	-r src_name
	'''

	optlist, args = getopt.getopt(sys.argv[1:], 'c:t:d:a:')
	for option, value in optlist:
		if option in ["-a","--analyze"]:
			print value
			param_config["Analyze"] = 1
		elif option in ["-t","--time"]:
			print 3
			param_config["Time"] = int(value)
		elif option in ["-d","--delta"]:
			print 4
			param_config["Delta"] = int(value)
		else:
			print "None"
	handle_init_c('')
	
	print "END"

