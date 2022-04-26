#-- coding:UTF-8 --
#!/usr/bin/env python

import Tkinter as tk
 
root = tk.Tk()

tk.Label(root, text="Red", bg="red", fg="white").pack(side="left")
tk.Label(root, text="Green", bg="green", fg="black").pack(side="left")
tk.Label(root, text="Blue", bg="blue", fg="white").pack(side="left")
 
root.mainloop()