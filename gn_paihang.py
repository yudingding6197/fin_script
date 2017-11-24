#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import urllib2
import re
import datetime
import logging
import shutil
from internal.dfcf_interface import *

#Main 开始
flname = '../data/gnbk.log'
logging.basicConfig(level=logging.DEBUG,
    format='',
    filename=flname,
    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
#formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
formatter = logging.Formatter('')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
cur=datetime.datetime.now()

listobj = []
bkInfo=bkStatInfo()
query_gainianbankuai(listobj, bkInfo)

listlen = len(listobj)
increase = bkInfo.increase
fall = bkInfo.fall
zt_count = bkInfo.zt_count
dt_count = bkInfo.dt_count

fmt = "[%02d:%02d] Increase:%d,  Fall:%d,  PING:%d, (ZT:%d  DT:%d)"
logging.info( fmt %(cur.hour, cur.minute, increase, fall, listlen-increase-fall, zt_count, dt_count))
for i in range(0, listlen):
	if i<30:
		#print listobj[i]
		logging.info( listobj[i] )
	elif i==31:
		logging.info( "......")
		logging.info( "......")
	elif i>=listlen-10:
		logging.info(listobj[i])

log = open(flname, 'r')
content = log.read()
log.close()

updateLog = 1
if updateLog==1:
	fmt_time = '%d-%02d-%02d' %(cur.year, cur.month, cur.day)
	path = '../data/entry/realtime/'
	flname = path + "gainian_" + fmt_time + ".txt"
	baklog = open(flname, 'a')
	baklog.write('##############################################################\n')
	baklog.write(content)
	baklog.write('\n\n')
	baklog.close()

	tmp_file = path + "a_gainian.txt"
	shutil.copy(flname, tmp_file)
