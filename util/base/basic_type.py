# coding=utf-8
"""
1.python 中有多少种类型？

解压序列赋值给多个变量
x,y,z = p

record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
name, email, *phone_numbers = record

本节内容主要研究字符串还有文本！

"""

"""
1. 使用多个界定符分割字符串
string 对象的 split() 方法只适应于非常简单的字符串分割情形
2.字符串开头或结尾匹配
str.startswith() 或者是 str.endswith()
3.用Shell通配符匹配字符串
fnmatch 模块提供了两个函数—— fnmatch() 和 fnmatchcase()
"""

if __name__ == '__main__':
    print("cuijiabin".startswith("cui"))
    print("cuijiabin".startswith("ui"))
