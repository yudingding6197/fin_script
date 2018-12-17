#!/usr/bin/env python
# -*- coding:gbk -*-

import sys
import re
import os
import datetime
import pandas as pd
import tushare as ts
from internal.common import *
from internal.ts_common import *
from internal.dfcf_interface import *

def fun1():
	print "we are in %s"%__name__ 

if __name__ == '__main__':
	stkList = []
	#get_stk_code_by_cond(stkList)
	#print stkList[0:30]
	for _ in range(10):
		print 111
	
	print "END"
