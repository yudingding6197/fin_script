# -*- coding:gbk -*-
from bs4 import BeautifulSoup as BS
import urllib.request as ur
import os
import sqlite3
import pandas as pd
# conn = sqlite3.connect('d:/stock/mainforce.db')
# sql = 'insert into lhb(code,day,typ,ranking,depart,buy,buyrate,sell,sellrate,net_value) VALUES (?,?,?,?,?,?,?,?,?,?)'
# cur =conn.cursor()
'''买入和卖出不做分类，看合计的正负'''
url = 'http://data.eastmoney.com/stock/lhb.html'
urlread = ur.urlopen(url)
html = urlread.read().decode('gbk','ignore')
soup = BS(html,'lxml')
table = soup.select('table')
htmlist = []
td = table[0].select('td')              # 上海龙虎板
for i in range(1,len(td)):
    first ="http://data.eastmoney.com/stock"+str(td[i])[33:55]
    htmlist.append(first)
td1 = table[1].select('td')
for r in range(1,len(td1)):
    first1 ="http://data.eastmoney.com/stock"+str(td1[r])[33:55]
    htmlist.append(first1)
x = []
for lhburl in htmlist:
    # print(lhburl)
    try:
        lhburlread = ur.urlopen(lhburl)
        lhbhtml = lhburlread.read().decode('gbk', 'ignore')
    except:
        fl = open('d: st.txt', 'a')            # 爬不成功的页放这里
        fl.write(code)
        fl.write("\n")
        fl.close()
    else:
        lhbsoup = BS(lhbhtml, 'lxml')
        list = lhbsoup.find_all('div', attrs={'class':'content-sepe'})      # 有几个上板理由 （）
        list1 = lhbsoup.find_all('div', attrs={'class':'left con-br'})        # 取日期 类型
        code = lhburl[42:48]            # 股票代码
        print(code)
        for i in range(len(list)):
            day = list1[i].text[:10]       #上榜日期
            l = list1[i].text.index('：')         # l字符值后为上榜类型
            typ = list1[i].text[(l+1):]        # 上榜类型
            lhbtab = list[i].select('table')       #　取数值
            for r in range(len(lhbtab)):
                lhbtr = lhbtab[r].select('tr')
                for d in range(2,len(lhbtr)):
                    lhbtd = lhbtr[d].select('td')
                    if len(lhbtd) == 7:
                        ranking =(lhbtd[0].text)                  #排名
                        depart =(lhbtd[1].select('a')[1].text)        #营业部
                        buy =(lhbtd[2].text)                   #　买入万元
                        buyrate = (lhbtd[3].text)                  #买入占比
                        sell =(lhbtd[4].text)                # 卖出
                        sellrate =(lhbtd[5].text)                # 卖出占比
                        net_value=(lhbtd[6].text)                 # 合计买入
                        y=(code,day,typ,ranking,depart,buy,buyrate,sell,sellrate,net_value)
                        # cur.execute(sql,y)
                        # print(y)
                        x.append(y)
# conn.commit()
# cur.close()
# conn.close()
df = pd.DataFrame(x, columns=['股票代码','上榜日期','上榜原因','排名','营业部','买入额','买入占比','卖出额','卖出占比','净值'])
print(df)
