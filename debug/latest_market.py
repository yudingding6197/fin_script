#!/usr/bin/env python
# -*- coding:gbk -*-

import sys
import re
import os
import datetime
import tushare as ts
sys.path.append(".")
sys.path.append("..")
from internal.dfcf_interface import *

if __name__ == '__main__':
	new_st_list = []
	get_latest_market(new_st_list)
	print len(new_st_list)


