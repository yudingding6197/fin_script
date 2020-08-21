
===== 新浪：=====================
分价表
http://market.finance.sina.com.cn/pricehis.php?symbol=sh600900&startdate=2011-08-17&enddate=2011-08-19
http://vip.stock.finance.sina.com.cn/quotes_service/view/cn_price.php?symbol=

分时：分钟K线， 获取深圳市场002095股票的 5 分钟数据，获取最近的 240 个节点
http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=sz002095&scale=5&ma=no&datalen=240
这个更加稳定
https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol=sh000300&scale=30&ma=no&datalen=1023
https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol=sh000300&scale=240&ma=no&datalen=60

前复权，后面参数需要再确认
http://finance.sina.com.cn/realstock/company/sz002095/qianfuquan.js?d=2015-06-16


方法5：http://market.finance.sina.com.cn/downxls.php?date=[日期]&symbol=[市场][股票代码]
返回数据：XLS文件；股票历史成交明细。
http://market.finance.sina.com.cn/downxls.php?date=2015-06-15&symbol=sz002095
获取2015-06-15日期的深圳市长002095数据。

方法6：http://market.finance.sina.com.cn/pricehis.php?symbol=[市场][股票代码]&startdate=[开始日期]&enddate=[结束日期]
返回数据：HTML文本；指定日期范围内的股票分价表。
http://market.finance.sina.com.cn/pricehis.php?symbol=sh600900&startdate=2011-08-17&enddate=2011-08-19
获取上证600900股票2011-08-17到2011-08-19日期的分价数据


逐分钟 当天 新浪投资易
https://touzi.sina.com.cn/public/mystock
https://stock.sina.com.cn/stock/api/jsonp.php/var%20_sh6001032017=/TouziService.getStockMinuteFlow?symbol=sh600103&random=$rn
https://stock.sina.com.cn/stock/api/jsonp.php//TouziService.getStockMinuteFlow?symbol=sh600103&
.replace(/\(newString\(|\(newString\(|\)\);/g,'')

新浪关键词查询股票接口 
http://suggest3.sinajs.cn/suggest/type=&key=000627&name=suggestdata_1429775785401



===== 网易：=====================
分价表
http://quotes.money.163.com/trade/fjb_688516.html
http://quotes.money.163.com/service/fenjia_table.html?symbol=300847&sort=PRICE&order=-1
    <a href="/trade/fjb_300849.html?sort=PRICE&order=1">  VOL  VOL_BUY_PERCENT VOL_TOTAL_PERCENT

获取为json格式数据
http://img1.money.126.net/data/hs/kline/day/times/1399001.json
http://img1.money.126.net/data/hs/kline/day/times/0000001.json

获取为csv文件
http://quotes.money.163.com/service/chddata.html?code=0000001
http://quotes.money.163.com/service/chddata.html?code=0000001&start=19901219&end=20150911&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER


方法1：http://img1.money.126.net/data/[沪深拼音]/time/today/[股票代码].json
返回结果：当日分时图数据；JSON数据；分时图获取数据依次是count节点数量、symbol股票代码、name股票名称、data数据，其中数据依次是小时分钟时间、价格、均价、成交量。
注意，沪深拼音为简写hs，以此可以推断出其他市场也可以获取，具体请自行判断研究。
例如，http://img1.money.126.net/data/hs/time/today/1399001.json，返回深证成指当日分时图数据。

方法2：http://img1.money.126.net/data/hs/time/4days/[股票代码].json
返回结果：获取4天分时数据；和上述分时图相似，但数据是连续4天的数据，不包括当天的数据。

方法3：http://img1.money.126.net/data/[沪深拼音]/[是否复权]/day/history/[年份]/[股票代码].json
返回结果：获取日线数据。
其中，是否复权，不复权为kline，复权为klinederc。
例如，http://img1.money.126.net/data/hs/kline/day/history/2015/1399001.json，获取深证成指2015年所有日线数据。

方法4：http://img1.money.126.net/data/[沪深拼音]/[是否复权]/[周期]/times/[股票代码].json
返回结果：获取日线所有时间节点和收盘价。
其中，[是否复权]，不复权为kline，复权为klinederc。
其中，[周期]，day为日数据，week周数据，month月数据。
例如，http://img1.money.126.net/data/hs/kline/day/times/1399001.json，获取深证成指所有时间节点数据。

方法5：http://quotes.money.163.com/cjmx/[今年年份]/[日期]/[股票代码].xls
返回结果：获取历史成交明细；XLS文件。
注意，只能获取5日内的数据，再之前的数据不会存在。
注意，该方法为网易公开获取数据方法，推荐使用。
例如，http://quotes.money.163.com/cjmx/2015/20150611/0601857.xls，获取0601857股票的2015年6月11日历史成交明细XLS文件。

方法6：http://quotes.money.163.com/service/chddata.html?code=[股票代码]&start=[开始日期]&end=[结束日期]&fields=[自定义列]
返回结果：历史股价及相关情况；CSV文件。
注意，该方法为网易公开方法，推荐使用。
其中，自定义列可定义TCLOSE收盘价 ;HIGH最高价;LOW最低价;TOPEN开盘价;LCLOSE前收盘价;CHG涨跌额;PCHG涨跌幅;TURNOVER换手率;VOTURNOVER成交量;VATURNOVER成交金额;TCAP总市值;MCAP流通市值这些值。
例如，http://quotes.money.163.com/service/chddata.html?code=0601857&start=20071105&end=20150618&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP，获取0601857从2007-11-05到2015-06-18区间的数据。



===== 东财：=====================
分时：分钟K线，获取深圳市场 300291 股票的 5 分钟数据
http://push2his.eastmoney.com/api/qt/stock/kline/get?cb=jQuery112407193784553515159_1594787036303&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf61&klt=5&fqt=1&secid=0.300291&beg=0&end=20500000
http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=4&id=0003001&type=m30k&_=1546486249481
rtntype = 返回数据格式，支持：1,2,3,4,5,6
id = 股票代码，后面多加个1
type = k线类型，m5k,m15k,m30k,m60k


===== 腾讯：=====================
实时行情：
http://stockhtm.finance.qq.com/sstock/ggcx/600103.shtml
http://qt.gtimg.cn/q=sh600103
http://web.sqt.gtimg.cn/q=sh600103 

有当天总成交量 外盘内盘 买卖各5挡 成交量 成交额 市值 等信息。

分时成交 当天
http://stockhtm.finance.qq.com/sstock/quotpage/q/600103.htm#detail
http://stock.gtimg.cn/data/index.php?appn=detail&action=data&c=sh600103&p=0
http://stock.gtimg.cn/data/index.php?appn=detail&action=data&c=sh600103&p=1



逐分钟 当天
http://stockhtm.finance.qq.com/sstock/ggcx/600103.shtml
http://web.ifzq.gtimg.cn/appstock/app/minute/query?code=sh600103
http://web.ifzq.gtimg.cn/appstock/app/minute/query?_var=min_data_sh600103&code=sh600103&r=0.12174363108800135


分价表 当天
http://stockhtm.finance.qq.com/sstock/quotpage/q/600103.htm#price
http://stock.gtimg.cn/data/index.php?appn=price&c=sh600103

日K
	按照年来处理
	http://data.gtimg.cn/flashdata/hushen/daily/19/sz000750.js?visitDstTime=1

	日K 后复权
	http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayhfq&param=sh600103,day,,,320,hfq&r=0.9860043111257255
	320代表查询几天的历史数据 初步推断 1年为320 两年为640
	http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayhfq&param=sh600103,day,1998-01-01,1998-12-31,320,hfq&r=0.444157593883574
	http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayhfq&param=sh600103,day,1999-01-01,1999-12-31,320,hfq&r=0.7529798413161188
	http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayhfq2000&param=sh600103,day,2000-01-01,2001-12-31,640,hfq&r=0.7360555452760309

	http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=sz000001,day,2017-12-01,,640,qfq
	参数简述：
	param=代码,日k，开始日期，结束日期，获取多少个交易日，前复权
	不复权
	http://web.ifzq.gtimg.cn/appstock/app/kline/kline?_var=kline_day&param=sz000001,day,2019-12-01,,640,

日K线 百度股市通
https://gupiao.baidu.com/stock/sh600103.html
https://gupiao.baidu.com/api/stocks/stockdaybar?from=pc&os_ver=1&cuid=xxx&vv=100&format=json&stock_code=sh600103&step=3&start=&count=320&fq_type=front&timestamp=1486464067730
https://gupiao.baidu.com/api/stocks/stockdaybar?from=pc&os_ver=1&cuid=xxx&vv=100&format=json&stock_code=sh600103&step=3&start=20150907&count=160&fq_type=no&timestamp=1486463762308



修改count的值为最大，不带start即可。 fq_type为复权。
分时成交Excel：
http://stock.gtimg.cn/data/index.php?appn=detail&action=download&c=sh600103&d=20170124 旧新都有
http://market.finance.sina.com.cn/downxls.php?date=2017-01-24&symbol=sh600103 新的全


http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=sz300178&scale=5&ma=no&datalen=240


===== 凤凰网：=====================
http://api.finance.ifeng.com/akmin?scode=sh000300&type=30
scode = 股票代码
type =  k线类型




