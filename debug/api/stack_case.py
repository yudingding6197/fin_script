#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
PY_VER=2
if sys.version > '3':
	PY_VER = 3
	from tkinter import *
else:
	PY_VER = 2
	from Tkinter import *

import time
import os
from ctypes import *
#from ctypes import string_at
import ctypes
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from collections import deque


if __name__ == '__main__':
    dq = deque()? #��ʼ��һ���µ�deque����ȻҲ���Դ�������list�����Ķ�����ʼ����
    dq.pop()? # ��ջ������
    dq.append(x)? #ѹջ
    len(dq)? #ջ��С
    dq[-1]? #ȡջ��Ԫ��

    #FIFO���е�ʵ�֣�
    dq = deque([1,2,3,4,5,6,7], maxlen=7)? #��ʼ��һ���µ�deque����ȻҲ���Դ�������list�����Ķ�����ʼ����
    dq.popleft()??#���׵���Ԫ�أ�������
    dq.append(x)? #ѹԪ�������β
   ?len(dq)? #ջ��С
    dq[0]? #ȡ��β
    dq[-1] #ȡ����
    
