#coding:utf-8
'''
Created on Mar 7, 2011
@author: fore
'''
import sys
#import pycurl
import StringIO 
import urllib2 
import urllib3 
def f(url): 
    c = pycurl.Curl() 
    c.setopt(pycurl.URL, url)
    b = StringIO.StringIO() 
    c.setopt(pycurl.WRITEFUNCTION, b.write) 
    c.setopt(pycurl.FOLLOWLOCATION, 1) 
    c.setopt(pycurl.MAXREDIRS, 5) 
    c.perform() 
    return b.getvalue()
 
def l2(url):
    obj = urllib2.urlopen(url).read()
    print(obj)
    #return urllib2.urlopen(url).read()
def l3(url):
    httppool = urllib3.connection_from_url(url)
    response = httppool.request('Get', '/')
    return response.data
#    print ''
 
def funcall(func): 
    import time 
    n = time.time() 
    for i in xrange(1): 
        value = func('http://hq.sinajs.cn/?_=0.7577027725009173&list=sh000001')
#        print '.'
#        print value 
    return time.time() - n
 
#print 'pycurl',  funcall(f) 
print 'urllib3', funcall(l3)
print 'urllib2', funcall(l2)
