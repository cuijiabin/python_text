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

"""
对文办进行统计计数与排序
"""


def dump():
    a = []
    dt = {}
    with open("F:/File/download/tmp.txt", encoding="utf8") as f:
        line = f.readline()
        while line:
            line = line.strip('\n')
            if len(line) > 0:
                a.append(line)
            line = f.readline()
        f.close()

    for key in a:
        dt[key] = dt.get(key, 0) + 1

    # 按value值排序
    dt = sorted(dt.items(), key=lambda item: item[1], reverse=True)
    for v in dt:
        print(v[0], " ", v[1])


if __name__ == '__main__':
    # print("cuijiabin".startswith("cui"))
    # print("cuijiabin".startswith("ui"))
    dump()
