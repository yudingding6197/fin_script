#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 以图南股份为例，计算每一天的EMA，和真正EMA算法有区别
import sys
import re
import os
import string
import datetime
import shutil

from internal.trade_date import *

#from internal.ts_common import *
from internal.price_limit import *
SHT = 12
LNG = 26
def EMA(X, N, i, Y_p=0.0):
	Y = (X*2 + Y_p*(N-1))/(N+1)
	Y1 = round(Y, 4)
	if N==SHT:
		print ("%2d %.2f"%(i+1, round(Y1, 2)) ),
	else:
		print (round(Y1, 2))
	return Y1

#Main
if __name__=="__main__":
	'''
	EMA(X, N): Y = (X*2 + Y_p*(N-1))/(N+1)
	#01  15.13
	#02	 16.64  
	  15.36	15.24
	#03  18.30
	  15.81	15.47
	#04  20.13
	  16.48		15.81
	#05  22.14
	  17.35		16.28
	#06  24.35
	#07  26.79
	#08  29.47
	#09  32.42
	#10  
	'''
	
	close = [
	15.13,
	16.64,
	18.30,
	20.13,
	22.14,
	24.35,
	26.79,
	]
	
	Ys_p = close[0]
	Yl_p = close[0]
	for i in range(len(close)):
		Ys = EMA(close[i], SHT, i, Ys_p)
		Yl = EMA(close[i], LNG, i, Yl_p)
		Ys_p = Ys
		Yl_p = Yl
	#print Y02S, Y02L
	#print Y03S, Y03L
	#print Y04S, Y04L
	
	exit(0)
