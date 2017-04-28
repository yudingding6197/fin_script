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
from internal.common import *

def fun1():
	print "we are in %s"%__name__ 

if __name__ == '__main__':
	file = open('D:/work/vxWork/script/c1.bat','r')
	print file
	file.close()
	fun1()
	
