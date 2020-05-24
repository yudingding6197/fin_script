#!/usr/bin/env python
# -*- coding:utf8 -*-
import json
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def run():
    ''' 主程序, 用来调度各个重要流程 '''
    kline = load_sse()
    df = init_df(kline)
    df = strategy(df)
    df = backtest(df)
    draw(df,days)
    df.to_csv('result.csv', index = False)

def load_sse():
    ''' 获取上交所的上证指数K线, 最近N个交易日数据 '''
    response = requests.get(
        # 'http://yunhq.sse.com.cn:32041/v1/sh1/dayk/000001?callback=jQuery111205234775875526079_1542185571865&select=date%2Copen%2Chigh%2Clow%2Cclose%2Cvolume&begin=-2000&end=-1&_=1542185571881',
        'http://yunhq.sse.com.cn:32041/v1/sh1/dayk/000001?callback=jQuery111205234775875526079_1542185571865&select=date%2Copen%2Chigh%2Clow%2Cclose%2Cvolume&begin=-'+ begin +'&end=-'+ end +'&_=1542185571881',
        headers={'Referer': 'http://www.sse.com.cn/market/price/trends/'}
    )

    # 针对结果进行格式处理
    json_str = response.text[42:-1]
    data = json.loads(json_str)
    return data['kline']

def init_df(kline):
    ''' 根据K线数据，创建含有日期与收盘价的矩阵 '''
    df = pd.DataFrame({})
    df['date'] =  [x[0] for x in kline]
    #kline中包含日期、开盘价、最高价、最低价、收盘价等信息
    df['close'] = [x[1] for x in kline]

    return df

def strategy(df):
    # 连续15天数据，计算平均值，作为当天的平均价格指标
    window_size = 15
    df['avg'] = df['close'].rolling(window_size).apply(lambda x: sum(x) / len(x))

    def avg_buy(x):
        ''' 做多策略 '''
        min_percent = 0.995
        max_percent = 1.005
        # 追涨，当我们的价格超过了均线一定程度时
        if (x[1] / x[0]) < min_percent:
            return 'open buy'
        # 杀跌，当我们的价格低于均线一定程度时
        if (x[1] / x[0]) > max_percent:
            return 'close buy'
        # 其他情况不操作
        return 'wait'

    # df['action'] = avg_buy([df['close'], df['avg']])
    df['action'] = df[['close', 'avg']].apply(avg_buy, axis=1)
    return df

def backtest(df):
    ''' 回归测试 '''
    global shares, cash
    amount = 1000000
    shares = 0
    cash = amount

    def run_strategy(row):
        ''' 把每天的数据执行策略 '''
        global shares, cash
        action = row['action']
        close = row['close']

        # 资产 = 现金 + 股票价值
        liquidate = cash + shares * close
        message = 'nothing'

        # 策略要求开仓做多，而且当前空仓时，做多
        if action == 'open buy' and shares == 0:
            shares = int(cash / close)
            cash -= shares * close
            message = 'open buy ' + str(shares)

        # 策略要求平仓，而且当前有仓时，平掉
        if action == 'close buy' and shares > 0:
            message = 'close buy ' + str(shares)
            cash += shares * close
            shares = 0

        return [message, shares, cash, liquidate]

    rows = df[['close', 'action']].apply(run_strategy, axis=1)
    df['message'], df['shares'], df['cash'], df['liquidate'] = zip(*rows)
    return df

def draw(df,days):
    ''' 画图 '''
    # 创建画板
    fig = plt.figure(figsize=(10, 5))

    # 准备横坐标
    count = df.count()['close']
    index = np.arange(count)
    df['index'] = index

    # 设置横坐标的刻度与显示标签
    limit = days
    plt.xticks(index[::limit], df['date'][::limit])

    # 收盘价与资产的两套坐标系
    ax_close = plt.gca()
    ax_liquidate = ax_close.twinx()

    # 画收盘价曲线
    ax_close.set(xlabel='Date', ylabel='close')
    l_close, = ax_close.plot(index, df['close'], 'black', label='close')
    l_avg, = ax_close.plot(index, df['avg'], 'pink', label='avg')

    # 画资产曲线
    ax_liquidate.set(ylabel = 'liquidate')
    l_liquidate, = ax_liquidate.plot(index, df['liquidate'], 'blue', label='liquidate')

    def drawAction(row):
        if row['message'] == 'nothing':
            return

        color = ''
        marker = 'o'
        size = 12

        if row['action'] == 'open buy':
            color='r'
        if row['action'] == 'close buy':
            color='g'

        ax_close.scatter(row['index'], row['close'], s=size, color=color, zorder=2, marker=marker)

    df[['index', 'action', 'message', 'close']].apply(drawAction, axis=1)

    # 给两条线都提供一个图例说明
    plt.legend(handles=[l_close, l_avg, l_liquidate])
    plt.show()

if __name__ == '__main__':
    begin=input('从前多少天：')
    end=input('到最近几天：')
    days=input('横坐标日期间隔天数：')
    days=int(days)
    run()
