# coding=utf-8
import datetime
import random
import time

# import pandas as pd

# 日期转换工具
import numpy

ISFORMAT = "%Y-%m-%d %H:%M:%S"


# 毫秒转化成为年月日
def convert_mill(mill_second):
    print(mill_second, "毫秒转换后", time.strftime(ISFORMAT, time.localtime(mill_second / 1000)))


def convert_second(mill_second):
    print(mill_second, "毫秒转换后", time.strftime(ISFORMAT, time.localtime(mill_second)))


# 字符串转化成为毫秒
def convert_str_mill(date_str, format="%Y-%m-%d %H:%M:%S"):
    struct_time = time.strptime(date_str, format)
    mk_time = time.mktime(struct_time)
    print(date_str, "转换后毫秒数:" + str(int(1000 * mk_time)))


def convert_str_second(date_str, format="%Y-%m-%d %H:%M:%S"):
    struct_time = time.strptime(date_str, format)
    mk_time = time.mktime(struct_time)
    print(date_str, "转换后毫秒数:" + str(int(mk_time)))


# def datelist(beginDate, endDate):
#     # beginDate, endDate是形如‘20160601’的字符串或datetime格式
#     date_l = [datetime.strftime(x, '%Y-%m-%d') for x in list(pd.date_range(start=beginDate, end=endDate))]
#     return date_l

def get_day_nday_ago(date, n):
    t = time.strptime(date, "%Y-%m-%d")
    y, m, d = t[0:3]
    Date = str(datetime.datetime(y, m, d) - datetime.timedelta(n)).split()
    return Date[0]


def fib(n):
    return (4 << n * (3 + n)) // ((4 << 2 * n) - (2 << n) - 1) & ((2 << n) - 1)


def fib_recursive(n):
    if n < 2: return 1
    return fib_recursive(n - 1) + fib_recursive(n - 2)


def fib_iter(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = a + b, a
    return b


def fib_matpow(n):
    m = numpy.matrix('1 1 ; 1 0') ** n
    return m.item(0)


def get_every_day(begin_date_str, end_date_str):
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date_str, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list


if __name__ == "__main__":
    convert_second(1641042002)
    # convert_second(1706077352389)
    # convert_mill(1627747199000)
    convert_mill(1706148465678)
    convert_mill(1584028800000)
    convert_str_second("2022-01-04 13:00:00")
    convert_str_mill("2020-03-13", "%Y-%m-%d")
    # for i in range(143, 1428):
    #     print(i, 7 * i)

    print(time.time())
    print(time.time() * 1000)
    print(round(time.time() * 1000))
    # print(get_day_nday_ago('2017-02-11', 7))
    # for i in range(1, 10):
    #     print(i, fib_matpow(i))
    # 生成随机数 0 或 1，并保留一位小数
    random_number = round(random.random() * 10) / 10
    print(random_number)
    random_number = round(random.choice([0.0, 1.0]), 1)
    print(random_number)
    # print(str(round(random.random() * 10) / 10))
    data = get_every_day("2020-01-01", "2020-08-10")
    for d in data:
        print(d)
