#!/usr/bin/env python
# -*- coding:utf8 -*-
import os
import requests as rq

#ts.get_today_all()

r =rq.get("http://www.baidu.com")
#r =rq.head("http://www.baidu.com")
#payload = {'key1':'val1', 'key2':'val2'}
#r =rq.post("http://www.baidu.com", data=payload)
#r =rq.put("http://www.baidu.com")
#r =rq.patch("http://www.baidu.com")
print r.status_code
print r.encoding
print r.apparent_encoding
print r.headers
enc = rq.utils.get_encodings_from_content(r.content)
print enc

#2种输出内容方式 r.content and r.text
print r.content.decode(enc[0])

r.encoding = enc[0]
print r.text
