#!/usr/bin/env python
# -*- coding:utf8 -*-
#导入需要使用到的模块
import urllib
import re
import pandas as pd
import pymysql
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
    urllib.request.urlretrieve(url, '../data/'+stockCode+'.csv')

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
    urllib.request.urlretrieve(url, '../data/'+stockCode+'.csv')

#连接数据库
def connect(host,port,user,passwd,db):
    conn = pymysql.Connect(host=host,port=port,user=user,passwd=passwd,db=db,charset='utf8')
    #print(conn)
    return conn

#关闭数据库连接
def close(conn):
    conn.close()

#查询数据库
def select(conn,sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    #print("cursor.excute:",cursor.rowcount) 
    #rs = cursor.fetchone()
    rs = cursor.fetchall()
    return rs


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

#批量插入数据库
def batchInsert(table,lists):
    print('begin insert...')
    conn = connect('127.0.0.1',3306,'root','123456','finance_db')
    conn.autocommit(False)
    cursor = conn.cursor()
    try:
        cursor.executemany('insert into '+table+' values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',lists)
        conn.commit()
        print('end ok')
    except Exception as e:
        print("Reason:",e)
        conn.rollback()

    print(cursor.rowcount)
    cursor.close()
    conn.close()


#main
def main():
    #读取上证指数、贵州茅台、洋河股份、五粮液、泸州老窖
    stock_list = ['000001','600519','000568','002304','000858']
    conn = connect('127.0.0.1',3306,'root','123456','finance_db')
    for stock in stock_list:
        statement = 'select left(max(trans_date),10) from t_stock where stock_code = '+stock
        rs = select(conn,statement)
        if rs[0][0] is None:
            endDate = datetime.datetime.now().strftime("%Y%m%d")
            getStockByCode2EndDate(stock,endDate)
            print(stock,strDate)
        else:
            startDate = datetime.datetime.strptime(rs[0][0], '%Y-%m-%d')
            startDate = startDate + datetime.timedelta(days=1)
            strDate = startDate.strftime("%Y%m%d")
            print(stock,strDate)
            getStockByCode(stock,strDate)

        ecsvFile = '../data/'+stock+'.csv'
        lists = openCsv('../data/'+stock+'.csv')
        if len(lists) > 0:
            batchInsert('t_stock',lists)

if __name__ == '__main__':
    main()

