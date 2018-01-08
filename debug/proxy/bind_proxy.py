#!/usr/bin/env python
# -*- coding:gbk -*-

import sys
import re
import os
import datetime
import tushare as ts
#from internal.common import *
#from internal.ts_common import *
import urllib2, httplib, socket

class BindableHTTPConnection(httplib.HTTPConnection):
    def connect(self):
        """Connect to the host and port specified in __init__."""
        self.sock = socket.socket()
        self.sock.bind((self.source_ip, 0))
        if isinstance(self.timeout, float):
            self.sock.settimeout(self.timeout)
        self.sock.connect((self.host,self.port))

def BindableHTTPConnectionFactory(source_ip):
    def _get(host, port=None, strict=None, timeout=0):
        bhc=BindableHTTPConnection(host, port=port, strict=strict, timeout=timeout)
        bhc.source_ip=source_ip
        return bhc
    return _get

class BindableHTTPHandler(urllib2.HTTPHandler):
    def http_open(self, req):
        return self.do_open(BindableHTTPConnectionFactory('61.135.217.7'), req)

opener = urllib2.build_opener(BindableHTTPHandler)
opener.open("http://www.baidu.com/").read() 
# Will fail, 127.0.0.1 can't reach outofmemory.cn


