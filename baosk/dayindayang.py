#!/user/bin/env python
# -*- coding:utf-8 -*-
"""
利用 Baostock 的数据源，在给定起止时间内计算单个证券在这段时间的阳线和阴线指
标。
"""
import baostock as bs
import pandas as pd
def judge_kline_category(code, startdate, enddate):
    """判断证券在起止时间内的每日 K 线类别：阳线，阴线
    :param code:证券代码
    :param startdate:起始日期
    :param enddate:截止日期
    :return:
    """
    login_result = bs.login(user_id='anonymous', password='123456')
    print(login_result.error_msg)
    # 获取股票日 K 线数据,adjustflag 复权状态(1：后复权， 2：前复权，3：不复权）
    rs = bs.query_history_k_data(code,"date,code,open,high,low,close,tradeStatus", start_date=startdate,end_date=enddate, frequency="d", adjustflag="3")
    # 打印结果集
    result_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        result_list.append(rs.get_row_data())
    df_init = pd.DataFrame(result_list, columns=rs.fields)
    # 剔除停盘数据
    df_status = df_init[df_init['tradeStatus'] == '1']
    df_status['open'] = df_status['open'].astype(float)
    df_status['high'] = df_status['high'].astype(float)
    df_status['low'] = df_status['low'].astype(float)
    df_status['close'] = df_status['close'].astype(float)
    df_status['kline_category'] = df_status.apply(
    lambda x: judge_function(x.open, x.close), axis=1)
    df_status.to_csv('C:/work/invest/fin_script/df.csv')
    return df_status

def kline_application(df, N):
    """已知证券在起止时间内的每日 K 线类别：阳线，阴线。
    做如下统计：
    情景 1. 若证券股价连续 N 天下跌后出现大阳线，次日股价开盘上涨的次数
   （第 N+2 天）
    情景 2. 若证券股价连续 N 天上涨之后出现大阴线，次日股价开盘下跌的次数
   （第 N+2 天）
    :return:
    """
    daycounts = df.shape[0]
    df['kline_numb'] = [1 if x == 'positive' else 0 for x in df['kline_category']]
    df['scene'] = 0
    total_counts_1 = 0 # 计算情景 1 中证券股价连续 N 天下跌后出现大阳线的次数
    total_counts_1_sub = 0 # 计算情景 1 出现的次数
    total_counts_2 = 0 # 计算情景 2 中证券证券股价连续 N 天上涨之后出现大阴线的次数
    total_counts_2_sub = 0 # 计算情景 2 出现的次数
    for i in range(0, daycounts - N - 1):
        kline_numb_counts = 0
        for j in range(0, N):
            kline_numb_counts += df.iloc[i + j, 8]
        if kline_numb_counts == N and df.iloc[i + N, 8] == 0:
            # 表明该证券连续 N 天上涨后出现了大阴线
            total_counts_2 += 1
            if df.iloc[i + N + 1, 2] < df.iloc[i + N, 5]:
                total_counts_2_sub += 1
                df.iloc[i + N, 9] = 2 # 表明这一天属于情景 2
        if kline_numb_counts == 0 and df.iloc[i + N, 8] == 1:
            # 表明该证券连续 N 天下跌后出现了大阳线
            total_counts_1 += 1
            if df.iloc[i + N + 1, 2] > df.iloc[i + N, 5]:
                total_counts_1_sub += 1
                df.iloc[i + N, 9] = 1 # 表明这一天属于情景 1
    df.to_csv('C:/work/invest/fin_script/df2.csv')
    print("证券代码：" + df['code'][0])
    print("证券股价连续 N 天下跌后出现大阳线的总次数：" + str(total_counts_1))
    print("若证券股价连续 N 天下跌后出现大阳线，次日股价开盘上涨的次数（第N+2 天）:" + str(total_counts_1_sub) + ",占比：" + str(total_counts_1_sub / total_counts_1))
    print("证券股价连续 N 天上涨之后出现大阴线的总次数：" +str(total_counts_2))
    print("若证券股价连续 N 天上涨之后出现大阴线，次日股价开盘下跌的次数（第N+2 天）:" + str(total_counts_2_sub) + ",占比：" + str(total_counts_2_sub / total_counts_2))
    return(total_counts_1, total_counts_1_sub, total_counts_2,total_counts_2_sub)

def judge_function(open, close):
    if open > close:
        return 'negative'
    else:
        return 'positive'

if __name__ == '__main__':
    code = "sh.600000"
    startdate = "2000-01-01"
    enddate = "2018-01-01"
    N = 3
    df = judge_kline_category(code, startdate, enddate)
    kline_application(df, N)