#!/usr/bin/env python
# -*- coding:gbk -*-
import sys
import re
import os
import string


STK_ZT = 1<<0
STK_DT = 1<<1
STK_ZTHL = 1<<2
STK_DTFT = 1<<3
STK_YZZT = 1<<4
STK_YZDT = 1<<5
STK_OPEN_ZT = 1<<6
STK_OPEN_DT = 1<<7
STK_ST_YZZT = 1<<8
STK_ST_YZDT = 1<<9
trade_data= None

class statisticsItem:
	s_zt = 0
	s_dt = 0
	s_zthl = 0
	s_dtft = 0
	s_yzzt = 0
	s_yzdt = 0
	s_cxzt = 0
	s_cxdt = 0
	s_open_zt = 0		#涨停开盘
	s_close_zt = 0		#涨停开盘个股收盘仍涨停
	s_open_T_zt = 0		#涨停开盘个股收盘仍涨停，非一字
	s_zt_o_gt_c = 0		#触及涨停,开盘价高于收盘价
	s_dk_zt = 0			#开盘涨停，收盘打开涨停
	s_open_dt = 0		#跌停开盘
	s_dt_daoT = 0		#跌停开盘，倒T
	s_st_yzzt = 0
	s_st_yzdt = 0
	s_open_sz = 0		#开盘上涨
	s_open_xd = 0		#开盘下跌
	s_open_pp = 0		#开盘平盘
	s_open_dz = 0		#开盘大涨
	s_open_dd = 0		#开盘大跌
	s_close_sz = 0		#收盘上涨
	s_close_xd = 0		#收盘下跌
	s_close_pp = 0		#收盘平盘
	s_close_dz = 0		#收盘大涨
	s_close_dd = 0		#收盘大跌
	s_high_zf = 0		#最高涨幅
	s_low_df = 0		#最低跌幅
	s_cx_yzzt = 0		#次新YZZT
	s_open_dt_dk = 0	#开盘跌停打开
	s_new = 0			#上市新股
	s_total = 0			#总计所有交易票
	s_sw_zt = 0			#上午ZT
	s_xw_zt = 0			#下午ZT
	lst_kd = []			#坑爹个股
	lst_nb = []			#NB，低位强拉高位
	lst_jc = []			#韭菜了，严重坑人
	lst_non_yzcx_zt = []		#非次新涨停
	lst_non_yzcx_yzzt = []		#非次新一字涨停
	lst_non_yzcx_zthl = []		#非次新涨停回落
	lst_dt = []					#跌停
	lst_yzdt = []				#YZ跌停
	lst_dtft = []				#跌停反弹
	lst_kbcx = []				#开板次新
	def __init__(self):
		self.s_zt = 0
		self.s_dt = 0
		self.s_zthl = 0
		self.s_dtft = 0
		self.s_yzzt = 0
		self.s_yzdt = 0
		self.s_cxzt = 0
		self.s_cxdt = 0
		self.s_open_zt = 0
		self.s_close_zt = 0
		self.s_open_T_zt = 0
		self.s_zt_o_gt_c = 0
		self.s_dk_zt = 0
		self.s_open_dt = 0
		self.s_st_yzzt = 0
		self.s_st_yzdt = 0
		self.s_open_sz = 0
		self.s_open_xd = 0
		self.s_open_pp = 0
		self.s_open_dz = 0
		self.s_open_dd = 0
		self.s_close_sz = 0
		self.s_close_xd = 0
		self.s_close_pp = 0
		self.s_close_dz = 0
		self.s_close_dd = 0
		self.s_high_zf = 0
		self.s_low_df = 0
		self.s_cx_yzzt = 0
		self.s_open_dt_dk = 0
		self.s_new = 0
		self.s_total = 0
		self.s_sw_zt = 0
		self.s_xw_zt = 0
		self.lst_kd = []
		self.lst_nb = []
		self.lst_jc = []
		self.lst_non_yzcx_zt = []
		self.lst_non_yzcx_yzzt = []
		self.lst_non_yzcx_zthl = []
		self.lst_dt = []
		self.lst_yzdt = []
		self.lst_dtft = []
		self.lst_kbcx = []

