#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import chardet

if __name__=='__main__':
	print chardet.detect('abc123')
	strg = '中国'
	print chardet.detect(strg)
	strg = '中国'.decode('gbk').encode('utf-8')
	print chardet.detect(strg)
	strg = '中国'.decode('gbk').encode('gb2312')
	print chardet.detect(strg)

