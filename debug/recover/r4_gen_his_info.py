#!/usr/bin/env python
# -*- coding:gbk -*-

#�ṩ���ڣ���ȡƥ�����ڵ���K
#���û������ζ��TP
#���浽 data/daily/����/����.txt,��Ҫ�ٴ���XD�͵�һ���ϵ�item
#[code,name,������,preClose,open,close,high,low,vol,percent]
import sys
import re
import os
import json
import getopt

sys.path.append('.')
from internal.handle_realtime import *
from internal.parse_juchao import *

def handle_argument():
	optlist, args = getopt.getopt(sys.argv[1:], 'd:f:')
	for option, value in optlist:
		if option in ["-d","--date"]:
			param_config["Date"] = value
		elif option in ["-f","--format"]:
			param_config["Format"] = value
	#print param_config

def handle_data(lobj, his_date, code, name, mark_date, jc_dict, allist):
	bFind = 0
	for i in range(len(lobj)):
		if lobj[i][0]==his_date:
			bFind = 1
			list = []
			list.append(code)
			list.append(name)
			list.append(mark_date)
			if i==0:
				#The is N flag
				#print code, i, lobj[i]
				list.append(-11)
			else:
				preClose = lobj[i-1][2]
				#print code, name, preClose, type(preClose)
				if code in jc_dict['fenhong']:
					list.append(-12)
				else:
					list.append(preClose)
			list.extend(lobj[i][1:])
			allist.append(list)
			#print json.dumps(list,encoding='gbk',ensure_ascii=False)
			#print item
	#if bFind==0:
	#	print code, lobj[0]

param_config = {
	"Date":'',
	"Format":'json',
}
REAL_DAILY_PRE_FD = "../data/daily/"

#Main Start:
if __name__=='__main__':
	handle_argument()
	if param_config["Date"]=='':
		print "Error:Must add arg -d([YYYY]MMDD)"
		exit(0)
	beginTm = datetime.datetime.now()
	hisDt = param_config["Date"]
	ret, hisDate = parseDate2(hisDt)
	year = hisDt[:4]
	tradeFl = REAL_DAILY_PRE_FD + year + '/' + "_trade_" + year + ".txt"
	jcLoc = "../data/entry/juchao/" + year + '/jc' + hisDate + ".txt"

	if os.path.exists(tradeFl) is False:
		print(tradeFl,"not exist")
		exit(0)
	if os.path.exists(jcLoc) is False:
		print(jcLoc,"not exist.")
		exit(0)
	jc_dict = {}
	read_tips_info(jcLoc, jc_dict)
	
	file = open(tradeFl, "r")
	line = file.readline()
	flag = 1
	
	allist = []
	while line:
		#print line
		if len(line)<10:
			line = file.readline()
			continue
		elif line[0]=="#":
			line = file.readline()
			continue

		obj = line.split(',')
		if flag == 0:
			line = file.readline()
			continue
	
		bNotExist = 0
		if param_config["Format"]=='':
			kFl = REAL_DAILY_PRE_FD + year + '/' + 'kday_' + obj[0] + ".txt"
			if os.path.exists(kFl) is False:
				bNotExist = 1
		elif param_config["Format"]=='json':
			kFl = REAL_DAILY_PRE_FD + year + '/json/' + 'j' + obj[0] + ".txt"
			#print kFl
			if os.path.exists(kFl) is False:
				bNotExist = 1
		else:
			print "Error: unsupport format", param_config["Format"]
			break

		if bNotExist==1:
			line = file.readline()
			continue

		kFile = open(kFl, "r")
		if param_config["Format"]=='':
			#handle_kline(dayLine, kFile)
			pass
		elif param_config["Format"]=='json':
			lobj = json.load(kFile)
			if isinstance(lobj, list) is False:
				print ("Error: invalid data", obj[0])
				kFile.close()
				break
			#print lobj
			mDate = obj[len(obj)-1]
			if len(mDate)<10:
				print(obj[0], "Invalid date", mDate)
			markDt = mDate[:10]
			handle_data(lobj, hisDt, obj[0], obj[1], markDt, jc_dict, allist)
			#json.dump(obj['data'], kFile)
		kFile.close()
		#if obj[0] == '000100':
		#	break

		line = file.readline()

	if len(allist)>0:
		flname = '../data/daily/' + hisDate +"/"+ hisDate + ".txt"
		if os.path.exists(flname):
			print "Data file exist"
			exit(0)
		hisFile = open(flname, "w")
		
		#��������ȫһ��
		#hisFile.write(json.dumps(allist, ensure_ascii=False, indent=4))
		#ÿһ������дһ��
		hisFile.write ("[")
		for i in range(len(allist)):
			if i==len(allist)-1:
				hisFile.write(json.dumps(allist[i], ensure_ascii=False)+"\n")
			else:
				hisFile.write(json.dumps(allist[i], ensure_ascii=False)+",\n")
		hisFile.write ("]")
		hisFile.close()
		'''
		'''
		
		hisFile = open(flname, "r")
		jsn = json.load(hisFile, encoding='gbk')
		hisFile.close()
	
	file.close()
