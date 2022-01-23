#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import re
import os
import datetime
import getopt
import json

from internal.trade_date import *
from internal.global_lhb import *
from internal.url_dfcf.dc_lhb_daily import *
from internal.lhb.fetch_dfcf import *

#-d download data
#-g debug lhb summary data
def show_lhb_info(contObj, lstDef):
	resultFmtF="%6s %-7s	%6.2f	%6.2f	%6.2f	%6.2f	%6.2f"
	for lstItem in contObj:
		if lstItem["code"] not in lstDef:
			continue
		head3 = lstItem["code"][:3]
		if head3=='200' or head3=='201' or head3=='900':
			continue
		fieldObj = lstItem["FieldName"].split(',')
		#有的上榜营业部没有10个
		dtLen = len(lstItem["Data"])
		lstTotal = lstItem["Data"][dtLen-1].split('|')
		smoneyIdx = fieldObj.index("Smoney")
		sMy = float(lstTotal[smoneyIdx])/1000000
		bmoneyIdx = fieldObj.index("Bmoney")
		bMy = float(lstTotal[bmoneyIdx])/1000000
		
		srateIdx = fieldObj.index("Srate")
		sRt = float(lstTotal[srateIdx])
		brateIdx = fieldObj.index("Brate")
		bRt = float(lstTotal[brateIdx])
		nameIdx = fieldObj.index("SName")
		#print "		", lstItem["code"], lstTotal[nameIdx]
		#print lstItem["Data"][10]
		print(resultFmtF%(lstItem["code"],lstTotal[nameIdx],(bRt-sRt), bMy, bRt, sMy, sRt))
	return

def analyse_lhb_content(filename, detailFile, curDate):
	if not os.path.exists(filename):
		print("No data for", filename)
		return
	if not os.path.exists(fileDetail):
		print("No data for", fileDetail)
		return

	file = open(filename, 'r')
	sumryObj = json.load(file)
	file.close()

	file = open(detailFile, 'r')
	contObj = json.load(file)
	file.close()

	allItems = sumryObj["Data"][0]["Data"]
	splitDef = sumryObj["Data"][0]["SplitSymbol"]
	fieldObjs = sumryObj["Data"][0]["FieldName"].split(',')
	typeIdx = fieldObjs.index("Ctypedes")
	stkList = []
	lstZhang = []
	lstZhen = []
	lstHs = []
	for i,val in enumerate(allItems):
		obj = val.split(splitDef)
		#print i, obj[0], obj[1], obj[typeIdx]
		if obj[typeIdx] in g_LHB_desc.iterkeys():
			if g_LHB_desc[obj[typeIdx]]==g_LHB_zhang:
				#print i, g_LHB_desc[obj[typeIdx]], obj[0], obj[1], obj[typeIdx]
				lstZhang.append(obj[0])
			elif g_LHB_desc[obj[typeIdx]]==g_LHB_zhen:
				#print i, g_LHB_desc[obj[typeIdx]], obj[0], obj[1], obj[typeIdx]
				lstZhen.append(obj[0])
			elif g_LHB_desc[obj[typeIdx]]==g_LHB_hs:
				#print i, g_LHB_desc[obj[typeIdx]], obj[0], obj[1], obj[typeIdx]
				lstHs.append(obj[0])
			pass
		else:
			#print i, obj[0], obj[1], obj[typeIdx]
			pass
		#for j in range(len(obj)):
		#	print j,obj[j]
		#break
	print curDate
	print("ZHANG")
	show_lhb_info(contObj, lstZhang)
	print("ZHENFU")
	show_lhb_info(contObj, lstZhen)
	print("HUANSHOU")
	show_lhb_info(contObj, lstHs)
	print("")

	return

def handle_argument():
	optlist, args = getopt.getopt(sys.argv[1:], 's:e:c:fdg')
	for option, value in optlist:
		if option in ["-s","--startdate"]:
			param_config["StartDate"] = value
		elif option in ["-e","--enddate"]:
			param_config["EndDate"] = value
		elif option in ["-c","--count"]:
			param_config["Count"] = int(value)
		elif option in ["-f","--full"]:
			param_config["Full"] = 0
		elif option in ["-d","--download"]:
			param_config["Download"] = 1
		elif option in ["-g","--debug"]:
			param_config["Debug"] = 1
	#print param_config

param_config = {
	"StartDate":"",
	"EndDate":"",
	"Count":0,
	"Full":1,
	"Download":0,
	"Debug":0,
}

#Main Start:
if __name__=='__main__':
	handle_argument()
	trade_date = get_lastday()

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

		filepath = LHB_fileFmt % (LHB_folder, base_date[:4], base_date)
		fileDetail = LHB_fileFmtDtl % (LHB_folder, base_date[:4], base_date)
		if param_config["Download"]==1:
			#print(filepath)
			fetch_dfcf_lhb_action(filepath, fileDetail, base_date)
			stepDt += datetime.timedelta(days=1)
			continue
		if param_config["Debug"]==1:
			parse_lhb_summary_debug(filepath, fileDetail, base_date)
			stepDt += datetime.timedelta(days=1)
			continue

		analyse_lhb_content(filepath, fileDetail, base_date)
		stepDt += datetime.timedelta(days=1)
	release_trade_list()
