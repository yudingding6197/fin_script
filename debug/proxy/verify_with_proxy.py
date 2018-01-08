#!/usr/bin/env python
# -*- coding:gbk -*-

import urllib2
import requests
from lxml import etree
'''
proxy={'http':'120.76.79.21:80'}
test_url="http://ip.filefab.com/index.php" 
 
resp=urllib2.urlopen(test_url).read()
response = etree.HTML(resp)
ip_addr = response.xpath('//div/h1[@id="ipd"]/span/text()')
print "Before switching the IP address:",ip_addr
 
try:
    response = requests.get(test_url,proxies = proxy)
    response = etree.HTML(resp)
    ip_addr = response.xpath('//div/h1[@id="ipd"]/span/text()')
    print "Now the IP ADDRESS IS:",ip_addr
except Exception:
    print "The IP Address is Useless"
'''

'''
# http://ip.catr.cn/

proxies={"http":"114.244.112.220:80"}
proxy_s=urllib2.ProxyHandler(proxies)       
opener=urllib2.build_opener(proxy_s)        
urllib2.install_opener(opener)
'''
#encoding=utf8
import urllib
import socket
socket.setdefaulttimeout(3)
f = open("./proxy/allproxy.txt")
lines = f.readlines()
proxys = []
for i in range(0,len(lines)):
    ip = lines[i].strip("\n").split("\t")
    proxy_host = "http://"+ip[0]+":"+ip[1]
    proxy_temp = {"http":proxy_host}
    proxys.append(proxy_temp)
url = "http://ip.catr.cn/"
for proxy in proxys:
    try:
        res = urllib.urlopen(url,proxies=proxy).read()
        print proxy
    except Exception,e:
        #print proxy
        #print e
        continue
