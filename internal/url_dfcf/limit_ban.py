#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import zlib
import urllib2

from internal.format_parse import *

'''
GET /EM_UBG_PDTI_Fast/api/js?id=0007962&TYPE=k&js=fsData1515847425760((x))&rtntype=1&isCR=true&authorityType=fa HTTP/1.1
Host: pdfm2.eastmoney.com
Connection: keep-alive
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,la;q=0.8
Cookie: em_hq_fls=js; em-quote-version=topspeed; intellpositionL=1079.19px; ct=sF121Gt_UoB_mn_Ipac5WXwrMDxfeWwD_00xm2Bqw7QXdGp6uQZQNAeEnFNS_ry1sxddo34Y_2qqfBtjJwcRrxxJkeQ6C2u10KQ0jG_C7DkG3KNasRshVHRUr7CncuLJDEApRhF-IhWNN8ap3dXvQQDeMKvsj70By6cRHrlfkq4; ut=FobyicMgeV5yNnZj1TOuTm9_7Mepp4C_44WD9HUBbsjB7uNlFulhxfzRm7oF2F64T_Eu9FDAmEWdnJsjOblf-7aLN89B9cOTLVelejWSusFfB-7-aE1b-FfIX4KaMYarOaDVld5f7HYFWw3xB5fl-6ZeM-iNjJigbryqlYjeKid3AYoHYciT5WJDQ_6iOvY7anprRfw3SpyjgCLxU7z5x51DL1Z0i1gt0--yjtxN421kKMjmsi-Wjb8XPUHLkwoPQiwRr5UBNhQ_YWVYpKdLAhEsSF15UdEz; pi=6100112247957528%3byudingding6197%3bgoutou%3b8SCe%2fTdcEIvLHHG1ut8543KmvrlIdzNC1ql6SrveLwxLlAYq9U3Mfj7AlA38SZ%2flYd2FWs%2bvMbdsOSVMXWVBgV4Vgl6fRSVaWvO7m2slXOhH03FqjhPaXyPwjbAmitjq4I1%2bC3%2b%2fXUjSSQKzS2SU5J6Oc7fyMPW2cwwXVsh1Na25m1HQDLiCNtXWL9f1yNTRcVzfS%2fw3%3bu00XyVpwDfkgmlWZK3vXnv8iygIu9XCOtBWLlUnUCu8ddeaGUPieVV3%2bR%2bjTGrrTaCcmumPDyWcBeGgXI2qiz34Ws2XBijkhGZ7sZQGbn0%2f5X5CdANFYhMMC378csEAl1ZpdOHIQJA7hPxio63a30b%2bz%2fZLD5Q%3d%3d; uidal=6100112247957528goutou; sid=4725419; vtpst=|; emshistory=%5B%22%E7%9C%81%E5%B9%BF%E9%9B%86%E5%9B%A2%22%2C%22skgf%22%2C%22shenguang%22%2C%22sggf%22%2C%22%E6%96%B0%E6%97%B6%E8%BE%BE%22%5D; intellpositionT=755px; emhq_picfq=1; HAList=a-sz-300849-N%u9526%u76DB%2Ca-sz-300291-%u534E%u5F55%u767E%u7EB3%2Ca-sz-300847-N%u4E2D%u8239%2Ca-sz-300831-%u6D3E%u745E%u80A1%u4EFD%2Ca-sh-600145-*ST%u65B0%u4EBF%2Ca-sz-000587-*ST%u91D1%u6D32%2Ca-sz-300830-%u91D1%u73B0%u4EE3%2Ca-sz-002400-%u7701%u5E7F%u96C6%u56E2%2Ca-sz-000931-%u4E2D%20%u5173%20%u6751%2Ca-sh-600000-%u6D66%u53D1%u94F6%u884C%2Ca-sh-603005-%u6676%u65B9%u79D1%u6280%2Ca-sh-605168-%u4E09%u4EBA%u884C; qgqp_b_id=1c2144bf8702d18e07410b7ba519d379; waptgshowtime=2020712; st_pvi=50425195960510; st_sp=2020-06-10%2023%3A44%3A15; st_inirUrl=http%3A%2F%2Fdata.eastmoney.com%2Fkzz%2Fdefault.html
'''

urlfmt = 'http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=%s&TYPE=k&js=%s((x))&rtntype=%d&isCR=true&authorityType=fa'
#'Referer': http://quote.eastmoney.com/chart/h5.html?id=0005202&type=k
send_headers = {
'Host': 'pdfm2.eastmoney.com',
#'Connection': 'keep-alive',
'Cache-Control': 'max-age=0',
#'Upgrade-Insecure-Requests': 1,
'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
'Accept': '*/*',
'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
'Accept-Encoding': 'gzip, deflate',
'Cookie': 'st_pvi=65131814925934; em_hq_fls=js; emhq_stock=300379%2C510300%2C300059; \
ct=gSzyZYX428bqF8KFmsvff_vR0WGKJAA0miUW7eR26gofMoK0iklrNPydT7ek5CAYmhkuwM3wbZOI2ZpFPAoWJelbJErRFVm7cCuHKYCtEJprcFnO6Q8wbTA_3JtbNlgYgCT2__I5z8tzKkfVANJw1xeOMTqksUHhEHm5G40vJ_E \
ut=FobyicMgeV7CWBTmL9Bu1obPhorDA1HbLw1lQWu36v9QOPj992o3gmSvzNX--G0lXhxZqa2MTa_B9Do2KSntZC_ssXb_gCrvSlax_wBf65973PgGLaxGqrqIXmGZFpMqsWk0SUMlQOCNdAg5wVaGd2GzdasuwK_fdFGtI9iJzvtEFnDsNVI5TGTtSqkoYM-oSZn1cY-cKZKPFHub6Gy75x68Dx1tTm5h7LywruhRDToUGB1laoHZIAJbVfqqyUI1RfICpFEaILg5jMTa9eNJPTOGX1YmEYHM; \
pi=6100112247957528%3byudingding6197%3bgoutou%3b0cW4DqnbVJoMdu1MZiropTm6BV1XLj16XsvJO70kiLEUyKsPMgichDgFLNQAsInwhJERWZz7yHcS7O7W3ZL2dcjA3%2fmZ3C5963s%2bDmkHccsL6pryylhnTIMnse5nSBAA9u4HViDawKBE2J1H99l9hN9FV2EDvHkoUmqLb6Yyf09WAifb%2bdYj9kNpyqiJziuNO7OTlZ8N%3bvNvIvbNvs29ty0dGWHDrlmY9DQZgV43TfP00Z0d5NjJm2tRrZqJ0843uLtzmM0c1G%2fs%2f3JarUusrH2NZdgcxiqLEIitAnfBpEb68QjYndEfZINJ%2bM1Pkry%2fnzvKD6XsX7nSGNF5EmGXIR23aUOrXivsh0bSqVQ%3d%3d; \
uidal=6100112247957528goutou; sid=4725419; vtpst=|; qgqp_b_id=3351a1846039a4841a7ac4edce9be185; st_si=57858667318678; \
HAList=a-sz-300059-%u4E1C%u65B9%u8D22%u5BCC%2Ca-sz-002252-%u4E0A%u6D77%u83B1%u58EB%2Ca-sz-300401-%u82B1%u56ED%u751F%u7269%2Ca-sh-600908-%u65E0%u9521%u94F6%u884C%2Ca-sz-002527-%u65B0%u65F6%u8FBE%2Ca-sh-600696-ST%u5339%u51F8%2Ca-sh-603618-%u676D%u7535%u80A1%u4EFD%2Ca-sz-300291-%u534E%u5F55%u767E%u7EB3%2Ca-sz-002815-%u5D07%u8FBE%u6280%u672F%2Ca-sh-603156-%u517B%u5143%u996E%u54C1%2Ca-sh-600845-%u5B9D%u4FE1%u8F6F%u4EF6; \
st_sn=1; st_psi=20180421183808157-117005300001-2337497230; st_asi=delete; EMSTtokenId=3bbbf98339c2b81dc9c8a173b9a51c54',
'DNT': 1
}
'''
'Cookie': 'st_pvi=97140791819816; emstat_bc_emcount=24578815992596371324; emstat_ss_emcount=0_1515626347_1914456706; \
em_hq_fls=old; _ga=GA1.2.1371087654.1472141391; Hm_lvt_557fb74c38569c2da66471446bbaea3f=1506330203; qgqp_b_id=867a67ca83c13fbd622d079314b267df; \
ct=tTNAoSxXA4HgHmLlK58m5dvCXLfX46zX2EhPxEC0Mp9KXne6YtatYD6Zc0kmqHFH9fEfxnQyVM3cy4d5hDSq4xaCuyjCtoat4MAwVJeFCgQ4jH3xU77tzv2BnAs_YtDRJ5YbPVra0XcbM0-zTxO2seQHPw9FjR4vaKjkGFEoupI; \
uidal=6100112247957528goutou; vtpst=|; emshistory=%5B%22%E4%BF%9D%E5%8D%83%E9%87%8C%E5%80%BA%E5%88%B8%22%5D; st_si=56676665040049',
'''
def get_zdting_by_dc(code, jstr, rtntype):
	res_data = None
	excecount=0

	ret, ncode = parseCode(code, 'dc')
	if ret!=0:
		exit(-1);

	urlall = urlfmt %(ncode, jstr, rtntype)
	#print("get_zdting_by_dc", urlall)
	while excecount<=5:
		try:
			req = urllib2.Request(urlall,headers=send_headers)
			res_data = urllib2.urlopen(req, timeout=3)
		except:
			excecount += 1
			continue
		else:
			break

	if res_data is None:
		print("Open URL fail", code, urlall)
		return None

	content1 = res_data.read()
	respInfo = res_data.info()
	if( ("Content-Encoding" in respInfo) and (respInfo['Content-Encoding'] == "gzip")):
		content1 = zlib.decompress(content1, 16+zlib.MAX_WBITS);
	#else:
	#	print "Content not zip"
	res_data.close()

	content = content1.decode('utf8')
	if content[-1]==")":
		content = content[:-1]
	
	return content
	
if __name__=="__main__":
	rtntype = 1
	jstr = 'fsData1515847425760'
	get_zdting_by_dc('000796', jstr, rtntype)
	
	