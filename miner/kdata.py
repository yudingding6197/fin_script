#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import os
import datetime
import getopt
import shutil
sys.path.append(".")
sys.path.append("..")
from internal.ts_common import *

# open  high  close   low     volume  price_change  p_change    ma5
# ma10   ma20      v_ma5     v_ma10     v_ma20  turnover
#选择文件，拷贝到指定位置
def output_hist(code, histDf, file):
	df = histDf
	fmt = "%s %6s %6s %6s %6s %6s %6s "

	msg = "Show " + code
	file.write(msg+'\n')

	colList=list(df.columns)
	bTurn = 0
	if "turnover" in colList:
		bTurn = 1
	print msg
	count=0
	for index,row in df.iterrows():
		if bTurn==0:
			msg = fmt%(index, row['p_change'], row['close'], row['open'], row['high'], row['low'], '')
		else:
			msg = fmt%(index, row['p_change'], row['close'], row['open'], row['high'], row['low'], row['turnover'])
		if count<10:
			print msg
		elif count>50:
			break
		file.write(msg+'\n')
		count += 1
	return

def get_hist_df(code):
	if len(code)!=6:
		return None
	if not code.isdigit():
		return None

	df = None
	try:
		df = ts.get_hist_data(code)
	except:
		print "Fail to get hist data"
		time.sleep(0.5)
	return df

def get_code_list(codeList):
	fpath = '../data/entry/miner/filter.txt'
	file = open(fpath, 'r')
	line = file.readline()
	while line:
		if len(line)>=6:
			codeList.append(line[:6])
		line = file.readline()
	return

# Main
param_config = {
	"Code":'',	#
	"File":''	#
}
if __name__=="__main__":
	td = ''
	nowToday = datetime.date.today()
	optlist, args = getopt.getopt(sys.argv[1:], '?fc:')
	for option, value in optlist:
		if option in ["-c","--code"]:
			param_config['Code'] = value
		elif option in ["-f","--file"]:
			param_config['File'] = 'F'
		elif option in ["-?","--??"]:
			print "Usage:", os.path.basename(sys.argv[0]), " [-c code] [-f filename]"
			exit()

	if len(sys.argv)<2:
		print "Usage:", os.path.basename(sys.argv[0]), " [-c code] [-f filename]"
		exit()

	codeList = []
	code = param_config['Code']
	if param_config['File']!='':
		print "Get from file"
		get_code_list(codeList)
	elif code!='':
		print "Get code"
		codeList.append(code)

	fpath = '../data/entry/miner/zKDate.txt'
	file = open(fpath, 'w')
	for code in codeList:
		df = get_hist_df(code)
		if df is None:
			continue
		output_hist(code, df, file)
	file.close()

