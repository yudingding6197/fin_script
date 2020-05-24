#!/usr/bin/env python
# -*- coding:utf8 -*-
if __name__ == '__main__':
    list = ['html', 'js', 'css', 'python']

    # 方法1
    print '1'
    for i in list:
        print ("num:%d   value:%s" % (list.index(i) + 1, i))

    print '\n2：'
    # 方法2
    for i in range(len(list)):
        print ("num:%d   value:%s" % (i + 1, list[i]))

    # 方法3
    print '\n3：'
    for i, val in enumerate(list):
        print ("num:%d   value:%s" % (i + 1, val))

    # 方法3
    print '\n4 （设置遍历开始初始位置，只改变了起始序号）：'.decode('utf8')
    for i, val in enumerate(list, 2):
        print ("num:%d   value:%s" % (i + 1, val))