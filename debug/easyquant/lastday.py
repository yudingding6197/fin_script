#!/usr/bin/env python
# -*- coding:utf8 -*-
#导入需要使用到的模块
import urllib
import re
import pandas as pd
#import pymysql
import os
import datetime
import easyquotation

if __name__ == '__main__':
	quotation = easyquotation.use('sina') # 新浪 ['sina'] 腾讯 ['tencent', 'qq']
	quotation.stocks(['sh000001', 'sz000001'], prefix=True)

