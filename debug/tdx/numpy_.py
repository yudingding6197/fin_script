#!/usr/bin/python
#-*- encoding: gbk -*- 

import numpy as np
import pandas as pd

def read_day_k(path):
    dt = np.dtype([
        ('Date', 'u4'),
        ('Open', 'u4'),
        ('High', 'u4'),
        ('Low', 'u4'),
        ('Close', 'u4'),
        ('Amount', 'f'),
        ('Volume', 'u4'),
        ('Reserve','u4')])
    data = np.fromfile(path, dtype=dt)
    #df = pd.DataFrame(data)
    # Or if you want to explicitly set the column names
    df = pd.DataFrame(data, columns=data.dtype.names)
    df.eval('''
        year=floor(Date/10000)
        month=floor((Date%10000)/100)
        day=floor(Date%10000%100)
        Open=Open/100
        High=High/100
        Low=Low/100
        Close=Close/100
    ''',inplace=True)
    df.index=pd.to_datetime(df.loc[:,['year','month','day']])
    return df.drop(['Date','year','month','day'],1)
def read_min_k(path):
    '''
    year=floor(m_date/2048)+2004; %提取年信息
    mon=floor(mod(m_date,2048)/100); %提取月信息
    day=mod(mod(m_date,2048),100); %提取日信息*/
    m_time/60 输出小时
    m_time%60 输出分钟
    '''
    dt = np.dtype([
        ('m_date', 'u2'),
        ('m_time', 'u2'),
        ('Open', 'f4'),
        ('High', 'f4'),
        ('Low', 'f4'),
        ('Close', 'f4'),
        ('Amount', 'f4'),
        ('Volume', 'u4'),
        ('Reserve','u4')])
    data = np.fromfile(path, dtype=dt)
    #df = pd.DataFrame(data)
    # Or if you want to explicitly set the column names
    df = pd.DataFrame(data, columns=data.dtype.names)
    df.eval('''
        year=floor(m_date/2048)+2004
        month=floor((m_date%2048)/100)
        day=floor(m_date%2048%100)
        hour = floor(m_time/60)
        minute = m_time%60
    ''',inplace=True)
    df.index=pd.to_datetime(df.loc[:,['year','month','day','hour','minute']])
    return df.drop(['m_date','m_time','year','month','day','hour','minute'],1)
path_day = r'C:\vipdoc\sh\lday\sh600025.day'
path_5m = r'./debug/tdx/lc5/sz000001.lc5'
path_1m = r'C:\vipdoc\sh\minline\sh600025.lc1'
#日线数据 = read_day_k(path_day)
data_5m = read_min_k(path_5m)
#一分数据 = read_min_k(path_1m)
#print(日线数据.tail(10))
print(data_5m.tail(10))
#print(一分数据.tail(10))
#print(一分数据.head(10))