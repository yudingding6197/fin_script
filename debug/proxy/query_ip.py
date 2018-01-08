# -*- coding=utf-8 -*-
#__author__:Mr丶zhang
import urllib2
import requests
from lxml import etree

proxy={'http':'112.95.107.249:8118'}
test_url="http://ip.filefab.com/index.php"
#test_url="http://ip.catr.cn/"
 
resp=urllib2.urlopen(test_url).read()
response = etree.HTML(resp)
ip_addr = response.xpath('//div/h1[@id="ipd"]/span/text()')
print "Before switching the IP address:",ip_addr
#使用代理IP地址之前的访问IP地址

try:
    response = requests.get(test_url,proxies = proxy)
    response = etree.HTML(resp)
    ip_addr = response.xpath('//div/h1[@id="ipd"]/span/text()')
    print "Now the IP ADDRESS IS:",ip_addr
    #使用代理IP地址之后的访问IP地址
except Exception:
    print "The IP Address is Useless" #代理IP不可用