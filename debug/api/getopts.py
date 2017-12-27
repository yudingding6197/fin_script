#!/usr/bin/env python
# -*- coding:utf8 -*-
#import re
import sys
import getopt

# 执行命令的时候跟随不同参数：
# --input=c:\temp\aa -o c:\temp\output -d
# --input=c:\temp\aa -o c:\temp\output -ds

#短参数,仅仅包含'-'
#参数是 '-d 2.3',需要包含':', 写为'd:'
#参数是 '-a', 不要包含':', 写为'a'
short_args = '-ac -b boy -d 2.3 unkown'.split()
optlist, args = getopt.getopt(short_args, 'acb:d:')
print '=======short -'
print optlist
print args
print ''

#长参数,带有 '--'
long_args = '--a=123 --b unkown p1 p2'.split()
optlist, args = getopt.getopt(long_args, '', ['a=', 'b'])
print '=======long --'
print optlist
print args
print ''

#长短混合包含
print '=======mix -- and -'
s = '--condition=foo --testing --output-file abc.def -x a1 unknown'
args = s.split()
optlist, args = getopt.getopt(args, 'x:', ['condition=', 'output-file=', 'testing'])
print optlist
print args
print ''

# 执行命令的时候跟随： --input=c:\temp\aa -o c:\temp\output -d

config = {
  "input":"",
  "output":".",
  "show":0
}

#getopt三个选项，第一个一般为sys.argv[1:],第二个参数为短参数，如果参数后面必须跟值，须加:，第三个参数为长参数 
#是一个列表， 
opts, args = getopt.getopt(sys.argv[1:], 'hi:o:ds',
   [ 
    'input=',  
    'output=',  
    'help'
    ] 
   ) 
  
#参数的解析过程,长参数为--，短参数为- 
for option, value in opts:
  #print "@@@@@"
  print option, value
  if option in ["-h","--help"]: 
    print """ 
    usage:%s --input=[value] --output=[value] 
    usage:%s -input value -o value 
    """
  elif option in ['--input', '-i']: 
    config["input"] = value 
  elif option in ['--output', '-o']: 
    config["output"] = value 
  elif option == "-s":
    config["show"] = 1 
  elif option == "-d": 
    print "usage -d"

print config
if config["show"]==0:
	print "Show is 0"
elif config["show"]==1:
	print "Show is 1"
'''

'''
