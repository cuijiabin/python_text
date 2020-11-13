# coding=utf-8
"""
Excel工具类

功能说明：批量开通口碑服务
"""
import xdrlib, sys, re, itertools
import xlrd
import requests
import json
import pymysql


# 打开Excel文件
def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(str(e))


def genetate_blank(num):
    if type(num) != int:
        return "参数错误"
    num = 40 - num
    result = " "
    for i in range(num):
        result += " "
    return result


def analyse_excel(file_path):
    # 1.读取Excel
    data = open_excel(file_path)
    # 2.获取一个工作表
    table = data.sheets()[0]
    # 3.获取行数与列数
    row_num = table.nrows
    col_num = table.ncols
    print("这个工作表的行数是：" + str(row_num) + "；行数是：" + str(col_num))
    # 4.输出栏目信息
    columns = table.row_values(0)
    print(columns)
    rule = re.compile(r'[a-zA-z]')

    tables = []
    for i in range(1, row_num):
        row_value = table.row_values(i)
        blank = genetate_blank(len(row_value[8]))
        result = row_value[8] + blank + rule.sub('', row_value[9])
        tables.append(result.lower())

    tables.sort()
    it = itertools.groupby(tables)
    myfile = open('C:/Users/cuijiabin/Desktop/table.txt', 'a')
    myfile.writelines(file_path.split("/")[-1] + '\n')
    myfile.writelines("======================" + '\n')
    for k, g in it:
        myfile.writelines(k + '\n')

    myfile.close()


if __name__ == "__main__":
    print("hello")
