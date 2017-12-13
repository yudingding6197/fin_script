#!/usr/bin/env python
# -*- coding:gbk -*-
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook
import sys
import re
import os
import time
import datetime
import ctypes
import sqlite3
import tushare as ts
from internal.common import *

def fun1():
	print "we are in %s"%__name__ 

if __name__ == '__main__':
	arr = ['YZZT', 'ZT', 'ZTHL', 'YZDT', 'DT', 'DTFT']
	key = 'ZT'
	if key in arr:
		print ""


