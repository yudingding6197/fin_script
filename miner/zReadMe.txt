Step 1:
如果有TDX数据
	1.通过TDX进行指定日期筛选，将文本拷贝到../data/entry/tdx_history/下
	2.tdx_data_extract.py 进行筛选当天不交易的item
如果没有TDX的数据
	前一日交易信息：
		1.debug\lastest_market.py更新
		#分离交易和TP的数据，不用参数
		2.miner\filter_not_trade_code.py
	如果期望更新当天交易信息：
		1.debug\lastest_market.py更新
		2.miner\filter_not_trade_code.py -dMMDD(当天交易日期)
	以前的交易数据，如果使用filter_not_trade_code，将加载tdx_apis，速度太慢不合适
	所以建议使用TDX进行过滤

3.down_day_tick.py下载数据
4.verify_day_trade_items.py下载完成后，尝试校验
5.miner_data.py请矿工挖矿吧！！！
