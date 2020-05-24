#!/user/bin/env python
# -*- coding:utf-8 -*-
"""
利用 Baostock 的数据源，在给定起止时间内计算单个证券在这段时间的阳线和阴线指
标。
"""
import baostock as bs
import pandas as pd

if __name__ == '__main__':
    login_result = bs.login(user_id='anonymous', password='123456')
    print(login_result.error_msg)
