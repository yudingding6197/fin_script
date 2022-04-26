#-- coding:UTF-8 --
#!/usr/bin/env python

import Tkinter as tk
from Tkinter import *
root = Tk()
# 改变root的大小为200x150
# root.geometry('200x150+0+0')
print root.pack_slaves()
# 创建三个Label分别使用不同的fill属性,改为水平放置
# 将第一个LabelFrame居左放置
L1 = LabelFrame(root,text = 'pack1',bg = 'red')
# 设置ipadx属性为20
L1.pack(side = LEFT,ipadx = 20)
Label(L1,
 
    text = 'inside',
      bg = 'blue'
      ).pack(expand = 1,side = LEFT)
Label(L1,
 
    text = 'inside',
      bg = 'blue'
      ).pack(expand = 1,side = RIGHT)
L2 = Label(root,
           text = 'pack2',
           bg = 'blue'
           ).pack(fill = BOTH,expand = 1,side = LEFT,padx = 10)
L3 = Label(root,
           text = 'pack3',
           bg = 'green'
           ).pack(fill = X,expand = 0,side = LEFT,pady = 10)
print root.pack_slaves()

root.mainloop()