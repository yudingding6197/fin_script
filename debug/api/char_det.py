#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import chardet

if __name__=='__main__':
	print chardet.detect('abc123')
	strg = '�й�'
	print chardet.detect(strg)
	strg = '�й�'.decode('gbk').encode('utf-8')
	print chardet.detect(strg)
	strg = '�й�'.decode('gbk').encode('gb2312')
	print chardet.detect(strg)

#�ַ��� ����ת
#"-".join(list)

#�ַ����滻, count����ʡ��
#str.replace("abc","xyz",count)

