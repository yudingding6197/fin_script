# -*- coding:gbk -*-
import sys
import re
import os
import string
import datetime
import urllib
import urllib2
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook
import tushare as ts

# Main
path = "..\\Data\\entry\\stk_trade\\"
pindex = len(sys.argv)
if pindex<2:
	sys.stderr.write("Usage: " +os.path.basename(sys.argv[0])+ " 代码 \n")
	exit(1);

code = sys.argv[1]
if len(code)!=6 or code.isdigit() is False:
	sys.stderr.write("Invalid code" + code)
	exit(1);

tddf = ts.get_hist_data(code)
print tddf.head(5)
tddf = tddf.loc[:,['open', 'high', 'close', 'low', 'volume', 'price_change', 'p_change', 'turnover']]

if len(tddf)==0:
	print "No trade data"
	exit(0)

today = datetime.date.today()
qdate = '%04d-%02d-%02d' %(today.year, today.month, today.day)
filename = "%s%s_%s.xlsx" % (path, code, qdate)
tddf.to_excel(filename)


