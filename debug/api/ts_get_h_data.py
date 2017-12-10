#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import time
import datetime
import tushare as ts

'''
        ��ȡ������ʷ���׼�¼
    Parameters
    ------
      code:string
                  ��Ʊ���� e.g. 600848
      start:string
                  ��ʼ���� format��YYYY-MM-DD Ϊ��ʱȡ��API���ṩ��������������
      end:string
                  �������� format��YYYY-MM-DD Ϊ��ʱȡ�����һ������������
      ktype��string
                  �������ͣ�D=��k�� W=�� M=�� 5=5���� 15=15���� 30=30���� 60=60���ӣ�Ĭ��ΪD
      retry_count : int, Ĭ�� 3
                 ��������������ظ�ִ�еĴ��� 
      pause : int, Ĭ�� 0
                �ظ��������ݹ�������ͣ����������ֹ������ʱ��̫�̳��ֵ�����
    return
    -------
      DataFrame
          ����:���� �����̼ۣ� ��߼ۣ� ���̼ۣ� ��ͼۣ� �ɽ����� �۸�䶯 ���ǵ�����5�վ��ۣ�10�վ��ۣ�20�վ��ۣ�5�վ�����10�վ�����20�վ�����������
'''
pindex = len(sys.argv)
code='300611'
if pindex==2:
	code = sys.argv[1]

LOOP_COUNT=0
while LOOP_COUNT<3:
	try:
		df = ts.get_h_data(code)
	except:
		LOOP_COUNT += 1
		time.sleep(0.5)
	else:
		break;
if df is None:
	print "Timeout to get hist data"
	exit(0)

print df.head(6)
