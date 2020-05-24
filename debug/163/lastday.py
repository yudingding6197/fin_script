#!/usr/bin/env python
# -*- coding:utf8 -*-
#导入需要使用到的模块
import urllib
import re
import pandas as pd
#import pymysql
import os
import datetime
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.writer.excel import ExcelWriter
import csv

#抓取特定股票, 保存到csv文本文件
def getStockByCode2EndDate(stockCode,endDate):
    if stockCode[0] == '0':
        if stockCode == '000001':
            url = 'http://quotes.money.163.com/service/chddata.html?code=0'+stockCode+\
            '&end='+endDate+'&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
        else:
            url = 'http://quotes.money.163.com/service/chddata.html?code=1'+stockCode+\
            '&end='+endDate+'&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
    else:
        url = 'http://quotes.money.163.com/service/chddata.html?code=0'+stockCode+\
        '&end='+endDate+'&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
    print(url)
    #urllib.request.urlretrieve(url, '../data/'+stockCode+'.csv')

#抓取特定股票， 保存到csv文本文件
def getStockByCode(stockCode,startDate):
    if stockCode[0] == '0': #深圳市场
        if stockCode == '000001': #上证指数
                url = 'http://quotes.money.163.com/service/chddata.html?code=0'+stockCode+\
                '&start='+startDate+'&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
        else :
                url = 'http://quotes.money.163.com/service/chddata.html?code=1'+stockCode+\
                '&start='+startDate+'&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
    else: #上海市场
        url = 'http://quotes.money.163.com/service/chddata.html?code=0'+stockCode+\
        '&start='+startDate+'&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'

    print(url)
    #urllib.request.urlretrieve(url, '../data/'+stockCode+'.csv')
    urllib.request(url)


#读取csv
def openCsv(csvFileName):
    with open(csvFileName,'r') as csv_file:
        csvFile = csv.reader(csv_file)
        header = next(csvFile)
        #print(header)
        lists = []
        for row in csvFile:
            row[1] = row[1].replace("'","")
            if row[10] == '' :
                row[10] = 0
            if row[13] == '' :
                row[13] = 0
            if row[14] == '' :
                row[14] = 0
            if row[8] == 'None' :
                row[8] = 0
            if row[9] == 'None' :
                row[9] = 0
            if row[3] == 'None' :
                row[3] = 0
            if row[4] == 'None' :
                row[4] = 0
            if row[5] == 'None' :
                row[5] = 0
            if row[6] == 'None' :
                row[6] = 0
            if row[7] == 'None' :
                row[7] = 0
            if row[12] == 'None' :
                row[12] = 0

            lists.append(row)
        return lists


#main
def main():
    #读取上证指数、贵州茅台、洋河股份、五粮液、泸州老窖
    stock_list = ['000001','600519','000568','002304','000858']
    for stock in stock_list:
        endDate = datetime.datetime.now().strftime("%Y%m%d")
        getStockByCode2EndDate(stock,endDate)
        #print(stock,strDate)


if __name__ == '__main__':
    main()

