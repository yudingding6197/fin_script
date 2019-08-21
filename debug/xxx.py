#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import json
import zlib
import random
import getopt
import datetime
sys.path.append(".")
from internal.common import *
import matplotlib.pyplot as plt
import numpy as np

#对数据解析
def read_content(tp, qdate, content, trade_dt, syl):
	fd = ''
	index = 0
	if tp=='h0':
		print("Not implement:", tp)
		return
	elif tp=='s0':
		fd = '0total'
	elif tp=='s1':
		fd = '1zhb'
		index = 1
	elif tp=='s2':
		fd = '2zxb'
		index = 2
	elif tp=='s3':
		fd = '3cyb'
		index = 3
	else:
		print("Unknow:", tp)
		return

	filename = '../data/entry/index/sz/'+fd+'/sz_'+fd+'_'+qdate+'.txt'
	if os.path.exists(filename) is False:
		#print(qdate, "No file")
		return

	with open(filename, 'r') as f:
		object = json.load(f)

		trade_dt.append(qdate)
		
		value = object[9]["today"]
		syl.append(float(value))
	return

#Main
#for i in range(0,1000):
#	formatRand()

param_config = {
	"Start":'',		#开始时间
	"End":'',		#结束时间
	"Type":'',		#获取的板块，总体,Main,ZX,CY
	"Force":0,		#是否强制刷新
}

optlist, args = getopt.getopt(sys.argv[1:], 's:e:t:f:')
for option, value in optlist:
	if option in ["-s","--start"]:
		param_config["Start"] = value
	elif option in ["-e","--end"]:
		param_config["End"] = value
	elif option in ["-t","--type"]:
		param_config["Type"] = value
	elif option in ["-f","--force"]:
		param_config["Force"] = int(value)

today = datetime.date.today()
str_end = ''
if param_config["End"]=='':
	str_end = '%04d-%02d-%02d' %(today.year, today.month, today.day)
else:
	ret,str_end = parseDate(param_config["End"], today)
	if ret==-1:
		exit(1)
ed_date = datetime.date(*map(int, str_end.split('-')))

str_start = ''
if param_config["Start"]=='':
	str_start = '%04d-%02d-%02d' %(today.year, today.month, today.day)
else:
	ret,str_start = parseDate(param_config["Start"], today)
	if ret==-1:
		exit(1)
st_date = datetime.date(*map(int, str_start.split('-')))

tp = param_config["Type"]
if tp=='':
	tp = 's3'

cur_date = st_date
syl = []
trade_dt = []
while (ed_date - cur_date).days>=0:
	#print(cur_date)
	content = []
	qdate = '%04d-%02d-%02d' %(cur_date.year, cur_date.month, cur_date.day)
	read_content(tp, qdate, content, trade_dt, syl)

	delta1=datetime.timedelta(days=1)
	cur_date = cur_date + delta1

if len(syl)==0:
	print("Fail to get any content", st_date, ed_date)
	exit(0)


# 创建一个点数为 8 x 6 的窗口, 并设置分辨率为 80像素/每英寸
plt.figure(figsize=(8, 6), dpi=80)

# 再创建一个规格为 1 x 1 的子图
plt.subplot(1, 1, 1)

# 柱子总数
N = len(syl)
# 包含每个柱子对应值的序列
#values = (25, 32, 34, 20, 41, 50)

# 包含每个柱子下标的序列
index = np.arange(N)

# 柱子的宽度
width = 0.2

# 绘制柱状图, 每根柱子的颜色为紫罗兰色
p2 = plt.bar(index, syl, width, label="rainfall", color="#87CEFA")

# 设置横轴标签
plt.xlabel('Months')
# 设置纵轴标签
plt.ylabel('rainfall (mm)')

# 添加标题
plt.title('Monthly average rainfall')

# 添加纵横轴的刻度
#plt.xticks(index, ('Jan', 'Fub', 'Mar', 'Apr', 'May', 'Jun'))
plt.yticks(np.arange(0, 200, 10))

# 添加图例
plt.legend(loc="upper right")

plt.show()