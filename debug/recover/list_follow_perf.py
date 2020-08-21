#!/usr/bin/env python
# -*- coding:gbk -*-

#得到指定STK和指定日期后的表现
#[code,name,上市日,preClose,open,close,high,low,vol,percent]
import sys
import re
import os
import json
import getopt

sys.path.append('.')
from internal.handle_realtime import *
from internal.inf_juchao.parse_jc_tips import *

#将在指定日期当天交易的ItemStk数据，记录到List中
#TODO:判断新股的方法不正确，如果是复牌的，就有风险
#lobj: 通过kday_文件读取的list, 类似:
#      ["20190102", 2.69, 2.67, 2.7, 2.66, 2909600, -0.37]...
#his_date:  指定恢复数据的日期
#mark_date: 个股上市的日期
#输出文件：
#      ["000002", "万科A", "1991-01-29", 27.73, 27.7, 28.45, 28.45, 27.63, 57748439, 2.6]...
#      [3]:preClose
#      [4]:Open,  [5]:Close,   [6]:High,    [7]:Low
def output_data(dlist):
	fmt = "%s %7.2f  %5.2f"
	value = fmt % (dlist[0], dlist[6], dlist[2])
	print value

def show_code_perform(j_list, his_date):
	bStart=0
	sNum = 0
	for index in range(len(j_list)):
		wyDate = j_list[index][0]
		ret,cur_date = parseDate2(wyDate)
		if cur_date==his_date:
			bStart = 1
			#print "Matched item"
			continue
		if bStart==0:
			continue
		output_data(j_list[index])
		
		sNum += 1
		if sNum>param_config['Number']:
			break

def handle_argument():
	optlist, args = getopt.getopt(sys.argv[1:], 'c:d:n:')
	for option, value in optlist:
		if option in ["-d","--date"]:
			param_config["Date"] = value
		elif option in ["-c","--code"]:
			param_config["Code"] = (value)
		elif option in ["-n","--number"]:
			param_config["Number"] = int(value)
	#print param_config

param_config = {
	"Date":'',
	"Number":30,
	"Format":'json',
}
REAL_DAILY_PRE_FD = "../data/daily/"

#Main Start:
if __name__=='__main__':
	beginTm = datetime.datetime.now()
	handle_argument()
	if param_config["Date"]=='':
		print "Error:Must add arg -d([YYYY]MMDD)"
		exit(0)
	elif param_config["Code"]=='':
		print "Error:Must add arg -c([code1][,code2]...)"
		exit(0)

	hisDt = param_config["Date"]
	ret, hisDate = parseDate2(hisDt)
	year = hisDate[:4]
	
	'''
	jcLoc = "../data/entry/juchao/" + year + '/jc' + hisDate + ".txt"
	if os.path.exists(jcLoc) is False:
		print(jcLoc,"not exist.")
		exit(0)
	jc_dict = {}
	read_tfp_fh_in_tips(jcLoc, jc_dict)
	'''
	
	codeArray = param_config["Code"].split(',')
	for code in codeArray:
		print code
		if param_config["Format"]=='':
			kPath = REAL_DAILY_PRE_FD + year + '/' + 'kday_' + code + ".txt"
			if os.path.exists(kPath) is False:
				print "lst File not exist", kPath
				continue
		elif param_config["Format"]=='json':
			kPath = REAL_DAILY_PRE_FD + year + '/json/' + 'j' + code + ".txt"
			#print kPath
			if os.path.exists(kPath) is False:
				print "lst File not exist", kPath
				continue
		else:
			print "Error: unsupport format", param_config["Format"]
			break

		kFile = open(kPath, "r")
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
			show_code_perform(lobj, hisDate)
			print ''
			'''
			mDate = obj[len(obj)-1]
			if len(mDate)<10:
				print(obj[0], "Invalid date", mDate)
			markDt = mDate[:10]
			select_all_trade_stk(lobj, hisDt, obj[0], obj[1], markDt, jc_dict, allist)
			'''
		kFile.close()
