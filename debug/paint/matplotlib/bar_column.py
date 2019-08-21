#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import urllib2
import json
import zlib
import random
import getopt
import datetime

import matplotlib.pyplot as plt
import numpy as np

# 创建一个点数为 8 x 6 的窗口, 并设置分辨率为 80像素/每英寸
plt.figure(figsize=(8, 6), dpi=80)

# 再创建一个规格为 1 x 1 的子图
plt.subplot(1, 1, 1)

# 柱子总数
N = 6
# 包含每个柱子对应值的序列
values = (25, 32, 34, 20, 41, 50)

# 包含每个柱子下标的序列
index = np.arange(N)

# 柱子的宽度
width = 0.35

# 绘制柱状图, 每根柱子的颜色为紫罗兰色
p2 = plt.bar(index, values, width, label="rainfall", color="#87CEFA")

# 设置横轴标签
plt.xlabel('Months')
# 设置纵轴标签
plt.ylabel('rainfall (mm)')

# 添加标题
plt.title('Monthly average rainfall')

# 添加纵横轴的刻度
plt.xticks(index, ('Jan', 'Fub', 'Mar', 'Apr', 'May', 'Jun'))
plt.yticks(np.arange(0, 81, 10))

# 添加图例
plt.legend(loc="upper right")

plt.show()