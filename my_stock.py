#!/usr/bin/env python
import asyncio
import pandas as pd
import tushare as ts
import requests
from collections import deque
from aiohttp import ClientSession
import json

import re
import sqlite3


ori_url = 'http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq2017&param=%s,day,2017-01-01,2018-12-31,640,qfq&r=%s'
count = 0
down_data = deque()
KLINE_TT_COLS = ['date', 'open', 'close', 'high', 'low', 'volume']
conn = sqlite3.connect('stock.db')
cu = conn.cursor()

async def hello_aio(q_code):
    while len(q_code) > 0:
        code = q_code.pop()
        url = ori_url % (code, ts.stock.trading._random(17))

        async with ClientSession() as session:
            async with session.get(url)as response:
                lines = await response.text()

                global count

                count += 1

                if len(lines) > 100:
                    lines = lines.split('=')[1]
                    reg = re.compile(r',{"nd.*?}')
                    lines = re.subn(reg, '', lines)
                    js = json.loads(lines[0])
                    down_data.append((js, code))

        await asyncio.sleep(0.01)

async def progress(q_code, max_code):
    current = max_code - len(q_code)
    step = max_code//25
    next_step = step
    while current < max_code:
        current = max_code - len(q_code)
        if current > next_step:
            print(current, max_code)
            next_step += step
        await asyncio.sleep(0.1)

def get_history():
    cor_num = 50
    myd = deque()
    global count
    stock_list = ts.get_stock_basics() ####################
    for stock_code in stock_list.index:
        stock_code = ts.stock.trading._code_to_symbol(stock_code)
        myd.append(stock_code)

    task_list = []
    for i in range(cor_num):
        task_list.append(hello_aio(myd))
    task_list.append(progress(myd, len(myd)))
    
    import time
    start = time.clock()
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(task_list))

    end = time.clock()
    print(end-start)
    print('count:{},  corout:{}'.format(count, cor_num))

    count = 0
    KLINE_TT_COLS = ['date', 'open', 'close', 'high', 'low', 'volume']
    start = time.clock()

    for item in down_data:
        js = item[0]
        code = item[1]

        sql = '''create table if not exists {}(
            id integer primary key autoincrement,
            date date,
            open float,
            close float,
            high float,
            low float,
            volume float
        )'''.format(code)

        cu.execute(sql)
        sql = 'insert into {} values(NULL,?,?,?,?,?,?)'.format(code)
        dataflag = 'qfqday'
        dataflag = dataflag if dataflag in list(js['data'][code].keys()) else 'day'

        cu.executemany(sql, js['data'][code][dataflag])
    conn.commit()
    print(time.clock()-start)
########################################################
if __name__ == '__main__':
    get_history()
