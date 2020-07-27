#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import re
import os
import string
import datetime
import shutil

from internal.trade_date import *

#from internal.ts_common import *
from internal.price_limit import *


#Main
if __name__=="__main__":
	curdate = ''
	bLast = 0
	trade_day = get_lastday()
	stk_list = [0, 0]
	get_zf_days('000796', 1, trade_day, 1,  stk_list)

	