#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import re
import os
import time
import string
import datetime

def spc_round2(value,bit):
	b = int(value*10000)
	b1 = b+51
	j = b1/100
	rd_val = float(j)/100
	return rd_val
	
if __name__=="__main__":
	print "Math"