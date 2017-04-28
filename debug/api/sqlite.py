#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import sqlite3

dbname = 'test.db'
def query():
	conn = sqlite3.connect(dbname)
	cursor = conn.cursor()
	# 执行查询语句:
	cursor.execute('select * from user where id=?', ('1',))
	#cursor.execute('select * from user where name=? and pwd=?', ('abc', '123456'))
	# 获得查询结果集:
	values = cursor.fetchall()
	print values
	cursor.close()
	conn.close()
	
if __name__ == '__main__':
	conn = sqlite3.connect(dbname)
	cursor = conn.cursor()
	cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
	cursor.execute('insert into user (id, name) values (\'1\', \'Michael\')')
	#print cursor.rowcount
	cursor.close()
	conn.commit()
	conn.close()

	query()