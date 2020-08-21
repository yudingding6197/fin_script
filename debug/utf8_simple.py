#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import re
import datetime
import getopt
from internal.common import *

#支持中文
param_config = {
	"Date":''
}

if __name__ == '__main__':
	today = datetime.date.today()
	optlist, args = getopt.getopt(sys.argv[1:], 'd:')
	for option, value in optlist:
		if option in ["-d","--date"]:
			ret,stdate = parseDate(value, today)
			if ret==-1:
				exit(1)
			param_config['Date'] = stdate

	print param_config['Date']
	req_count=0
