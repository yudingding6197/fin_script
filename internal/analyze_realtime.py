#!/usr/bin/env python
# -*- coding:utf8 -*-
import os
import urllib2,time
import datetime
import sys
sys.path.append('.')
from internal.realtime_obj import *
from internal.trade_date import *

REAL_PRE_FD = "../data/"

def get_rt_time(f, dtObj):
	line = f.readline()
	while line:
		objs = re.match("TIME: (.*)", line)
		if objs is not None:
			dt = datetime.datetime.strptime(objs.group(1), "%Y-%m-%d %H:%M")
			if dt.hour>=15:
				#print "Find matched line", line
				dtObj.append(dt)
				return 0
		line = f.readline()
		continue
	return -1

#找到显示日期那一行，然后就可以处理统计数据了
def match_rt_date(f):
	line = f.readline()
	while line:
		objs = re.match("(\d+)-(\d+)-(\d+)", line)
		if objs is not None:
			#print "date line", line
			return 0
		line = f.readline()
	return -1
	
def parse_summary_info(f, stcsItem):
	#print(f.filename)
	line = f.readline()
	#这是强制找到匹配的第一行
	'''
	while line:
		objs = re.match(".*ST\((\d+) ZT (\d+) DT\)(.*)", line)
		#print(line, objs)
		if objs is not None:
			break
		line = f.readline()
	'''
	
	#print("parse_summary_info", line)
	while line:
		objs = re.match(".*ST\((\d+) ZT (\d+) DT\)(.*)", line)
		#print(line, objs)
		if objs is not None:
			break
		
		#判断访问超时导致的错误信息
		if line[:2]=="['":
			pass
		elif line[:4]=="<url":
			pass
		elif line[:6]=="timed ":
			pass
		else:
			print("Error: Get ZT DT fail", line)
			return -1
		line = f.readline()
	stcsItem.s_st_yzzt = int(objs.group(1))
	stcsItem.s_st_yzdt = int(objs.group(2))
	
	com_str = objs.group(3)
	objs = com_str.split(',')
	#print(len(objs), objs[0])
	for i in range(0, len(objs)):
		items = re.match('[\t ]+(\d+)[\t ]+(.*)', objs[i])
		#print(i, objs[i], items.groups())
		value = int(items.group(1))
		tname = items.group(2)
		if tname=='DTKP':
			stcsItem.s_open_dt = value
		elif tname=='YZDT':
			stcsItem.s_yzdt = value
		elif tname=='DTDK':
			stcsItem.s_open_dt_dk = value
		elif tname=='DaoT ':
			stcsItem.s_dt_daoT = value
		else:
			print("Warning: ======== unknown", items.groups());
	
	line = f.readline()
	while line:
		objs = re.match(".*(\d+)\-ZT[\t ]+(\d+)\-DT[\t ]+(\d+)\-X[\t ]+(\d+)--(.*)", line)
		#print(line, objs)
		if objs is None:
			print("Error: parse fail1", line)
			return -1
		stcsItem.s_zt = int(objs.group(1))
		stcsItem.s_dt = int(objs.group(2))
		stcsItem.s_new = int(objs.group(3))
		stcsItem.s_yzzt = int(objs.group(4))
		
		line = objs.group(5)
		cond = "\((\d+)\+(\d+)\)[\t ]+\[(\d+) (\d+) (\d+) (\d+)\][\t ]+(\d+) 上,[\t ]*(\d+) 下"
		objs = re.match(cond.decode('utf8').encode('gbk'), line)
		#print(line, objs)
		if objs is None:
			print("Error: parse fail2", line)
			return -1
		stcsItem.s_cx_yz = int(objs.group(1))
		stcsItem.s_non_cx_yz = int(objs.group(2))
		stcsItem.s_open_zt = int(objs.group(3))
		stcsItem.s_close_zt = int(objs.group(4))
		stcsItem.s_open_T_zt = int(objs.group(5))
		stcsItem.s_dk_zt = int(objs.group(6))
		stcsItem.s_sw_zt = int(objs.group(7))
		stcsItem.s_xw_zt = int(objs.group(8))

		break
		
	line = f.readline()
	while line:
		cond = ".*(\d+)\-CG\((\d+)\)[\t ]+(\d+)\-FT\((\d+)\)[\t ]+(\d+)\-YIN  KD:\[(.*)\]"
		objs = re.match(cond, line)
		#print(line, objs)
		if objs is None:
			print("Error: parse fail1", line)
			return -1
		stcsItem.s_zthl = int(objs.group(1))
		#stcsItem.s_kd  not defined, only lst_kd
		stcsItem.s_dtft = int(objs.group(3))
		#stcsItem.s_ftq  not defined, only lst_dtft
		stcsItem.s_zt_o_gt_c = int(objs.group(5))
		#_____ TODO: KD stocks
		if objs.group(6)=="":
			break
		objs = objs.group(5).split(',')
		for item in objs:
			stcsItem.lst_kd.append(item)
		break

	line = f.readline()
	while line:
		#cond = "[ ]+(\d+)\([ ]+(\d+)\)[\t ]+ZERO:[\t ]+(\d+)[\t ]+(\d+)[\t ]+\([\t ]+(\d+)\)"
		cond  = "[ ]*(\d+)\([ ]*(\d+)\)[\t ]*ZERO:[\t ]+(\d+)[\t ]*(\d+)[\t ]*\([\t ]*(\d+)\)"
		objs = re.match(cond, line)
		#print(line, objs)
		if objs is None:
			print("Error: parse fail1", line)
			return -1
		stcsItem.s_open_sz = int(objs.group(1))
		stcsItem.s_open_dz = int(objs.group(2))
		stcsItem.s_open_pp = int(objs.group(3))
		stcsItem.s_open_xd = int(objs.group(4))
		stcsItem.s_open_dd = int(objs.group(5))
		break

	line = f.readline()
	while line:
		cond  = "[ ]*(\d+)\([ ]*(\d+)\)[\t ]*ZERO:[\t ]+(\d+)[\t ]*(\d+)[\t ]*\([\t ]*(\d+)\)"
		objs = re.match(cond, line)
		#print(line, objs)
		if objs is None:
			print("Error: parse fail1", line)
			return -1
		stcsItem.s_close_sz = int(objs.group(1))
		stcsItem.s_close_dz = int(objs.group(2))
		stcsItem.s_close_pp = int(objs.group(3))
		stcsItem.s_close_xd = int(objs.group(4))
		stcsItem.s_close_dd = int(objs.group(5))
		break

	line = f.readline()
	while line:
		cond = "4\%:[ ]*(\d+)[\t ]+(\d+)"
		objs = re.match(cond, line)
		#print(line, objs)
		if objs is None:
			print("Error: parse fail1", line)
			return -1
		stcsItem.s_high_zf = int(objs.group(1))
		stcsItem.s_low_df = int(objs.group(2))
		break

	return 0

def parse_kb_cx(line, stcsItem):
	cond = '(.*?)\((\d+),(.*?)\),(.*)'
	obj = re.match(cond, line)
	while obj:
		left = obj.group(4)
		name = obj.group(1).strip()
		ilist = [name, obj.group(2), obj.group(3).strip()]
		#print obj.group(1),"#",obj.group(2),"#",obj.group(3)
		#print "left", left
		stcsItem.lst_kbcx.append(ilist)

		obj = re.match(cond, left)
	return
		
	
#获得开班CX的信息
def parse_cixin_item(f, stcsItem):
	line = f.readline()
	while line:
		if line=="CXKB:\n":
			#line = f.readline()
			#break
			pass
		elif line=="CXKB:=====\n":
			#break
			pass
		elif line=="\n":
			#line = f.readline()
			break
		elif len(line)>10 and line[:5]=="#####":
			print("Error: Read next block")
			return -1
		else:
			line = line.strip()
			parse_kb_cx(line, stcsItem)
			#print ("%d: '%s'" % (len(line), line))
		line = f.readline()
	return 0

def parse_total_line(line, stcsItem):
	#tol_str = "Total( %d = %d + %d	YZ: %d=%d(%d)+%d   %d CXZT,%d CXDT ):"
	#tol_str%( stcsItem.s_zt, stcsItem.s_zt-non_cx, non_cx, stcsItem.s_yzzt, cx_yz, stcsItem.s_cx_yzzt, non_cx_yz, stcsItem.s_cxzt, stcsItem.s_cxdt)
	cond = "Total\( (\d+) = (\d+) \+ (\d+)	YZ: (\d+)=(\d+)\((\d+)\)\+(\d+)   (\d+) CXZT,(\d+) CXDT \):"
	objs = re.match(cond, line)
	if objs is None:
		print("Error, Total line", line)
		return -1
	#print(objs, line)
	stcsItem.s_zt = int(objs.group(1))
	#已经保存该值
	if stcsItem.s_cx_yz!=int(objs.group(2)):
		print("Error: CX_YZ",stcsItem.s_cx_yz,objs.group(2))
	#stcsItem.s_non_cx_zt = int(objs.group(3))
	if stcsItem.s_yzzt!=int(objs.group(4)):
		print("Error: CX_YZ",stcsItem.s_yzzt,objs.group(4))
	#stcsItem.s_yzzt = int(objs.group(4))
	if stcsItem.s_cx_yz!=int(objs.group(5)):
		print("Error: CX_YZ",stcsItem.s_cx_yz,objs.group(5))
	#stcsItem.s_cx_yz = int(objs.group(5))
	stcsItem.s_cx_yzzt = int(objs.group(6))
	#stcsItem.non_cx_yz = int(objs.group(7))
	stcsItem.s_cxzt = int(objs.group(8))
	stcsItem.s_cxdt = int(objs.group(9))
	return 0

def parse_nb_jc_item(f, stcsItem):
	ret = 0
	line = f.readline()
	while line:
		if line=="NB:\n":
			line = f.readline()
			#break
		elif line=="JC:\n":
			line = f.readline()
			pass
		elif line[:5]=="Total":
			#print(line)
			#print("line is EMPTY")
			ret = parse_total_line(line, stcsItem)
			break
		elif len(line)>10 and line[:5]=="#####":
			print("Error: Read next block")
			return -1
		else:
			print("Error: NB_JC line", line)
			return -1
		line = f.readline()
	return ret

def parse_zdt_item(f, stcsItem, zdt_type):
	#fmt1 = "%2d %6s %-7s	%8.2f %8.2f %8.2f %8.2f %8.2f %4d %3s"
	#fmt2 = "%2d %6s %-7s	%8.2f %8.2f %8.2f %8.2f %8.2f %4d %3s %9s"
	#fmt3 = "%2d %6s %-7s	%8.2f %8.2f %8.2f %8.2f %8.2f %4d %3s %9s %9s"
	head = "[ ]*(\d+) (.*)[\t ]+"
	lprice = "[\-]?(\d+\.\d+)[ ]*(\d+\.\d+)[ ]*[\-]?(\d+\.\d+)[ ]*[\-]?(\d+\.\d+)[ ]*[\-]?(\d+\.\d+)[ ]*"
	line = f.readline()
	while line:
		#print(zdt_type, line)
		stkList = []
		if line=="\n":
			break

		if zdt_type==1:
			cond = head + lprice + "(\d+) (.*)"
			stkList = stcsItem.lst_non_yzcx_yzzt
		elif zdt_type==2:
			cond = head + lprice + "(\d+) (.*)"
			stkList = stcsItem.lst_non_yzcx_zt
		elif zdt_type==3:
			cond = head + lprice + "(\d+) (.*)"
			stkList = stcsItem.lst_non_yzcx_zthl
		elif zdt_type==4:
			cond = head + lprice + "(\d+) (.*)"
			stkList = stcsItem.lst_yzdt
		elif zdt_type==5:
			cond = head + lprice + "(\d+) (.*)"
			stkList = stcsItem.lst_dt
		elif zdt_type==6:
			cond = head + lprice + "(\d+) (.*)"
			stkList = stcsItem.lst_dtft
		else:
			line = f.readline()
			continue
		objs = re.match(cond, line)
		if objs is None:
			print(objs, line)
			return -1
		#print(zdt_type, objs.group(2)[7:] )
		code = objs.group(2)[:6]
		name = objs.group(2)[7:].replace(" ", "").replace("\t","").strip()
		change_percent = float(objs.group(3))
		price = float(objs.group(4))
		open_percent = float(objs.group(5))
		high_zf_percent = float(objs.group(6))
		low_df_percent = float(objs.group(7))
		count = int(objs.group(8))
		desc = objs.group(9)
		item = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent, count, desc]
		stkList.append(item)

		line = f.readline()
	return 0

#解析ZT(YZZT ZT ZTHL), DT(YZDT DT DTFT) 6种ZDT数据
def parse_zt_dt_stcs(f, stcsItem):
	line = f.readline()
	objs = re.match("id[ ]+code(.*)", line)
	if objs is None:
		print("Error: desc error", line)
		return -1
	
	line = f.readline()
	while line:
		if line[:7]=="YZZT  [":
			parse_zdt_item(f, stcsItem, 1)
			pass
		elif line[:5]=="ZT  [":
			parse_zdt_item(f, stcsItem, 2)
			pass
		elif line[:6]=="ZTHL [":
			parse_zdt_item(f, stcsItem, 3)
			pass
		elif line[:5]=="Total":
			break
		else:
			print("Error: ZT issue", line)
			return -1
		line = f.readline()

	line = f.readline()
	while line:
		if line[:7]=="YZDT  [":
			parse_zdt_item(f, stcsItem, 4)
			pass
		elif line[:5]=="DT  [":
			parse_zdt_item(f, stcsItem, 5)
			pass
		elif line[:7]=="DTFT  [":
			parse_zdt_item(f, stcsItem, 6)
			pass
		elif line=="\n":
			break
		else:
			print("Error: DT issue", line)
			return -1
		line = f.readline()
	return 0

def parse_realtime_his_file(trade_day, stcsItem):
	filename = get_path_by_tdate(trade_day)
	if filename=='':
		return -1

	if not os.path.isfile(filename):
		print("Error: not find ",filename)
		return -1
	
	#print("realtime file", filename)
	f = open(filename, 'r')

	dtObj = []
	ret = get_rt_time(f, dtObj)
	if ret==-1:
		print ("Not find matched rt time, Re-get latest realtime")
		return -1
	#print(len(dtObj), dtObj)
	
	ret = match_rt_date(f)
	stcsItem.s_date = trade_day

	ret = parse_summary_info(f, stcsItem)
	if ret==-1:
		return ret

	ret = parse_cixin_item(f, stcsItem)
	if ret==-1:
		return ret

	ret = parse_nb_jc_item(f, stcsItem)
	if ret==-1:
		return ret

	ret = parse_zt_dt_stcs(f, stcsItem)
	if ret==-1:
		return ret

	ret = get_rt_time(f, dtObj)
	#print(len(dtObj), dtObj)

	f.close()
	
	if len(dtObj)==0:
		print("Error: no matched time", filename)
		return -1
	elif len(dtObj)==1:
		print("Warning: only time0", filename)
	if dtObj[0].hour<15:
		print("Warning: time0 < 15", filename, dtObj[0].hour, dtObj[0].minute)
	if len(dtObj)>1:
		if dtObj[1].hour<15:
			print("Warning: time1 < 15", filename, dtObj[1].hour, dtObj[1].minute)
		if (dtObj[1]-dtObj[0]).seconds<=0:
			print("Warning: time issue", filename)
	return 0

def get_path_by_tdate(pre_day):
	filename = REAL_PRE_FD + 'entry/realtime/' + 'rt_' + pre_day + '.txt'
	if os.path.isfile(filename):
		return filename
	syear = pre_day[:4]
	filename = REAL_PRE_FD + 'entry/realtime/' + syear + '/rt_' + pre_day + '.txt'
	if os.path.isfile(filename):
		return filename
	print("Warning: not find file",pre_day)
	return ''

#Main
if __name__=='__main__':
	trade_date = get_lastday()
	pre_date = get_preday(1, trade_date)	
	preStatItem = statisticsItem()
	ret = parse_realtime_his_file(pre_date, preStatItem)
	for item in preStatItem.lst_non_yzcx_yzzt:
		print item[0],item[1]
	print "-----\n"
	for item in preStatItem.lst_non_yzcx_zt:
		print item[0],item[1]
	pass
