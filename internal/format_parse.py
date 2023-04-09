# -*- coding:gbk -*-
import sys
import re
import os
import datetime

from global_var import g_shcd
from global_var import g_szcd

# _____ debug print log
def loginfo1(flag=0):
	if (flag==1):
		frame = None
		try:
			raise  ZeroDivisionError
		except  ZeroDivisionError:
			frame = sys.exc_info()[2].tb_frame.f_back
		print "%s in line %d" %(str(datetime.datetime.now()), frame.f_lineno)

#TODO: 将mode参数改为字符，'dc','qq','sn','wy'...
def parseCode(code, mode='sn'):
	if (len(code) != 6):
		sys.stderr.write("Len should be 6\n")
		return (-1, '')

	head3 = code[0:3]
	if mode=='dc':
		if head3 in g_szcd:
			ncode = code + '2'
		else:
			if head3 in g_shcd:
				ncode = code + '1'
			else:
				print "非法代码:" +code+ "\n"
				return (-1, '')
	elif mode=='sn':
		if head3 in g_szcd:
			ncode = 'sz' + code
		else:
			if head3 in g_shcd:
				ncode = 'sh' + code
			else:
				print code
				str = "非法代码:" +code+ "\n"
				print str.encode('utf8')
				return (-1, '')
	elif mode=='wy':
		if head3 in g_szcd:
			ncode = '1' + code
		else:
			if head3 in g_shcd:
				ncode = '0' + code
			else:
				print "非法代码:" +code+ "\n"
				return (-1, '')
	elif mode=='dc_push2':
		if head3 in g_szcd:
			ncode = '0.' + code
		else:
			if head3 in g_shcd:
				ncode = '1.' + code
			else:
				print "非法代码:" +code+ "\n"
				return (-1, '')
		return (0, ncode)
	else:
		print("WIP parse code fmt", mode)
		return (-1, '')
	return (0, ncode)

def parseDate(qdate, today, ai=0):
	dateObj = re.match(r'^(\d{4})(\d{2})(\d{2})', qdate)
	if (dateObj is None):
		dateObj = re.match(r'^(\d{2})(\d{2})', qdate)
		if (dateObj is None):
			print "非法日期格式：" +qdate+ ",期望格式:YYYYMMDD or MMDD"
			return (-1, '')
		else:
			if len(qdate)>4:
				print "非法日期格式：" +qdate+ ",期望格式:YYYYMMDD or MMDD"
				return (-1, '')
			year = today.year
			month = int(dateObj.group(1))
			day = int(dateObj.group(2))
	else:
		year = int(dateObj.group(1))
		month = int(dateObj.group(2))
		day = int(dateObj.group(3))
	strdate = '%04d-%02d-%02d' %(year, month, day)

	try:
		newdate = datetime.date(year,month,day)
	except:
		print strdate, "is invalid date"
		return (-1, '')
	if ai==1:
		delta = newdate-today
		if delta.days>10:
			year -= 1
			strdate = '%04d-%02d-%02d' %(year, month, day)
	return (0, strdate)

def parseDate2(qdate, con_ch='-'):
	dlen = len(qdate)
	beginTm = datetime.datetime.now()
	dateObj = None
	if '-' in qdate:
		if dlen==10:
			dateObj = re.match(r'^(\d{4})-(\d{2})-(\d{2})', qdate)
			year = int(dateObj.group(1))
			month = int(dateObj.group(2))
			day = int(dateObj.group(3))
		elif dlen==8:
			dateObj = re.match(r'^(\d{2})-(\d{2})-(\d{2})', qdate)
			year = 2000+int(dateObj.group(1))
			month = int(dateObj.group(2))
			day = int(dateObj.group(3))
		elif dlen==5:
			dateObj = re.match(r'^(\d{2})-(\d{2})', qdate)
			year = beginTm.year
			month = int(dateObj.group(1))
			day = int(dateObj.group(2))
		else:
			print("非法日期 %s,期望格式:YYYY-MM-DD or YY-MM-DD or MM-DD"%(qdate))
			return (-1, '')
	else:
		if dlen==8:
			dateObj = re.match(r'^(\d{4})(\d{2})(\d{2})', qdate)
			year = int(dateObj.group(1))
			month = int(dateObj.group(2))
			day = int(dateObj.group(3))
		elif dlen==6:
			dateObj = re.match(r'^(\d{2})(\d{2})(\d{2})', qdate)
			year = 2000+int(dateObj.group(1))
			month = int(dateObj.group(2))
			day = int(dateObj.group(3))
		elif dlen==4:
			dateObj = re.match(r'^(\d{2})(\d{2})', qdate)
			year = beginTm.year
			month = int(dateObj.group(1))
			day = int(dateObj.group(2))
		else:
			print("非法日期 %s,期望格式:YYYYMMDD or YYMMDD or MMDD"%(qdate))
			return (-1, '')

	#验证日期的合法性
	try:
		datetime.date(year,month,day)
	except:
		print year, month, day, "is invalid date"
		return (-1, '')

	strdate = '%04d%s%02d%s%02d' %(year, con_ch, month, con_ch, day)
	return (0, strdate)

def parseTime(qtime):
	timeObj = re.match(r'^(\d{2}):(\d{2}):(\d{2})', qtime)
	if (timeObj is None):
		print "非法时间格式：" +qtime+ ",期望格式:HH:MM:SS"
		return (-1, -1, -1, -1)

	hour = int(timeObj.group(1))
	minute = int(timeObj.group(2))
	second = int(timeObj.group(3))
	return (0, hour, minute, second)

def time_range(firstHour, firstMinute, hour, minute, interval):
	bMatch = 0
	if firstMinute<interval:
		if (hour==firstHour and minute<=firstMinute):
			bMatch = 1
		elif ((firstHour-hour==1) and minute>=(60-interval+firstMinute)):
			bMatch = 1
	else:
		if (hour==firstHour and firstMinute-minute<=5):
			bMatch = 1
	return bMatch
