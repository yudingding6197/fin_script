#!/usr/bin/env python
# -*- coding:gbk -*-

import sys
import re
import os
import datetime
import tushare as ts
from internal.common import *
from internal.ts_common import *

def fun1():
	print "we are in %s"%__name__ 

if __name__ == '__main__':
	new_st_list = []

	get_latest_market(new_st_list)
	
	print len(new_st_list)


