#!/usr/bin/env python
# -*- coding:utf8 -*-

def chgList(list):
	list.append("kk")
	print list
	
if __name__=="__main__":
	list = ['aa', 'cb', 'dad']
	print("List id is", id(list))

	chgList(list)
	print("List id is", id(list))
