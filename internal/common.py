# -*- coding:gbk -*-
import sys
import re
import os
import string
import datetime
import urllib
import urllib2
from openpyxl import Workbook
from openpyxl.reader.excel  import  load_workbook

#url = "http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php?symbol=sz300001&date=2015-09-10&page=48"
#成交时间	成交价	涨跌幅	价格变动	成交量(手)		成交额(元)	性质
#	<tr ><th>11:29:48</th><td>14.57</td><td>-3.06%</td><td>+0.01</td><td>16</td><td>23,312</td><th><h1>中性盘</h1></th></tr>
#<tr ><th>11:29:36</th><td>14.56</td><td>-3.13%</td><td>--</td><td>9</td><td>13,104</td><th><h6>卖盘</h6></th></tr>
#<tr ><th>11:29:21</th><td>14.56</td><td>-3.13%</td><td>-0.02</td><td>10</td><td>14,560</td><th><h6>卖盘</h6></th></tr>

class fitItem:
	volumn = 0
	buyvol = 0
	buyct = 0
	buyavg = 0
	sellvol = 0
	sellct = 0
	sellavg = 0
	def __init__(self, vol):
		self.volumn = vol
		self.buyvol = 0
		self.buyct = 0
		self.buyavg = 0
		self.sellvol = 0
		self.sellct = 0
		self.sellavg = 0
		

def handle_data(addcsv, prepath, url, code, qdate, sarr):
	url = url + "?symbol=" +code+ "&date=" +qdate
	if not os.path.isdir(prepath):
		os.makedirs(prepath)

	dataObj = []
	if cmp(sarr, '')==0:
		sarr = "0,300,600,900"
	volObj = sarr.split(',')
	arrlen = len(volObj)
	for i in range(0,arrlen):
		obj = fitItem(int(volObj[i]))
		dataObj.append(obj)
	dataObjLen = len(dataObj)

	wb = Workbook()
	# grab the active worksheet
	ws = wb.active

	totalline = 0
	#可能数据在不同的页面，同时存在，这是重复数据需要过滤重复结果
	#还可能相同时间，产生多个成交量，需要都保留
	lasttime = ''
	lastvol = 0
	filename = code+ '_' + qdate
	if addcsv==1:
		filecsv = prepath + filename + '.csv'
		fcsv = open(filecsv, 'w')
		strline = '成交时间,成交价,涨跌幅,价格变动,成交量,成交额,性质'
		fcsv.write(strline)
		fcsv.write("\n")

	strline = u'成交时间,成交价,涨跌幅,价格变动,成交量,成交额,性质'
	strObj = strline.split(u',')
	ws.append(strObj)
	for i in range(1,1000):
		urlall = url + "&page=" +str(i)
		#print "%d, %s" %(i,urlall)
		
		req = urllib2.Request(urlall)
		res_data = urllib2.urlopen(req)

		flag = 0
		count = 0
		line = res_data.readline()
		checkStr = '成交时间'
		while line:
			#print line
			index = line.find(checkStr)
			if (index<0):
				line = res_data.readline()
				continue

			if flag==0:
				checkStr = '<th>'
				flag = 1
			else:
				key = re.match(r'\D+(\d{2}:\d{2}:\d{2})\D+(\d+.\d{1,2})</td><td>(\+?-?\d+.\d+%)\D+(--|\+\d+.\d+|-\d+.\d+)\D+(\d+)</td><td>([\d,]+)</td><th><h\d+>(卖盘|买盘|中性盘)\D', line)
				if (key):
					#print key.groups()
					curtime = key.group(1)
					curvol = int(key.group(5))
					timeobj = re.search(curtime, lasttime)
					if (timeobj and curvol==lastvol):
						pass
					else:
						lasttime = curtime
						lastvol = curvol
						amount = key.group(6)
						obj = amount.split(',')
						amount = ''.join(obj)
						
						intamount = int(key.group(5))
						state = key.group(7)
						for j in range(0, dataObjLen):
							filvol = int(dataObj[j].volumn)
							if intamount<filvol:
								continue;
							if cmp(state, '卖盘')==0:
								dataObj[j].sellvol += intamount
								dataObj[j].sellct += 1
								#print "S:%d %d" %(dataObj[j].sellvol, dataObj[j].sellct)
							elif cmp(state, '买盘')==0:
								dataObj[j].buyvol += intamount
								dataObj[j].buyct += 1
								#print "B:%d %d" %(dataObj[j].buyvol, dataObj[j].buyct)

						if addcsv==1:
							strline = curtime +","+ key.group(2) +","+ key.group(3) +","+ key.group(4) +","+ key.group(5) +","+ amount +","+ key.group(7) + "\n"
							fcsv.write(strline)

						totalline += 1
						row = totalline+1
						cell = 'A' + str(row)
						ws[cell] = curtime
						cell = 'B' + str(row)
						ws[cell] = key.group(2)
						cell = 'C' + str(row)
						ws[cell] = key.group(3)
						cell = 'D' + str(row)
						ws[cell] = key.group(4)
						cell = 'E' + str(row)
						ws[cell] = int(key.group(5))
						cell = 'F' + str(row)
						ws[cell] = int(amount)
						cell = 'G' + str(row)
						s1 = key.group(7).decode('gbk')
						ws[cell] = s1
					count += 1
				else:
					endObj = re.search(r'</td><td>', qdate)
					if (endObj):
						print "Error line:" + line
					else:
						break;
			line = res_data.readline()

		if (count==0):
			break;

	if addcsv==1:
		fcsv.close()
		if (totalline==0):
			os.remove(filecsv)

	if (totalline>0):
		ws = wb.create_sheet()
		ws.title = 'statistics'

		row = 1
		cell = 'B' + str(row)
		ws[cell] = 'B'
		cell = 'C' + str(row)
		ws[cell] = 'B_vol'
		cell = 'D' + str(row)
		ws[cell] = 'B_avg'
		cell = 'E' + str(row)
		ws[cell] = 'S'
		cell = 'F' + str(row)
		ws[cell] = 'S_vol'
		cell = 'G' + str(row)
		ws[cell] = 'S_avg'

		for j in range(0, dataObjLen):
			row = row+1
			cell = 'A' + str(row)
			ws[cell] = dataObj[j].volumn

			buyvol = dataObj[j].buyvol
			buyct = dataObj[j].buyct
			cell = 'B' + str(row)
			ws[cell] = buyvol
			cell = 'C' + str(row)
			ws[cell] = buyct
			cell = 'D' + str(row)
			if buyct==0:
				ws[cell] = 0
			else:
				ws[cell] = buyvol/buyct

			sellvol = dataObj[j].sellvol
			sellct = dataObj[j].sellct
			cell = 'E' + str(row)
			ws[cell] = sellvol
			cell = 'F' + str(row)
			ws[cell] = sellct
			cell = 'G' + str(row)
			if sellct==0:
				ws[cell] = 0
			else:
				ws[cell] = sellvol/sellct

			cell = 'I' + str(row)
			ws[cell] = buyvol + sellvol
			cell = 'J' + str(row)
			ws[cell] = buyct + sellct

	filexlsx = prepath +filename+ '.xlsx'
	wb.save(filexlsx)
	if (totalline==0):
		print "No Matched Record"
		os.remove(filexlsx)


