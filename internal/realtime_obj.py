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
	s_open_zt = 0		#��ͣ����
	s_close_zt = 0		#��ͣ���̸�����������ͣ
	s_open_T_zt = 0		#��ͣ���̸�����������ͣ����һ��
	s_zt_o_gt_c = 0		#������ͣ,���̼۸������̼�
	s_dk_zt = 0			#������ͣ�����̴���ͣ
	s_open_dt = 0		#��ͣ����
	s_dt_daoT = 0		#��ͣ���̣���T
	s_st_yzzt = 0
	s_st_yzdt = 0
	s_open_sz = 0		#��������
	s_open_xd = 0		#�����µ�
	s_open_pp = 0		#����ƽ��
	s_open_dz = 0		#���̴���
	s_open_dd = 0		#���̴��
	s_close_sz = 0		#��������
	s_close_xd = 0		#�����µ�
	s_close_pp = 0		#����ƽ��
	s_close_dz = 0		#���̴���
	s_close_dd = 0		#���̴��
	s_high_zf = 0		#����Ƿ�
	s_low_df = 0		#��͵���
	s_cx_yzzt = 0		#����YZZT
	s_open_dt_dk = 0	#���̵�ͣ��
	s_new = 0			#�����¹�
	s_total = 0			#�ܼ����н���Ʊ
	s_sw_zt = 0			#����ZT
	s_xw_zt = 0			#����ZT
	lst_kd = []			#�ӵ�����
	lst_nb = []			#NB����λǿ����λ
	lst_jc = []			#�²��ˣ����ؿ���
	lst_non_yzcx_zt = []		#�Ǵ�����ͣ
	lst_non_yzcx_yzzt = []		#�Ǵ���һ����ͣ
	lst_non_yzcx_zthl = []		#�Ǵ�����ͣ����
	lst_dt = []					#��ͣ
	lst_yzdt = []				#YZ��ͣ
	lst_dtft = []				#��ͣ����
	lst_kbcx = []				#�������
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

