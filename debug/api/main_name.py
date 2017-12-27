#!/usr/bin/env python
# -*- coding:utf8 -*-
import main_name_obj

'''
__name__ 是python的内置变量
main_name_obj可以作为模块被导入，其它模块可以使用它的方法
虽然我们想使用 main_name_obj.py 下的函数，import的时候代码会运行
所以 "Main_Name_Obj Always be called"将会执行并打印出来，
实际上通常并不希望这句话被打印
通过 ' __name__=="__main__" '条件判断的内部打印语句不会被执行
仅仅在cmd下执行 main_name_obj.py 时才会打印其内部语句
'''

main_name_obj.f1()
pass
