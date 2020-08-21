#!/usr/bin/env python
# -*- coding:gbk -*-

#提取5分钟的历史数据
#从通达信中提取

import sys
import re
import os
import json
import getopt
import struct

sys.path.append('.')
from internal.handle_realtime import *
from internal.global_var import g_shcd
from internal.global_var import g_szcd
from internal.tdx.tdx_const import *
from collections import OrderedDict

def handle_argument():
	optlist, args = getopt.getopt(sys.argv[1:], 'd:f:')
	for option, value in optlist:
		if option in ["-d","--date"]:
			param_config["Date"] = value
		elif option in ["-f","--format"]:
			param_config["Format"] = value
	#print param_config

def int2datetime_new(p_int):
    mask = 0xFFF - (1 << 11)  # 11位的1
    mins = (p_int >> 16) & 0xffff
    ymds  = p_int & 0xffff
    tmpdd = ymds & mask
    month = int( tmpdd / 100 )
    day   = tmpdd % 100
    year =  ( ymds >> 11 ) + 2004
    hour = int(mins / 60)
    minute = mins % 60
    return datetime.datetime(year,month,day,hour,minute)

def readMinBin_new(p_name):
		"""tdx 5min 数据 
		   日期上低16位表示年月日，高16位表示分钟
		"""
		f = open(p_name,'rb')
		stkid = os.path.split(p_name)[1]
		stkid = os.path.splitext(stkid)[0]
		if string.lower(stkid[0:2]) == 'sh' or string.lower(stkid[0:2]) == 'sz':
			stkid = stkid[2:]
		icnt = 0
		data = []
		while 1:
			raw = f.read(4*8)
			if len(raw) <= 0 : break
			t = struct.unpack('IfffffII',raw)
			data.append({M_ID:stkid,
						 M_DT:int2datetime_new(t[0]),
						 M_OPEN:t[1],
						 M_HIGH:t[2],
						 M_LOW:t[3],
						 M_CLOSE:t[4],
						 M_AMT:t[5],
						 M_VOL:t[6],
						 'UNKOWN':t[7]})
			icnt += 1
		## end while
		f.close()
		return data

def get_k5m_data(code, folder, dict, his_date):
	k5file = folder
	if code[:3] in g_shcd:
		k5file += 'sh/fzline/sh'+code+'.lc5'
	elif code[:3] in g_szcd:
		k5file += 'sz/fzline/sz'+code+'.lc5'
	else:
		return

	if os.path.exists(k5file) is False:
		print "Error: no file", k5file
		return

	data = readMinBin_new(k5file)
	#print data
	#dict[code] = []
	bFind = 0
	list = []
	hisDt = datetime.datetime.strptime(his_date, '%Y-%m-%d').date()
	for item in data:
		if (item['DT'].date() - hisDt).days != 0:
			if bFind==1:
				break
			continue
		bFind = 1
		stm = "%02d:%02d"%(item['DT'].hour, item['DT'].minute)
		tmList = [stm, round(item['OPEN'],2), round(item['CLOSE'],2), 
			round(item['HIGH'],2), round(item['LOW'],2), item['AMT'], item['VOL']]
		list.append(tmList)
	dict[code] = list

param_config = {
	"Date":'',
	"Format":'json',
}
REAL_DAILY_PRE_FD = "../data/daily/"
TXD_K_5M_PRE_PATH = "C:\\work\\invest\\program\\tdx_gtja\\vipdoc\\"

#Main Start:
if __name__=='__main__':
	beginTm = datetime.datetime.now()
	
	handle_argument()
	if param_config["Date"]=='':
		print "Error:Must add arg -d([YYYY]MMDD)"
		exit(0)
	beginTm = datetime.datetime.now()
	hisDt = param_config["Date"]
	ret, hisDate = parseDate2(hisDt)

	flname = REAL_DAILY_PRE_FD + hisDate +"/"+ hisDate + ".txt"
	if os.path.exists(flname) is False:
		print "Error: need file", flname 
		exit(0)
	updFile = open(flname, "r")
	jdata = json.load(updFile, encoding='gbk')
	updFile.close()

	dict = OrderedDict()
	for index in range(len(jdata)):
		item = jdata[index]
		get_k5m_data(item[0], TXD_K_5M_PRE_PATH, dict, hisDate)

	endTm = datetime.datetime.now()
	print "END ", (endTm-beginTm)

	fmt = 1
	k5path = REAL_DAILY_PRE_FD + hisDate +"/"+ hisDate + "_k5min.txt"
	k5file = open(k5path, "w")
	if fmt==1:
		k5file.write("{\n")
		count = 1
		total = len(dict)
		for key,value in dict.items():
			kval = json.dumps(value)
			str = '"%s":%s'%(key, kval)
			if count!=total:
				str += ','
			k5file.write(str + '\n')
			count += 1
			
		k5file.write("}")
	else:
		json.dump(dict, k5file, indent=4)
	k5file.close()
	#print dict

