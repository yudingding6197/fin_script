# -*- coding:gbk -*-
import sys
import re
import os
import string
import datetime
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook

prepath = '../Data/'
allFileNum = 0
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
		if "statistics" not in wb.get_sheet_names():
			print "NONNN"
			continue

		sheet_ranges_r = wb.get_sheet_by_name(name='statistics')
		print "YYYY:"
		print sheet_ranges_r
	'''	

def parseFile(path, filename):
	wkfile = path +"/"+ filename
	print wkfile

	wb = load_workbook(wkfile)
	print "Worksheet range(s):", wb.get_named_ranges()
	print "Worksheet name(s):", wb.get_sheet_names()
	if "statistics" not in wb.get_sheet_names():
		return

	ws = wb.get_sheet_by_name(name='statistics')
	print   "Work Sheet Titile:" , ws.title
	print   "Work Sheet Rows:" , ws.max_row

	max_column = ws.max_column
	if max_column<7:
		print "column(%d) too short, please check" % max_column
		return

	# 建立存储数据的字典 
	data_dic = {} 

	#把数据存到字典中
	for rx in range(1,ws.max_row):
		print "rx=", rx
		temp_list = []
		pid = ws.cell(row = rx, column = 0).value
		w1 = ws.cell(row = rx, column = 1).value
		w2 = ws.cell(row = rx, column = 2).value
		w3 = ws.cell(row = rx, column = 3).value
		w4 = ws.cell(row = rx, column = 4).value
		w5 = ws.cell(row = rx, column = 5).value
		w6 = ws.cell(row = rx, column = 6).value
		w7 = ws.cell(row = rx, column = 7).value
		temp_list = [w1,w2,w3,w4,w5,w6,w7]
		print temp_list

		data_dic[pid] = temp_list

	#打印字典数据个数
	print 'Total:%d' %len(data_dic)
	
	
	
	

if __name__ == '__main__':
	pindex = len(sys.argv)
	if pindex<2:
		sys.stderr.write("Usage: " +os.path.basename(sys.argv[0])+ " 代码\n")
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
	#print code

	fileList = []
	path = prepath + code
	if not os.path.isdir(path):
		print "'"+ path +"' not a dir"
		exit(1)

	for (dirpath, dirnames, filenames) in os.walk(path):  
		print('dirpath = ' + dirpath)
		for filename in filenames:
			extname = filename.split('.')[-1]
			if cmp(extname,"xlsx")!=0:
				continue

			parseFile(path, filename)
			
		#仅仅得到父文件夹的文件，忽略子文件夹下文件
		break;

		
