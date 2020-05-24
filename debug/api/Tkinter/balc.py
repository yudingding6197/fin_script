#!/usr/bin/env python
# -*- coding:utf-8 -*-

#-*- coding:utf-8 -*-
from Tkinter import *
import tkMessageBox



def get_Tk():
    top = Tk()
    return top

#定义求总和函数
def sum_test(baseNum,growthRate,time):
    return baseNum * (1+growthRate)**(time)

#定义增长函数
def add_sum (baseNum,growthRate,time):
    return baseNum * (1+growthRate)**(time) - baseNum


#定义第N天增长数函数
def add_num (baseNum,growthRate,time):
    return baseNum *growthRate* (1+growthRate)**(time-1)

def show_result(top,re_sum,re_add,add_Num,times):
    #这里使用Toplevel(top) 是为了新开一个窗口 ，且显示计算结果，如果直接实例化一个窗口，则新窗口不显示结算结果。
    top_show = Toplevel(top)
    top_show.title("计算结果显示")
    top_show.geometry('300x240+810+420')

    addNum = Label(top_show, text='第%d天增长数：' % times)
    addNum.pack()
    num_text = StringVar()
    add_Nums = Entry(top_show, textvariable=num_text,state='readonly')
    num_text.set(add_Num)
    add_Nums.pack()

    # 显示增长数
    add_Sums = Label(top_show, text='%d天增长总数：' % times)
    add_Sums.pack()
    add_text = StringVar()
    adds = Entry(top_show, textvariable=add_text,state='readonly')
    add_text.set(re_add)
    adds.pack()
    # 显示总数
    Sums = Label(top_show, text='%d天后总数：' % times)
    Sums.pack()
    sum_text = StringVar()
    sums = Entry(top_show, textvariable=sum_text,state='readonly')
    sum_text.set(re_sum)
    sums.pack()

    top_show.mainloop()

def on_click(top,base_text,growth_text,time_text):

    #获取输入信息
    if base_text.get().strip() == '':
        tkMessageBox.showinfo(title='基数', message='基数为空，请输入有效的数值！')
    else:
        base_Num = float(base_text.get())

    if growth_text.get().strip() == '':
        tkMessageBox.showinfo(title='增长率', message='增长率为空，请输入有效的数值！')
    else:
        growth_Rate = float(growth_text.get())

    if time_text.get().strip() == '':
        tkMessageBox.showinfo(title='时间', message='时间为空，请输入有效的数值！')
    elif float(time_text.get()) < 1:
        tkMessageBox.showinfo(title='时间', message='时间小于1，请输入大于或等于1的数值！')
    else:
        temp_time = float(time_text.get())
        times = int(temp_time)

    re_sum = sum_test(base_Num, growth_Rate, times)
    # 四舍五入保留小数点后两位
    re_sum = round(re_sum, 2)
    # print type(re_sum)
    re_add = add_sum(base_Num, growth_Rate, times)
    # 四舍五入保留小数点后两位
    re_add = round(re_add, 2)

    add_Num = add_num(base_Num, growth_Rate, times)
    add_Num = round(add_Num, 2)

    show_result(top,re_sum,re_add,add_Num,times)

def put_info():
    top = get_Tk()
    #top.minsize(100, 100)  # 窗口的最小缩放
    top.title("计算总数量")
    top.geometry('300x240+420+420')


    baseNum = Label(top, text='基数：')
    baseNum.pack()
    base_text = StringVar()
    base = Entry(top, textvariable=base_text)
    base_text.set(" ")
    base.pack()

    growthRate = Label(top, text='增长率：')
    growthRate.pack()
    growth_text = StringVar()
    growth = Entry(top, textvariable=growth_text)
    growth_text.set('0.0115')
    growth.pack()

    useTime = Label(top, text='时间（天）：')
    useTime.pack()
    time_text = StringVar()
    times = Entry(top, textvariable=time_text)
    time_text.set(" ")
    times.pack()

    Button(top, text="计算", command= lambda:on_click(top,base_text,growth_text,time_text)).pack()
    top.mainloop()

   # 这种 直接command = 方法名的方式，函数是不能传递参数的，所以为了能传递参数使用了上面的方法。
   # Button(top, text="计算", command= on_click).pack()

if __name__ == '__main__':
    put_info()