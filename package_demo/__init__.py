# coding=utf-8
import pymysql

"""
1.__init__.py的在文件夹中，可以使文件夹变为一个python模块，python的每个模块对应的包中都有一个__init__.py文件的存在

2.通常__init__.py文件为空，但是我们还可以为它增加其他的功能，我们在导入一个模块时候（也叫包），实际上导入的是这个模块的__init__.py文件。我们可以在__init__.py导入我们需要的模块，不需要一个个导入

3._init__.py 中还有一个重要的变量，叫做 __all__。我们有时会使出一招“全部导入”，也就是这样：from PackageName import *，这时 import 就会把注册在包 __init__.py 文件中 
__all__ 列表中的子模块和子包导入到当前作用域中来。比如：

#文件 __init__.py

__all__ = ["Module1", "Module2", "subPackage1", "subPackage2"]

"""


def hi():
    print("hi")


def get_mia_cursor(db_name="mia_mirror"):
    conn = pymysql.connect(host="10.1.3.33",
                           port=3306,
                           user="pop_cuijiabin",
                           passwd="8dtx5EOUZASc#",
                           db=db_name,
                           charset="utf8")
    return conn.cursor()
