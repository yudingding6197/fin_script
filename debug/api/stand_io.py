#!/usr/bin/env python
# -*- coding:gbk -*-
import sys


class Logger_IO(object): 
	def __init__(self, filename="Default.log"):
		self.terminal = sys.stdout
		self.log = open(filename, "a")

	def write(self, message):
		self.terminal.write(message)
		self.log.write(message)

	def flush(self):
		self.log.flush()
		pass


sys.stdout = Logger_IO("yourlogfilename.txt")
print("Hello world !") # this is should be saved in yourlogfilename.txt
sys.stdout.flush()

print "AAAA"
