#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import re
import os
import time
import string
import datetime
#import platform
#import shutil
#import getopt
#import tushare as ts
#import internal.common
#from internal.ts_common import *
from internal.url_dfcf.new_yzb import *
from internal.trade_date import *


#Main Start:
if __name__=='__main__':
	yz_list = []
	getNoOpenYZStock(yz_list)