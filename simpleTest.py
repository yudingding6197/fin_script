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

def fun1():
	print "we are in %s"%__name__ 

if __name__ == '__main__':
	src = ['sn', 'tt', 'nt']
	df = ts.get_notices('000520')
	print df['title']
	df = ts.guba_sina(True)
	#print df

	
	print "END"
