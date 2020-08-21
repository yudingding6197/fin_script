#!/usr/bin/env python
# -*- coding:gbk -*-

#����ָ�������ڣ���ȡÿһ��ItemStk��Ӧ��kday_... �ļ�����ȡָ�����ڵļ�¼
#���û������ζ��TP
#���浽 data/daily/����/����.txt,
#Ŀǰû�и��´���XD�͵���NewStk�������̼۸�(��Ҫ�ֶ�����,���±���Ϊ'����xd.txt'�ļ�)
#[code,name,������,preClose,open,close,high,low,vol,percent]
import sys
import re
import os
import json
import getopt

sys.path.append('.')
from internal.handle_realtime import *
from internal.inf_juchao.parse_jc_tips import *

def handle_argument():
	optlist, args = getopt.getopt(sys.argv[1:], 'd:f:')
	for option, value in optlist:
		if option in ["-d","--date"]:
			param_config["Date"] = value
		elif option in ["-f","--format"]:
			param_config["Format"] = value
	#print param_config

#����ָ�����ڵ��콻�׵�ItemStk���ݣ���¼��List��
#TODO:�ж��¹ɵķ�������ȷ������Ǹ��Ƶģ����з���
#lobj: ͨ��kday_�ļ���ȡ��list, ����:
#      ["20190102", 2.69, 2.67, 2.7, 2.66, 2909600, -0.37]...
#his_date:  ָ���ָ����ݵ�����
#mark_date: �������е�����
#����ļ���
#      ["000002", "���A", "1991-01-29", 27.73, 27.7, 28.45, 28.45, 27.63, 57748439, 2.6]...
#      [3]:preClose
#      [4]:Open,  [5]:Close,   [6]:High,    [7]:Low
def select_all_trade_stk(lobj, his_date, code, name, mark_date, jc_dict, allist):
	bFind = 0
	for i in range(len(lobj)):
		if lobj[i][0]==his_date:
			bFind = 1
			list = []
			list.append(code)
			list.append(name)
			list.append(mark_date)
			if code in jc_dict['newmrk']:
				if his_date != mark_date:
					print "Error: Check why not the same day",his_date, mark_date
				#print code, i, lobj[i]
				print "This is new s", code, name
				list.append(-111)
			else:
				preClose = lobj[i-1][2]
				#print code, name, preClose, type(preClose)
				if code in jc_dict['fenhong']:
					list.append(-112)
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
	read_tfp_fh_in_tips(jcLoc, jc_dict)
	
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
			select_all_trade_stk(lobj, hisDt, obj[0], obj[1], markDt, jc_dict, allist)
			#json.dump(obj['data'], kFile)
		kFile.close()
		#if obj[0] == '000100':
		#	break

		line = file.readline()

	if len(allist)>0:
		flname = REAL_DAILY_PRE_FD + hisDate +"/"+ hisDate + ".txt"
		if os.path.exists(flname):
			print "Data file exist"
			exit(0)
		updFile = open(flname, "w")
		
		fmt = 0
		if fmt==0:
			#��������ȫһ��
			updFile.write(json.dumps(allist, ensure_ascii=False, indent=4))
		else:
			#ÿһ������дһ��
			updFile.write ("[")
			for i in range(len(allist)):
				if i==len(allist)-1:
					updFile.write(json.dumps(allist[i], ensure_ascii=False)+"\n")
				else:
					updFile.write(json.dumps(allist[i], ensure_ascii=False)+",\n")
			updFile.write ("]")
			updFile.close()
		'''
		'''
		
		updFile = open(flname, "r")
		jsn = json.load(updFile, encoding='gbk')
		updFile.close()
	
	file.close()
