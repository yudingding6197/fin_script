#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import urllib2
import json
import zlib
import random
import getopt
import datetime

import matplotlib.pyplot as plt  #plt是约定俗成的别名
 
plt.plot([3, 1, 4, 5, 2])  #只有一个列表时默认是y轴坐标
plt.ylabel("Grade")       #y轴标签
plt.savefig("mat1", dpi=700)  #保存为png文件，文件名是mat1,dpi是图片质量.
plt.show()
