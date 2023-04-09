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
    dq = deque()? #初始化一个新的deque，当然也可以传入诸如list这样的东西初始化。
    dq.pop()? # 弹栈并返回
    dq.append(x)? #压栈
    len(dq)? #栈大小
    dq[-1]? #取栈顶元素

    #FIFO队列的实现：
    dq = deque([1,2,3,4,5,6,7], maxlen=7)? #初始化一个新的deque，当然也可以传入诸如list这样的东西初始化。
    dq.popleft()??#队首弹出元素，并返回
    dq.append(x)? #压元素入队列尾
   ?len(dq)? #栈大小
    dq[0]? #取队尾
    dq[-1] #取队首
    
