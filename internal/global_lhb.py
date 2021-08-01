#!/usr/bin/env python
# -*- coding:utf8 -*-

LHB_folder = "..\data\entry\lhb"
LHB_fileFmt = "%s\%s\lhb_dfcf_%s.txt"
LHB_fileFmtDtl = "%s\%s\lhb_dfcf_%s_full.log"
LHB_date_fmt = '%04d-%02d-%02d'

#
g_LHB_zhang = 0
#
g_LHB_zhen = 1
g_LHB_hs = 2
g_LHB_die = 3
g_LHB_3d_zhang = 4
g_LHB_3d_st_zhang = 5
g_LHB_3d_die = 6
g_LHB_3d_st_die = 7
g_LHB_3d_hs = 8
g_LHB_rongzi = 9
g_LHB_yidong_z = 10
g_LHB_yidong_d = 11

g_LHB_xin = 12

g_LHB_tuishi = 13
g_LHB_other = 20

g_LHB_desc = {
	u"日涨幅偏离值达到7%的前5只证券":g_LHB_zhang,   #SHEN ZB
	u"日涨幅偏离值达到7%的前五只证券":g_LHB_zhang,  #SHEN ZB prevail
	u"日价格涨幅偏离值达到":g_LHB_zhang,  #SHEN ZB prevail
	u"日价格涨幅达到":g_LHB_zhang,  #SHEN CYB prevail 改变
	u"日涨幅达到15%的前5只证券":g_LHB_zhang,
	u"有价格涨跌幅限制的日收盘价格涨幅偏离值达到7%的前三只证券":g_LHB_zhang,
	u"有价格涨跌幅限制的日收盘价格涨幅达到15%的前五只证券":g_LHB_zhang,
	u"日振幅值达到15%的前5只证券":g_LHB_zhen,   #SHEN ZB
	u"日振幅值达到15%的前五只证券":g_LHB_zhen,  #SHEN ZB and CY prevail
	u"日价格振幅达到":g_LHB_zhen,   #SHEN ZB
	u"日振幅值达到30%的前5只证券":g_LHB_zhen,	
	u"有价格涨跌幅限制的日价格振幅达到15%的前三只证券":g_LHB_zhen,
	u"有价格涨跌幅限制的日价格振幅达到":g_LHB_zhen,    #HU KC prevail 改变
	u"日换手率达到20%的前5只证券":g_LHB_hs,   #SHEN ZB
	u"日换手率达到20%的前五只证券":g_LHB_hs,  #SHEN ZB prevail
	u"日换手率达到":g_LHB_hs,  #SHEN ZB prevail
	u"日换手率达到30%的前5只证券":g_LHB_hs,
	u"有价格涨跌幅限制的日换手率达到20%的前三只证券":g_LHB_hs,
	u"有价格涨跌幅限制的日换手率达到30%的前五只证券":g_LHB_hs,
	u"连续三个交易日内，涨幅偏离值累计达到20%的证券":g_LHB_3d_zhang,
	u"异常期间价格涨幅偏离值累计达到":g_LHB_3d_zhang,     #SHEN ZB prevail 改变
	u"非ST、*ST和S证券连续三个交易日内收盘价格涨幅偏离值累计达到20%的证券":g_LHB_3d_zhang,
	u"连续三个交易日内，涨幅偏离值累计达到30%的证券":g_LHB_3d_zhang,
	u"有价格涨跌幅限制的连续3个交易日内收盘价格涨幅偏离值累计达到30%的证券":g_LHB_3d_zhang,
	u"有价格涨跌幅限制的连续+":g_LHB_3d_zhang,   #HU KC prevail 改变
	u"连续三个交易日内，涨幅偏离值累计达到12%的ST证券、*ST证券和未完成股改证券":g_LHB_3d_st_zhang,
	u"异常期间价格涨幅偏离值累计达到ST":g_LHB_3d_st_zhang,
	u"连续三个交易日内，涨幅偏离值累计达到12%的ST证券、*ST证券":g_LHB_3d_st_zhang,   #SHEN ZB
	u"ST、*ST和S证券连续三个交易日内收盘价格涨幅偏离值累计达到15%的证券":g_LHB_3d_st_zhang,
	u"连续三个交易日内，日均换手率与前五个交易日的日均换手率的比值达到30倍，且换手率累计达20%的证券":g_LHB_3d_hs,
	u"日跌幅偏离值达到7%的前5只证券":g_LHB_die,   #SHEN ZB
	u"日价格跌幅偏离值达到":g_LHB_die,   #SHEN ZB prevail 改变
	u"日跌幅偏离值达到7%的前五只证券":g_LHB_die,  #SHEN ZB and CY prevail
	u"日价格跌幅达到":g_LHB_die,   #SHEN CY prevail 改变
	u"有价格涨跌幅限制的日收盘价格跌幅偏离值达到7%的前三只证券":g_LHB_die,
	u"有价格涨跌幅限制的日收盘价格跌幅达到15%的前五只证券":g_LHB_die,  #HU
	u"日跌幅达到15%的前5只证券":g_LHB_die,   #HU
	u"连续三个交易日内，跌幅偏离值累计达到20%的证券":g_LHB_3d_die,  #SHEN
	u"连续三个交易日内，跌幅偏离值累计达到30%的证券":g_LHB_3d_die,  #SHEN CY
	u"有价格涨跌幅限制的连续-":g_LHB_3d_die,  #SHEN CY prevail 改变
	u"异常期间价格跌幅偏离值累计达到":g_LHB_3d_die,  #SHEN ZB prevail 改变
	u"非ST、*ST和S证券连续三个交易日内收盘价格跌幅偏离值累计达到20%的证券":g_LHB_3d_die,   #HU
	u"连续三个交易日内，跌幅偏离值累计达到12%的ST证券、*ST证券和未完成股改证券":g_LHB_3d_st_die, #SHEN
	u"异常期间价格跌幅偏离值累计达到ST":g_LHB_3d_st_die, #SHEN ZB prevail 改变
	u"连续三个交易日内，跌幅偏离值累计达到12%的ST证券、*ST证券":g_LHB_3d_st_die, #HU
	u"ST、*ST和S证券连续三个交易日内收盘价格跌幅偏离值累计达到15%的证券":g_LHB_3d_st_die,  #HU ST 3days
	u"单只标的证券的当日融资买入数量达到当日该证券总交易量的50％以上":g_LHB_rongzi,
	u"严重异常期间日收盘价格跌幅偏离值累计达到50%的证券":g_LHB_yidong_z,      #SHEN CY
	u"严重异常期间3次出现正向异常波动的证券":g_LHB_yidong_z,    #SHEN CY
	u"严重异常期间日收盘价格跌幅偏离值累计达到":g_LHB_yidong_z,    #SHEN CY prevail 改变
	u"严重异常期间日收盘价格跌幅偏离值累计达到":g_LHB_yidong_z,    #SHEN CY prevail 改变
	u"严重异常期间日收盘价格涨幅偏离值累计达到100%的证券":g_LHB_yidong_d,     #SHEN CY
	u"无价格涨跌幅限制":g_LHB_xin,
	u"无价格涨跌幅限制的证券":g_LHB_xin,
	u"当日无价格涨跌幅限制的A股，出现异常波动停牌的":g_LHB_xin,
	u"退市整理期":g_LHB_tuishi,
	u"退市整理的证券":g_LHB_tuishi,
	u"Other":1000
}

