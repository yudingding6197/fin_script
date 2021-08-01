#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import re
import os
import datetime
import getopt
import json

#from internal.trade_date import *
from internal.url_juchao.yidong_res import *

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

def show_hecha(ydObj, year):
	fmt = "%6s %-7s	%11s  %s"
	print(year)
	for item in ydObj:
		value = fmt%(item['secCode'],item['secName'],item['adjunctUrl'][10:20],item['announcementTitle'])
		print value
	
def handle_argument():
	optlist, args = getopt.getopt(sys.argv[1:], 's:e:c:fd:gh')
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
			param_config["Download"] = value
		elif option in ["-g","--debug"]:
			param_config["Debug"] = 1
		elif option in ["-h","--help"]:
			print("-d[(year)|. '.' means this year")
			exit(0)
	#print param_config

param_config = {
	"StartDate":"",
	"EndDate":"",
	"Count":0,
	"Full":1,
	"Download":0,
	"Debug":0,
}

HECHA_PRE_FD = "../data/entry/juchao/hecha"

#Main Start:
if __name__=='__main__':
	handle_argument()
	nowDate = datetime.datetime.now()
	currTm = "%d-%02d-%02d" %(nowDate.year, nowDate.month, nowDate.day)

	istYear = 0
	iedYear = 0
	if param_config["StartDate"] == '.' or param_config["StartDate"] == '':
		istYear = int(currTm[:4])
	else:
		istYear = int(param_config["StartDate"][:4])
		
	if param_config["EndDate"] == '.' or param_config["EndDate"] == '':
		iedYear = int(currTm[:4])
	else:
		iedYear = int(param_config["EndDate"][:4])

	if not (istYear>2000 or istYear<=int(currTm[:4])):
		print("Out of range start year", istYear)
		exit()
	if not (iedYear>2000 or iedYear<=int(currTm[:4])):
		print("Out of range end year", iedYear)
		exit()

	keyword = "停牌核查"
	for year in range(istYear, iedYear+1):
		filename = "tingpai_hecha_%d.txt"%(year)
		fullpath = os.path.join(HECHA_PRE_FD,filename)
		#如果是今年，始终下载。不是今年，以前的年份不存在则下载
		if year==nowDate.year:
			sDate = "%d-%s"%(year, '01-01')
			eDate = "%d-%s"%(year, currTm[5:])
			fetch_yidong_hecha(fullpath, keyword, sDate, eDate)
		else:
			if not os.path.exists(fullpath):
				sDate = "%d-%s"%(year, '01-01')
				eDate = "%d-%s"%(year, '12-31')
				fetch_yidong_hecha(fullpath, keyword, sDate, eDate)

		file = open(fullpath,'r')
		#obj = json.load(file)
		obj = json.load(file, encoding='utf-8')
		file.close()
		show_hecha(obj, year)
		print('')