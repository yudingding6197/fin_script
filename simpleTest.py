# -*- coding:gbk -*-
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook
import sys
import re
import os
import time
import datetime

from internal.common import *

def fun(list):
	del list[:]
	
tmpContPrice = ['Buy', 1, 302, 232, 22, 42, 54,856, 545, 432, 355, 655]
#tmpContPrice = ['Buy', 1, 302, 232, 22]
contPrice = [302, 232, 22]
tmpPriceLen = len(tmpContPrice)
contPriceLen = len(contPrice)
bChange = 0

print tmpPriceLen, contPriceLen
if tmpPriceLen>0:
	if contPriceLen==0:
		for k in range(2,tmpPriceLen):
			contPrice.append(tmpContPrice[k])
	else:
		if (tmpPriceLen-2)<contPriceLen:
			del contPrice[:]
			for k in range(2,tmpPriceLen):
				contPrice.append(tmpContPrice[k])
			bChange = 1
		else:
			bAllMatch = 1
			for k in range(0, contPriceLen):
				if (tmpContPrice[k+2]!=contPrice[k]):
					bAllMatch = 0
			if bAllMatch==0:
				del contPrice[:]
				for k in range(2,tmpPriceLen):
					contPrice.append(tmpContPrice[k])
				bChange = 1
			else:
				if (tmpPriceLen-2)>contPriceLen:
					for k in range(contPriceLen+2,tmpPriceLen):
						contPrice.append(tmpContPrice[k])
					bChange = 1
	print "CCCCCCCCCCCC", contPrice
	if (len(contPrice)>=6 and bChange==1):
		msgstr = 'msg "*" "Continued value:%d"'%(contPriceLen)
		#os.system(msgstr)

