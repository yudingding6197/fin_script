# -*- coding:gbk -*-
import os
import pymysql
import time
# 1min 数据导出后 运行
pathsh = os.listdir('c:/new_gxzq_v6ipdoc/送花/minline')
for sh in pathsh:
    shname = os.path.join('c:/new_gxzq_v6ipdoc/送花/minline/',sh)
    os.remove(shname)
pathsz = os.listdir('c:/new_gxzq_v6ipdoc/sz/minline')
for sz in pathsz:
    szname = os.path.join('c:/new_gxzq_v6ipdoc/sz/minline/',sz)
    os.remove(szname)

Dir =  os.listdir('c:/1min')
for name in Dir:
    start=time.clock()
# 连接数据库取值
    config = {
          'host':'127.0.0.1',
          'port':3306,
          'user':'root',
          'password':'',
          'db':'stock',
          'charset':'utf8mb4'
          }
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    sql = "insert into one_min values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    filename = os.path.join('%s%s' % ('c:/1min/', name))
    f_open = open(filename,'r')
    f_read =f_open.readlines()
    f_open.close()
    code = f_read[0].split(' ')[0]   # 第一行 切出股票代码
    for i in range(2,len(f_read)-1):        #
        row_list=f_read[i].strip('\n')  # strip()函数去\n
        line_list = row_list.split(",")   # 切割
        line_list.insert(2,code)          # code插入到第三个位置
        x = tuple(line_list)
        cur.execute(sql,x)
    print(code)
    conn.commit()
    conn.close()
    os.remove(filename)
    end = time.clock()
    print(round((end-start),3))