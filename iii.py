#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import re
import os
import string
import datetime

from internal.trade_date import *
#from internal.realtime_obj import *
#from internal.analyze_realtime import *
#from internal.handle_realtime import *

#Main
if __name__=="__main__":
	trade_date = get_lastday()
	#pre_date = get_preday(2, trade_date)
	#print "iii", trade_date, pre_date
	