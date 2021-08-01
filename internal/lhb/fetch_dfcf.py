#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import re
import datetime
import getopt
import json

sys.path.append('.')
from internal.trade_date import *
from internal.global_lhb import *
from internal.url_dfcf.dc_lhb_daily import *

def handle_lhb_dtl_cont(scode,sname,curDate,content,lhbList):
	obj = json.loads(content)
	#检查data
	dictObj = obj["Data"][0]
	dictObj["code"] = scode
	lhbList.append(dictObj)
	return

#通过解析LHB summary的时候，获取每一个item的详细数据并保存
def ready_get_lhb_detail(filename, detailFile, curDate):
	if param_config["Full"]==0:
		return
	if (os.path.exists(detailFile)):
		return

	file = open(filename, 'r')
	smObj = json.load(file)
	file.close()
	#print type(smObj["Data"][0]["Data"])
	#print (smObj["Message"], smObj["Status"])
	#print (smObj["Data"][0]["Data"][0])
	allItems = smObj["Data"][0]["Data"]
	splitDef = smObj["Data"][0]["SplitSymbol"]
	fieldObjs = smObj["Data"][0]["FieldName"].split(',')
	typeIdx = fieldObjs.index("Ctypedes")
	stkList = []
	lhbDtlList = []
	for i,val in enumerate(allItems):
		obj = val.split(splitDef)
		#print i, obj[0], obj[1], obj[typeIdx]
		if obj[0] not in stkList:
			#continue
			stkList.append(obj[0])
			content = fetch_lhb_stk_detail(obj[0],curDate)
			if content=='':
				return
			handle_lhb_dtl_cont(obj[0],obj[1],curDate,content,lhbDtlList)
		else:
			#print "Repeat", obj[0], obj[1]
			pass

		#for j in range(len(obj)):
		#	print j,obj[j]
		#break
	if len(lhbDtlList)==0:
		print("%s is NULL???"%(curDate))
		return
	#print lhbDtlList
	
	file = open(detailFile,'w')
	val = json.dumps(lhbDtlList,ensure_ascii=False)
	#print(val)
	file.write(val.encode('utf8'))
	file.close()

#通过解析LHB summary，解析其中关键字是否在LHB全局变量中定义
def parse_lhb_summary_debug(filename, detailFile, curDate):
	if not os.path.exists(filename):
		print("Error: not exist file", filename)
		return

	file = open(filename, 'r')
	smObj = json.load(file)
	file.close()
	#print type(smObj["Data"][0]["Data"])
	#print (smObj["Message"], smObj["Status"])
	#print (smObj["Data"][0]["Data"][0])
	allItems = smObj["Data"][0]["Data"]
	splitDef = smObj["Data"][0]["SplitSymbol"]
	fieldObjs = smObj["Data"][0]["FieldName"].split(',')
	typeIdx = fieldObjs.index("Ctypedes")
	stkList = []
	lhbDtlList = []
	bTitle=0
	for i,val in enumerate(allItems):
		obj = val.split(splitDef)
		#print i, obj[0], obj[1], obj[typeIdx]
		if obj[0] not in stkList:
			#continue
			stkList.append(obj[0])
		else:
			#print "Repeat", obj[0], obj[1]
			pass

		if obj[typeIdx] in g_LHB_desc.iterkeys():
			#print i, g_LHB_desc[obj[typeIdx]], obj[0], obj[1], obj[typeIdx]
			pass
		else:
			#进行二次比较，去掉真正百分比
			origStr=obj[typeIdx]
			reObj = re.match(r"([^-\d]*)(.*)%(.*)", origStr)
			if reObj:
				desc = reObj.group(1)
				#print reObj.groups(), desc
				if origStr.find(u"异常期间价格")!=-1 and origStr.find("ST")!=-1:
					desc += "ST"
				elif origStr.find(u"有价格涨跌幅限制的连续")!=-1:
					if origStr.find(u"跌幅偏离值")!=-1:
						desc += "-"
					elif origStr.find(u"涨幅偏离值")!=-1:
						desc += "+"
				#print obj[typeIdx], "---", desc
				if desc not in g_LHB_desc.iterkeys():
					if bTitle==0:
						print(curDate)
						bTitle=1
					print i, obj[0], obj[1], obj[typeIdx]
			else:
				if bTitle==0:
					print(curDate)
					bTitle=1
				print "===",i, obj[0], obj[1], obj[typeIdx]
	return

def fetch_dfcf_lhb_action(filepath, fileDetail, base_date):
	#先检查summary文件是否存在，不存在则下载
	if not os.path.exists(filepath):
		content = fetch_dfcf_lhb_summary(base_date, base_date, '')	
		if content != '':
			lhb_fl = open(filepath, 'w+')
			lhb_fl.write(content)
			lhb_fl.close()
		else:
			print ("Get %s LHB fail"%(base_date))
			return
	#然后检查详细数据文件是否存在
	if os.path.exists(fileDetail):
		return
	ready_get_lhb_detail(filepath, fileDetail, base_date)



def handle_argument():
	optlist, args = getopt.getopt(sys.argv[1:], 's:e:c:f:')
	for option, value in optlist:
		if option in ["-s","--startdate"]:
			param_config["StartDate"] = value
		elif option in ["-e","--enddate"]:
			param_config["EndDate"] = value
		elif option in ["-c","--count"]:
			param_config["Count"] = int(value)
		elif option in ["-f","--full"]:
			param_config["Full"] = 1
		elif option in ["-q","--tuishi"]:
			param_config["TuiShi"] = 1
	#print param_config

param_config = {
	"StartDate":"",
	"EndDate":"",
	"Count":0,
	"Full":1,
	"TuiShi":0,
	"Exchange":0,
}

#Main Start:
if __name__=='__main__':
	handle_argument()
	trade_date = get_lastday()

	if param_config["Count"] != 0:
		edate = trade_date
	else:
		if param_config["StartDate"]=='' or param_config["StartDate"]=='.':
			param_config["StartDate"] = trade_date
			sdate = trade_date
		else:
			ret, sdate = parseDate2(param_config["StartDate"])
			if ret==-1:
				exit(-1)

		if param_config["EndDate"]=='' or param_config["EndDate"]=='.':
			param_config["EndDate"] = trade_date
			edate = trade_date
		else:
			ret, edate = parseDate2(param_config["EndDate"])
			if ret==-1:
				exit(-1)

	init_trade_list(trade_date)
	if param_config["Count"] != 0:
		sdate = get_preday(param_config["Count"], trade_date)
		#print("sssss", sdate)
	
	startDt = datetime.datetime.strptime(sdate, '%Y-%m-%d').date()
	endDt = datetime.datetime.strptime(edate, '%Y-%m-%d').date()
	stepDt = startDt

	while (endDt-stepDt).days>=0:
		base_date = LHB_date_fmt %(stepDt.year, stepDt.month, stepDt.day)
		#print ("bs_date", base_date)
		#read_st_in_daily_tips(base_date, stk_list, stk_dict)

		if not is_trade_date(base_date):
			stepDt += datetime.timedelta(days=1)
			continue
		#print base_date
		filepath = LHB_fileFmt % (LHB_folder, base_date[:4], base_date)
		fileDetail = LHB_fileFmtDtl % (LHB_folder, base_date[:4], base_date)
		if (os.path.exists(filepath)):
			stepDt += datetime.timedelta(days=1)
			#如果summary文件存在，再检查详细文件。不存在则下载
			fetch_lhb_detail_data(filepath, fileDetail, base_date)
			continue

		fetch_dfcf_lhb_action(filepath, fileDetail, base_date)
		stepDt += datetime.timedelta(days=1)
	release_trade_list()
