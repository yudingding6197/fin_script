#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import chardet

print chardet.detect('我')
s = "中文测试"
#按照utf8编码的中文，在Linux端可以正常输出,Windows CMD无法正常输出
print s
s1 = s.decode('utf8').encode('gbk')
#转为GBK后，在Linux端可以无法正常输出, Windows CMD可以输出
print s1
