#!/usr/bin/env python
# -*- coding:gbk -*-
import os
import struct
import datetime

def stock_csv(filepath, name):
	with open(filepath, 'rb') as f:
		file_object_path = '_test_' + name +'.csv'
		file_object = open(file_object_path, 'w+')
		while True:
			stock_date = f.read(4)
			stock_open = f.read(4)
			stock_high = f.read(4)
			stock_low= f.read(4)
			stock_close = f.read(4)
			stock_amount = f.read(4)
			stock_vol = f.read(4)
			stock_reservation = f.read(4)  # date,open,high,low,close,amount,vol,reservation
			if not stock_date:
				break
			# 4字节如20091229
			stock_date = struct.unpack("l", stock_date)
			print "s_d", type(stock_date), stock_date
			
			year=floor(stock_date/10000)
			month=floor((stock_date%10000)/100)
			day=floor(stock_date%10000%100)
			print year, month, day
			#开盘价*100
			stock_open = struct.unpack("l", stock_open) 
			#最高价*100
			stock_high = struct.unpack("l", stock_high)  
			#最低价*100
			stock_low= struct.unpack("l", stock_low) 
			#收盘价*100
			stock_close = struct.unpack("l", stock_close) 
			#成交额
			stock_amount = struct.unpack("f", stock_amount) 
			#成交量
			stock_vol = struct.unpack("l", stock_vol) 
			#保留值
			stock_reservation = struct.unpack("l", stock_reservation) 
			#格式化日期
			date_format = datetime.datetime.strptime(str(stock_date[0]),'%Y%M%d')
			list= date_format.strftime('%Y-%M-%d')+ "," + str(stock_open[0]/100)+","\
						+str(stock_high[0]/100.0) +"," +str(stock_low[0]/100.0)+"," \
						+ str(stock_close[0]/100.0)+"," + str(stock_vol[0])+"\r\n"
			file_object.writelines(list)
			file_object.close()

if __name__=="__main__":
	path = './debug/tdx/lc5/'
  	listfile = os.listdir(path)
	for i in listfile:
		stock_csv(path+i, i[:-4])