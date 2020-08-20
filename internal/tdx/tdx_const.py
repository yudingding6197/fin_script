#!/usr/bin/python
#-*- encoding: utf8 -*-

DEBUG = True
M_ID = 'ID'    #stkid
M_DT = 'DT'    #datetime
M_OPEN = 'OPEN' 
M_HIGH = 'HIGH' 
M_LOW = 'LOW'
M_CLOSE = 'CLOSE'
M_VOL = 'VOL'
M_AMT = 'AMT' 

# line.dat 一个记录的长度
LINE_LEN = 298


# color 
TDX_WHITE	=	0xFFFFFF
TDX_RED	    =	0xFF0000
TDX_GREEN	=	0x00FF00
TDX_BLUE	=	0x0000FF
TDX_YELLOW	=	0xFFFF00
TDX_BLACK	=	0x000000

color={
	"白色"      :   0xFFFFFF    ,
	"红色" : 0xFF0000    ,
	"绿色" : 0x00FF00    ,
	"蓝色" : 0x0000FF    ,
	"黄色" : 0xFFFF00    ,
	"黑色" : 0x000000    ,
	"牡丹红"	:	0xFF00FF	,
	"青色"	:	0x00FFFF	,
	"海蓝"	:	0x70DB93	,
	"巧克力色"	:	0x5C3317	,
	"蓝紫色"	:	0x9F5F9F	,
	"黄铜色"	:	0xB5A642	,
	"亮金色"	:	0xD9D919	,
	"棕色"	:	0xA67D3D	,
	"青铜色"	:	0x8C7853	,
	"2号青铜色"	:	0xA67D3D	,
	"士官服蓝色"	:	0x5F9F9F	,
	"冷铜色"	:	0xD98719	,
	"铜色"	:	0xB87333	,
	"珊瑚红"	:	0xFF7F00	,
	"紫蓝色"	:	0x42426F	,
	"深棕"	:	0x5C4033	,
	"深绿"	:	0x2F4F2F	,
	"深铜绿色"	:	0x4A766E	,
	"深橄榄绿"	:	0x4F4F2F	,
	"深兰花色"	:	0x9932CD	,
	"深紫色"	:	0x871F78	,
	"深石板蓝"	:	0x6B238E	,
	"深铅灰色"	:	0x2F4F4F	,
	"深棕褐色"	:	0x97694F	,
	"深绿松石色"	:	0x7093DB	,
	"暗木色"	:	0x855E42	,
	"淡灰色"	:	0x545454	,
	"土灰玫瑰红色"	:	0x545454	,
	"长石色"	:	0xD19275	,
	"火砖色"	:	0x8E2323	,
	"森林绿"	:	0x238E23	,
	"金色"	:	0xCD7F32	,
	"鲜黄色"	:	0xDBDB70	,
	"灰色"	:	0xC0C0C0	,
	"铜绿色"	:	0x527F76	,
	"青黄色"	:	0x93DB70	,
	"猎人绿"	:	0x215E21	,
	"印度红"	:	0x4E2F2F	,
	"土黄色"	:	0x9F9F5F	,
	"浅蓝色"	:	0xC0D9D9	,
	"浅灰色"	:	0xA8A8A8	,
	"浅钢蓝色"	:	0x8F8FBD	,
	"浅木色"	:	0xE9C2A6	,
	"石灰绿色"	:	0x32CD32	,
	"桔黄色"	:	0xE47833	,
	"褐红色"	:	0x8E236B	,
	"中海蓝色"	:	0x32CD99	,
	"中蓝色"	:	0x3232CD	,
	"中森林绿"	:	0x6B8E23	,
	"中鲜黄色"	:	0xEAEAAE	,
	"中兰花色"	:	0x9370DB	,
	"中海绿色"	:	0x426F42	,
	"中石板蓝色"	:	0x7F00FF	,
	"中春绿色"	:	0x7FFF00	,
	"中绿松石色"	:	0x70DBDB	,
	"中紫红色"	:	0xDB7093	,
	"中木色"	:	0xA68064	,
	"深藏青色"	:	0x2F2F4F	,
	"海军蓝"	:	0x23238E	,
	"霓虹篮"	:	0x4D4DFF	,
	"霓虹粉红"	:	0xFF6EC7	,
	"新深藏青色"	:	0x00009C	,
	"新棕褐色"	:	0xEBC79E	,
	"暗金黄色"	:	0xCFB53B	,
	"橙色"	:	0xFF7F00	,
	"橙红色"	:	0xFF2400	,
	"淡紫色"	:	0xDB70DB	,
	"浅绿色"	:	0x8FBC8F	,
	"粉红色"	:	0xBC8F8F	,
	"李子色"	:	0xEAADEA	,
	"石英色"	:	0xD9D9F3	,
	"艳蓝色"	:	0x5959AB	,
	"鲑鱼色"	:	0x6F4242	,
	"猩红色"	:	0xBC1717	,
	"海绿色"	:	0x238E68	,
	"半甜巧克力色"	:	0x6B4226	,
	"赭色"	:	0x8E6B23	,
	"银色"	:	0xE6E8FA	,
	"天蓝"	:	0x3299CC	,
	"石板蓝"	:	0x007FFF	,
	"艳粉红色"	:	0xFF1CAE	,
	"春绿色"	:	0x00FF7F	,
	"钢蓝色"	:	0x236B8E	,
	"亮天蓝色"	:	0x38B0DE	,
	"棕褐色"	:	0xDB9370	,
	"紫红色"	:	0xD8BFD8	,
	"石板蓝色"	:	0xADEAEA	,
	"浓深棕色"	:	0x5C4033	,
	"淡浅灰色"	:	0xCDCDCD	,
	"紫罗兰色"	:	0x4F2F4F	,
	"紫罗兰红色"	:	0xCC3299	,
	"麦黄色"	:	0xD8D8BF	,
	"黄绿色"	:	0x99CC32	
        }


market={
        'SH' : 0X01, # 上海
        'SZ' : 0X00  # 深圳
        }

mkt_desc={
        0X01 : 'SH',
        0X00 : 'SZ'
        }

cycle = {
    "日线":0x04 ,        
    "周线":0x05 ,        
    "月线":0x06 ,        
    "一分":0x07 ,        
    "五分":0x00 ,        
    "十五分":0x01 ,        
    "三十分":0x02 ,        
    "六十分":0x03         
        }

cycle_desc = {
    0x04:"日线" ,        
    0x05:"周线" ,        
    0x06:"月线" ,        
    0x07:"一分" ,        
    0x00:"五分" ,        
    0x01:"十五分" ,        
    0x02:"三十分" ,        
    0x03:"六十分"              
        }

line_type = {
    "线段" : 0x0a,        
    "文字" : 0x16,        
    "上箭头" : 0x1a,        
    "下箭头" : 0x0b,        
    "矩形" : 0x17,        
    "平行线" : 0x1d,      
    "定点文字" : 0x25      
        }
type_desc = {
    0x0a:"线段" ,        
    0x16:"文字" ,        
    0x1a:"上箭头"  ,        
    0x0b:"下箭头"  ,        
    0x17:"矩形"  ,        
    0x1d:"平行线" ,                
    0x25:"定点文字"                
        }


if __name__ == '__main__' :
    print 'red color is ',color["红色"]
    print type_desc[0x0a].decode('utf8').encode('gbk')
