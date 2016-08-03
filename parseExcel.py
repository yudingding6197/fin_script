# -*- coding:gbk -*-
import sys
import re
import os
import string
import datetime
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook
from internal.common import *

prepath = '../Data/'
sheetName = "statistics"
allFileNum = 0
volumnList = [200, 300, 600, 900]
volumnList1 = [0,200, 300, 600, 900]

def printPath(level, path,fileList):
	global allFileNum
	# 所有文件夹，第一个字段是次目录的级别
	dirList = []
	# 所有文件
	#fileList = []
	# 返回一个列表，其中包含在目录条目的名称(google翻译)
	files = os.listdir(path)
	# 先添加目录级别
	dirList.append(str(level))
	for f in files:
		if(os.path.isdir(path + '/' + f)):
			# 排除隐藏文件夹。因为隐藏文件夹过多
			if(f[0] == '.'):
				pass
			else:
				# 添加非隐藏文件夹
				dirList.append(f)
		if(os.path.isfile(path + '/' + f)):
			# 添加文件
			fileList.append(f)
	# 当一个标志使用，文件夹列表第一个级别不打印
	''' 目前不需要子文件夹
	i_dl = 0
	for dl in dirList:
		if(i_dl == 0):
			i_dl = i_dl + 1
		else:
			# 打印至控制台，不是第一个的目录
			print '-' * (int(dirList[0])), dl
			# 打印目录下的所有文件夹和文件，目录级别+1
			printPath((int(dirList[0]) + 1), path + '/' + dl)
	for fl in fileList:
		# 打印文件
		#print '-' * (int(dirList[0])), fl
		# 随便计算一下有多少个文件
		allFileNum = allFileNum + 1
		file = os.open(fl, "r")
	'''
	
	'''
	printPath(1, path, fileList)
	for fl in fileList:
		wkfile = path +"//"+ fl
		wb = load_workbook(wkfile)
		print "Worksheet range(s):", wb.get_named_ranges()
		print "Worksheet name(s):", wb.get_sheet_names()
		if sheetName not in wb.get_sheet_names():
			print "NONNN"
			continue

		sheet_ranges_r = wb.get_sheet_by_name(name=sheetName)
		print "YYYY:"
		print sheet_ranges_r
	'''	

# 建立存储数据的字典 
data_dic = []
bCheckDate = 0

def parseFile(path, filename):
	wkfile = path +"/"+ filename
	#print wkfile

	wb = load_workbook(wkfile)
	#print "Worksheet range(s):", wb.get_named_ranges()
	#print "Worksheet name(s):", wb.get_sheet_names()
	if sheetName not in wb.get_sheet_names():
		return

	ws = wb.get_sheet_by_name(name=sheetName)
	max_column = ws.max_column
	if max_column<7:
		print "column(%d) too short, please check" % max_column
		return

	#把数据存到字典中
	pid = ''
	data_list = []
	for rx in range(1,ws.max_row):
		w1 = ws.cell(row = rx, column = 1).value
		w2 = ws.cell(row = rx, column = 2).value
		w3 = ws.cell(row = rx, column = 3).value
		w4 = ws.cell(row = rx, column = 4).value
		w5 = ws.cell(row = rx, column = 5).value
		w6 = ws.cell(row = rx, column = 6).value
		w7 = ws.cell(row = rx, column = 7).value
		w8 = ws.cell(row = rx, column = 8).value
		w9 = ws.cell(row = rx, column = 9).value
		
		if (w1 is None) and (w2 is None) and (w3 is None) and (w4 is None)\
			and (w5 is None) and (w6 is None) and (w7 is None):
			break
		if (w1 is None) or (w2 is None) or (w3 is None) or (w4 is None)\
			or (w5 is None) or (w6 is None) or (w7 is None):
			print rx,"某项记录为None，不正确", w1, w2, w3, w4, w5, w6, w7 
			continue
		temp_list = [w1,w2,w3,w4,w5,w6,w7,w8,w9]
		if rx==1:
			pid = w1
		else:
			#print temp_list
			data_list.append(temp_list)

	if cmp(pid, '')!=0:
		day_list = [pid, data_list]
		data_dic.append(day_list)

def statVolume(path, filename):
	wkfile = path +"/"+ filename

	dataObjLen = len(data_dic)
	if dataObjLen==0:
		print "没有数据"
		return
	
	wb = Workbook()
	ws = wb.active
	ws.title = sheetName
	
	row = 1
	ascid = 65
	title = []
	title.append('')
	for fltvol in volumnList1:
		bs = 'B%d'%(fltvol)
		title.append(bs)
		bs = 'S%d'%(fltvol)
		title.append(bs)

		number = len(title)
		for i in range(0,number):
			cell = chr(ascid+i) + str(row)
			ws[cell] = title[i]

	row = 2
	buy = [0,0,0,0,0]
	sell = [0,0,0,0,0]
	index = dataObjLen-1
	while index>=0:
		day_list = data_dic[index]
		index -= 1

		cell = chr(ascid) + str(row)
		ws[cell] = day_list[0]

		i = 1
		j = 0
		for data_list in day_list[1]:
			#print data_list,day_list[0], data_list[0]
			
			buy[j] = buy[j] + data_list[1]
			cell = chr(ascid+i) + str(row)
			ws[cell] = data_list[1]
			i += 1

			sell[j] = sell[j] + data_list[3]
			cell = chr(ascid+i) + str(row)
			ws[cell] = data_list[3]
			i += 1

			j += 1
		row += 1

	cell = chr(ascid) + str(row)
	ws[cell] = "Total"
	number = len(buy)
	#统计买卖成交量总和
	for i in range(0, number):
		cell = chr(ascid+1+i*2) + str(row)
		ws[cell] = buy[i]
		cell = chr(ascid+1+i*2+1) + str(row)
		ws[cell] = sell[i]
	row += 1

	#获取买卖成交量占比对应的买卖总量
	totalBVol = buy[0]
	totalSVol = sell[0]
	for i in range(0, number):
		cell = chr(ascid+1+i*2) + str(row)
		if i==0:
			continue;
			buyPerc = round(float(totalBVol) * 100 / (totalBVol+totalSVol), 2)
		else:
			buyPerc = round(float(buy[i]) * 100 / totalBVol, 2)
		ws[cell] = buyPerc

		cell = chr(ascid+1+i*2+1) + str(row)
		if i==0:
			continue;
			sellPerc = round(float(totalSVol) * 100 / (totalBVol+totalSVol), 2)
		else:
			sellPerc = round(float(sell[i]) * 100 / totalSVol, 2)
		ws[cell] = sellPerc
	row += 1

	#获取买卖成交量占比总买卖总量
	totoalVol = totalBVol+totalSVol
	for i in range(0, number):
		cell = chr(ascid+1+i*2) + str(row)
		if i==0:
			buyPerc = round(float(totalBVol) * 100 / totoalVol, 2)
		else:
			buyPerc = round(float(buy[i]) * 100 / totoalVol, 2)
		ws[cell] = buyPerc

		cell = chr(ascid+1+i*2+1) + str(row)
		if i==0:
			sellPerc = round(float(totalSVol) * 100 / totoalVol, 2)
		else:
			sellPerc = round(float(sell[i]) * 100 / totoalVol, 2)
		ws[cell] = sellPerc
	row += 1

	wb.save(wkfile)

def statByVolume(path, filename):
	wkfile = path +"/"+ filename

	dataObjLen = len(data_dic)
	if dataObjLen==0:
		print "没有数据"
		return
	
	wb = Workbook()
	ws = wb.active
	ws.title = sheetName
	
	ascid = 65
	row = 1
	for fltvol in volumnList:
		title = [fltvol, 'B', 'S', 'B_vol', 'S_vol', 'B_avg', 'S_avg']
		number = len(title)
		for i in range(0,number):
			cell = chr(ascid+i) + str(row)
			ws[cell] = title[i]
		row += 1

		index = dataObjLen-1
		while index>=0:
			day_list = data_dic[index]
			index -= 1
			for data_list in day_list[1]:
				if data_list[0]!=fltvol:
					continue

				number = len(data_list)
				for i in range(0,number):
					cell = chr(ascid+i) + str(row)
					if i==0:
						ws[cell] = day_list[0]
					else:
						ws[cell] = data_list[i]
				row += 1
		#写完相同数据然后空一行
		row += 1
	wb.save(wkfile)

	
if __name__ == '__main__':
	pindex = len(sys.argv)
	if pindex==2 or pindex==4:
		pass
	else:
		sys.stderr.write("Usage: " +os.path.basename(sys.argv[0])+ " 代码 [开始时间<YYYYMMDD or MMDD>] [结束时间<YYYYMMDD or MMDD>]\n")
		exit(1);

	code = sys.argv[1]
	if (len(code) != 6):
		sys.stderr.write("Len should be 6\n")
		exit(1);

	head3 = code[0:3]
	result = (cmp(head3, "000")==0) or (cmp(head3, "002")==0) or (cmp(head3, "300")==0)
	if result is True:
		code = "sz" + code
	else:
		result = (cmp(head3, "600")==0) or (cmp(head3, "601")==0) or (cmp(head3, "603")==0)
		if result is True:
			code = "sh" + code
		else:
			print "非法代码:" +code+ "\n"
			exit(1);

	bCheckDate = 0
	styear = 0
	stmonth = 0
	stday = 0
	edyear = 0
	edmonth = 0
	edday = 0
	today = datetime.date.today()
	if pindex==4:
		ret,styear,stmonth,stday= parseSeparateDate(sys.argv[2], today)
		if ret==-1:
			exit(1)

		eddate = sys.argv[3]
		if cmp(eddate, '.')==0:
			edyear = today.year
			edmonth = today.month
			edday = today.day
		else:
			ret,edyear,edmonth,edday = parseSeparateDate(eddate, today)
			if ret==-1:
				exit(1)

		bCheckDate = 1
		print styear, stmonth, stday
		print edyear, edmonth, edday

	fileList = []
	path = prepath + code
	if not os.path.isdir(path):
		print "'"+ path +"' not a dir"
		exit(1)

	for (dirpath, dirnames, filenames) in os.walk(path):  
		#print('dirpath = ' + dirpath)
		i = 0
		for filename in filenames:
			extname = filename.split('.')[-1]
			if cmp(extname,"xlsx")!=0:
				continue
			prename = code+"_"
			if cmp(filename[0:9], prename[0:9])!=0:
				continue
			if bCheckDate==1:
				fileDate = filename[9:(len(filename)-5)]
				if len(fileDate)!=10:
					continue

				fileDateN = fileDate[0:4] + fileDate[5:7] + fileDate[8:10]
				ret,curyear,curmonth,curday = parseSeparateDate(fileDateN, today)
				if ret==-1:
					continue
				if ((curyear<styear or curyear>edyear) or (curmonth<stmonth or curmonth>edmonth)\
					or (curday<stday or curday>edday)) :
					continue

			print filename
			parseFile(path, filename)
			i += 1
			
		#仅仅得到父文件夹的文件，忽略子文件夹下文件
		break

	if cmp('meg', '')!=0:
		cur=datetime.datetime.now()
		fctime = '%04d%02d%02d_%02d%02d' %(cur.year, cur.month, cur.day, cur.hour, cur.minute)
		#stfile = 'z_'+ code +'_result_'+fctime+'.xlsx'
		#statByVolume(path, stfile)
		stfile = 'z_'+ code +'_result1_'+fctime+'.xlsx'
		statVolume(path, stfile)
