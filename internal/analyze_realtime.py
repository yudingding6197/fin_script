#!/usr/bin/env python
# -*- coding:utf8 -*-
import os
import urllib2,time
import datetime
import sys
sys.path.append('.')
from internal.realtime_obj import *
from internal.trade_date import *

REALTM_PRE_FD = "../data/"

def get_rt_props(f, dtObj, verObj, bTrade=False):
	finalTm = ''
	pos = 0
	preLine = ''
	headLine = ''
	line = f.readline()
	#print "GetRtProp", verObj, bTrade
	while line:
		objs = re.match("TIME: (.*)", line)
		if objs is not None:
			pos = f.tell()
			finalTm = objs.group(1)[-5:]
			dt = datetime.datetime.strptime(objs.group(1), "%Y-%m-%d %H:%M")
			#print "Matched", finalTm, dt
			headLine = preLine
			if dt.hour>=15:
				#print "Find matched line", line
				dtObj.append(dt)
				if verObj is not None:
					val = headLine[5:7]
					if val=="##":
						verObj.append('V1')
					else:
						verObj.append(val)
				return 0
		preLine = line
		line = f.readline()

	if bTrade:
		#print "current day ", finalTm, pos
		val = headLine[5:7]
		if verObj is not None:
			val = headLine[5:7]
			if val=="##":
				verObj.append('V1')
			else:
				verObj.append(val)
		f.seek(pos)
		dtObj.append(dt)
		return 0
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
	
def parse_summary_info(f, stcsItem, rt_ver='V1'):
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

	#print("parse_summary_info", line, rt_ver)
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
		elif line[:6]=="Check ":
			pass
		else:
			print("Error: Get ZT DT fail", line)
			return -1
		line = f.readline()
	stcsItem.s_st_yzzt = int(objs.group(1))
	stcsItem.s_st_yzdt = int(objs.group(2))
	
	com_str = objs.group(3)
	#print "l_sum", com_str
	if rt_ver=='V1':
		objs = com_str.split(',')
		#print(len(objs), objs[0])
	elif rt_ver=='V2':
		part2Obj = com_str.split('===')
		objs = part2Obj[0].split(',')
	for i in range(0, len(objs)):
		items = re.match('[\t ]+(\d+)[\t ]+(.*)', objs[i])
		#print(i, objs[i], items.groups())
		value = int(items.group(1))
		tname = items.group(2)
		#print "ggget", value, tname
		if tname[:4]=='DTKP':
			stcsItem.s_open_dt = value
		elif tname[:4]=='YZDT':
			stcsItem.s_yzdt = value
		elif tname[:4]=='DTDK':
			stcsItem.s_open_dt_dk = value
		elif tname[:4]=='DaoT':
			stcsItem.s_dt_daoT = value
		else:
			print("Warning: ======== unknown", items.groups());
	if rt_ver=='V2':
		for i in range(0, len(objs)):
			items = re.match('[\t ]+(\d+)[\t ]+(.*)', objs[i])
			#print(i, objs[i], items.groups())
			value = int(items.group(1))
			tname = items.group(2)
			#print "ggget", value, tname
			if tname[:4]=='DTKP':
				stcsItem.s_large_open_dt = value
			elif tname[:4]=='YZDT':
				stcsItem.s_large_yzdt = value
			elif tname[:4]=='DTDK':
				stcsItem.s_large_open_dt_dk = value
			elif tname[:4]=='DaoT':
				stcsItem.s_large_dt_daoT = value
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
		if objs is None:
			cond = "\((\d+)\+(\d+)\)[\t ]+\[(\d+) (\d+) (\d+) (\d+)\][\t ]+(\d+) 上,[\t ]*(\d+) 下"
			objs = re.match(cond, line)
			#print('BB', line, objs)
		if objs is None:
			print "Error: parse fail2", line.decode('utf8').encode('gbk')
			return -1
		stcsItem.s_cx_yz = int(objs.group(1))
		stcsItem.s_non_cx_yz = int(objs.group(2))
		stcsItem.s_open_zt = int(objs.group(3))
		stcsItem.s_close_zt = int(objs.group(4))
		stcsItem.s_open_T_zt = int(objs.group(5))
		stcsItem.s_dk_zt = int(objs.group(6))
		stcsItem.s_sw_zt = int(objs.group(7))
		stcsItem.s_xw_zt = int(objs.group(8))
		#print stcsItem.s_cx_yz,stcsItem.s_non_cx_yz,stcsItem.s_open_zt,stcsItem.s_close_zt
		break

	if rt_ver=="V2":
		line = f.readline()
		while line:
			objs = re.match(".*(\d+)\-ZT[\t ]+(\d+)\-DT[\t ]+(\d+)--(.*)", line)
			#print(line, objs)
			if objs is None:
				print("Error: parse fail1", line)
				return -1
			stcsItem.s_large_zt = int(objs.group(1))
			stcsItem.s_large_dt = int(objs.group(2))
			stcsItem.s_large_yzzt = int(objs.group(3))
			
			line = objs.group(4).strip()
			cond = "\[(\d+) (\d+) (\d+) (\d+)\][\t ]+(\d+) 上,[\t ]*(\d+) 下"
			objs = re.match(cond.decode('utf8').encode('gbk'), line)
			#if objs is None:
			#	cond = "\((\d+)\+(\d+)\)[\t ]+\[(\d+) (\d+) (\d+) (\d+)\][\t ]+(\d+) 上,[\t ]*(\d+) 下"
			#	objs = re.match(cond, line)
			#	#print('BB', line, objs)
			if objs is None:
				print "Error: parse fail2", line.decode('utf8').encode('gbk')
				return -1
			stcsItem.s_large_open_zt = int(objs.group(1))
			stcsItem.s_large_close_zt = int(objs.group(2))
			stcsItem.s_large_open_T_zt = int(objs.group(3))
			stcsItem.s_large_dk_zt = int(objs.group(4))
			stcsItem.s_large_sw_zt = int(objs.group(5))
			stcsItem.s_large_xw_zt = int(objs.group(6))
			break
	
	line = f.readline()
	while line:
		cond = ".*(\d+)\-CG\((\d+)\)[\t ]+(\d+)\-FT\((\d+)\)[\t ]+(\d+)\-YIN  KD:\[(.*)\]"
		objs = re.match(cond, line)
		#print(line, objs)
		if objs is None:
			print("Error: parse fail3", line)
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

	if rt_ver=="V2":
		line = f.readline()
		while line:
			cond = ".*(\d+)\-CG\((\d+)\)[\t ]+(\d+)\-FT\((\d+)\)[\t ]+(\d+)\-YIN  KD:\[(.*)\]"
			objs = re.match(cond, line)
			#print(line, objs)
			if objs is None:
				print("Error: parse fail3", line)
				return -1
			break

	line = f.readline()
	while line:
		#cond = "[ ]+(\d+)\([ ]+(\d+)\)[\t ]+ZERO:[\t ]+(\d+)[\t ]+(\d+)[\t ]+\([\t ]+(\d+)\)"
		cond  = "[ ]*(\d+)\([ ]*(\d+)\)[\t ]*ZERO:[\t ]*(\d+)[\t ]*(\d+)[\t ]*\([\t ]*(\d+)\)"
		objs = re.match(cond, line)
		#line=line.strip();
		#print(line, objs)
		if objs is None:
			print("Error: parse fail4", line)
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
			print("Error: parse fail5", line)
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
			print("Error: parse fail6", line)
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
def parse_cixin_item(f, stcsItem, rt_ver='V1'):
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

def parse_total_line(fl, line, stcsItem):
	#tol_str = "Total( %d = %d + %d	YZ: %d=%d(%d)+%d   %d CXZT,%d CXDT ):"
	#tol_str%( stcsItem.s_zt, stcsItem.s_zt-non_cx, non_cx, stcsItem.s_yzzt, cx_yz, stcsItem.s_cx_yzzt, non_cx_yz, stcsItem.s_cxzt, stcsItem.s_cxdt)
	cond = "Total\( (\d+) = (\d+) \+ (\d+)	YZ: (\d+)=(\d+)\((\d+)\)\+(\d+)   (\d+) CXZT,(\d+) CXDT \):"
	objs = re.match(cond, line)
	if objs is None:
		print("Error, Total line", line)
		return -1
	#print("parse22_total_line", line)
	stcsItem.s_zt = int(objs.group(1))
	#已经保存该值，注册制下CX没有YZZT
	#print("parse_total1_line",stcsItem.s_yzzt,objs.group(2),objs.group(4))
	if stcsItem.s_yzzt!=int(objs.group(2)):
		#print("Error: CX_YZ1",stcsItem.s_yzzt,objs.group(2),fl.name)
		pass
	#stcsItem.s_non_cx_zt = int(objs.group(3))
	if stcsItem.s_yzzt!=int(objs.group(4)):
		print("Error: CX_YZ2",stcsItem.s_yzzt,objs.group(4),fl.name)
	#stcsItem.s_yzzt = int(objs.group(4))
	if stcsItem.s_cx_yz!=int(objs.group(5)):
		print("Error: CX_YZ3",stcsItem.s_cx_yz,objs.group(5),fl.name)
	#stcsItem.s_cx_yz = int(objs.group(5))
	stcsItem.s_cx_yzzt = int(objs.group(6))
	#stcsItem.non_cx_yz = int(objs.group(7))
	stcsItem.s_cxzt = int(objs.group(8))
	stcsItem.s_cxdt = int(objs.group(9))
	return 0

def parse_zhenfu_item(f, stcsItem, rt_ver='V1'):
	ret = 0
	#cond = "ZFD: \((\d+)\+[\d]+\+[\d]),([\d]+\+[\d]+),([\d]+\+[\d]+)"
	cond = "ZFD: \((\d+)\=(\d+)\+(\d+)\+(\d+)\),\((\d+)\+(\d+)\),\((\d+)\+(\d+)\)"
	line = f.readline()
	while line:
		if len(line)<3:
			line = f.readline()
			continue
		if line[:3]!="ZFD":
			return (1,line)
		#包含ZFD的项目
		line = line.strip()
		objs = re.match(cond, line)
		stcsItem.s_zhenfu = objs.group(2)
		stcsItem.s_large_zhenfu = objs.group(2)
		stcsItem.s_large_5day_cx = objs.group(3)
		stcsItem.s_zhenfu_zt = objs.group(5)
		stcsItem.s_zhenfu_dt = objs.group(6)
		stcsItem.s_large_zhenfu_zt = objs.group(7)
		stcsItem.s_large_zhenfu_dt = objs.group(8)
		line = f.readline()
		break
	return (0,'')

def parse_nb_jc_item(f, stcsItem, rt_ver='V1', firstLn=''):
	ret = 0
	if firstLn=='':
		line = f.readline()
	else:
		line = firstLn
	while line:
		if line=="NB:\n":
			line = f.readline()
			#break
		elif line=="JC:\n":
			line = f.readline()
			pass
		elif line[:5]=="Total":
			#print("parse_nb_jc1_item",line)
			#print("line is EMPTY")
			ret = parse_total_line(f, line, stcsItem)
			break
		elif len(line)>10 and line[:5]=="#####":
			print("Error: Read next block")
			return -1
		else:
			print("Error: NB_JC line", line)
			return -1
		line = f.readline()
	return ret

#解析history realtm文件中指定每一行数据
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
		elif zdt_type==11:
			cond = head + lprice + "(\d+) (.*)"
			stkList = stcsItem.lst_large_non_yzcx_yzzt
		elif zdt_type==12:
			cond = head + lprice + "(\d+) (.*)"
			stkList = stcsItem.lst_large_non_yzcx_zt
		elif zdt_type==13:
			cond = head + lprice + "(\d+) (.*)"
			stkList = stcsItem.lst_large_non_yzcx_zthl
		elif zdt_type==14:
			cond = head + lprice + "(\d+) (.*)"
			stkList = stcsItem.lst_large_yzdt
		elif zdt_type==15:
			cond = head + lprice + "(\d+) (.*)"
			stkList = stcsItem.lst_large_dt
		elif zdt_type==16:
			cond = head + lprice + "(\d+) (.*)"
			stkList = stcsItem.lst_large_dtft
		else:
			line = f.readline()
			continue
		#line = line.strip()
		objs = re.match(cond, line)
		#print "rtlne:",line
		if objs is None:
			print(objs, line, cond)
			return -1
		code = objs.group(2)[:6]
		name = objs.group(2)[7:].replace(" ", "").replace("\t","").strip()
		change_percent = float(objs.group(3))
		price = float(objs.group(4))
		open_percent = float(objs.group(5))
		high_zf_percent = float(objs.group(6))
		low_df_percent = float(objs.group(7))
		count = int(objs.group(8))
		desc = objs.group(9)
		#print ("here-'%s','%s'"%(count,desc))
		item = [code, name, change_percent, price, open_percent, high_zf_percent, low_df_percent, count, desc]
		stkList.append(item)
		#print "zdt anly", zdt_type, code,name,count
		#if zdt_type==12:
		#	print "zdt anly", code,name,count
		line = f.readline()
	return 0

#解析ZT(YZZT ZT ZTHL), DT(YZDT DT DTFT) 6种ZDT数据
def parse_zt_dt_stcs(f, stcsItem, rt_ver='V1'):
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
		elif line[:8]=="CZL_YZZT":
			parse_zdt_item(f, stcsItem, 11)
			pass
		elif line[:8]=="CZL_ZT  ":
			parse_zdt_item(f, stcsItem, 12)
			pass
		elif line[:8]=="CZL_ZTHL":
			parse_zdt_item(f, stcsItem, 13)
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
		elif line[:7]=="CZL_YZD":
			parse_zdt_item(f, stcsItem, 14)
			pass
		elif line[:7]=="CZL_DT ":
			parse_zdt_item(f, stcsItem, 15)
			pass
		elif line[:7]=="CZL_DTF":
			parse_zdt_item(f, stcsItem, 16)
			pass
		elif line=="\n":
			break
		else:
			#print("Error: DT issue", line)
			break
		line = f.readline()
	return 0

#解析history 生成的realtm文件
def parse_realtime_his_file(trade_day, stcsItem, bTrade=False):
	#print "ps rt", trade_day, bTrade
	filename = get_path_by_tdate(trade_day)
	if filename=='':
		return -1

	if not os.path.isfile(filename):
		print("Error: not find ",filename)
		return -1
	
	#print("realtime file", filename)
	f = open(filename, 'r')

	dtObj = []
	verObj = []
	ret = get_rt_props(f, dtObj, verObj, bTrade)
	if ret==-1:
		print ("Not find matched rt time, Re-get latest realtime")
		return -1
	#print(len(dtObj), dtObj)
	
	ret = match_rt_date(f)
	stcsItem.s_date = trade_day

	ret = parse_summary_info(f, stcsItem, verObj[0])
	if ret==-1:
		return ret

	ret = parse_cixin_item(f, stcsItem, verObj[0])
	if ret==-1:
		return ret

	#以前版本没有ZFD，告诉以前版本刚开始是否读取第一行
	ret,firstLn = parse_zhenfu_item(f, stcsItem, verObj[0])
	if ret==-1:
		return ret

	ret = parse_nb_jc_item(f, stcsItem, verObj[0], firstLn)
	if ret==-1:
		return ret

	ret = parse_zt_dt_stcs(f, stcsItem, verObj[0])
	if ret==-1:
		return ret

	#再继续读取，理论上还有最后一次按照时间排序的数据
	#两者后面时间将进行对比
	#此时，最后参数强行设置为False
	ret = get_rt_props(f, dtObj, None, False)
	#print(len(dtObj), dtObj)

	f.close()

	if bTrade==True:
		curTm = datetime.datetime.now()
		if curTm.hour<15:
			return 0
	
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
		if (dtObj[1]-dtObj[0]).seconds<0:
			print("Warning: time issue", filename)
	return 0

def get_path_by_tdate(pre_day):
	filename = REALTM_PRE_FD + 'entry/realtime/' + 'rt_' + pre_day + '.txt'
	if os.path.isfile(filename):
		return filename
	syear = pre_day[:4]
	filename = REALTM_PRE_FD + 'entry/realtime/' + syear + '/rt_' + pre_day + '.txt'
	if os.path.isfile(filename):
		return filename
	print("Warning: not find file",pre_day)
	return ''

#Main
if __name__=='__main__':
	trade_date = get_lastday()
	pre_date = get_preday(1, trade_date)	
	preStatItem = statisticsItem()
	ret = parse_realtime_his_file(trade_date, preStatItem)

	pList = preStatItem.lst_non_yzcx_yzzt
	for obj in pList:
		print obj[0],obj[1],obj[7]
	print ''
	pList = preStatItem.lst_non_yzcx_zt
	for obj in pList:
		print obj[0],obj[1],obj[7]
	print ''
	pList = preStatItem.lst_large_non_yzcx_yzzt
	for obj in pList:
		print obj[0],obj[1],obj[7]
	print ''
	pList = preStatItem.lst_large_non_yzcx_zt
	for obj in pList:
		print obj[0],obj[1],obj[7]
	print ''
	
	pass
