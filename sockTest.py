#!/usr/bin/env python
# -*- coding:utf8 -*-

import sys
import socket

sk=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ('192.168.10.2',21)

sk.connect(address)

data = sk.recv(1024)
print(data)

#print(str(data,'utf8'))
