#-- coding:UTF-8 --
#!/usr/bin/env python

import Tkinter as tk
 
root = tk.Tk()
# fill 选项是告诉窗口管理器该组件将填充整个分配给它的空间，"both" 表示同时横向和纵向扩展，"x" 表示横向，"y" 表示纵向
# expand 选项是告诉窗口管理器将父组件的额外空间也填满。
listbox = tk.Listbox(root)
listbox.pack(fill="both", expand=True)
 
for i in range(10):
	listbox.insert("end", str(i))

root.mainloop()