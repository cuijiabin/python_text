# coding=utf-8
import common_build_model as bm
import pymysql
import xlrd

"""
1.引用之前默写的各种小的工具类 主要就是文件名称 build_model 但是目前IDE是有这个bug的
2.主要的Excel处理工具

return_items
new_refund_request
3.问题：特殊类型字段的处理 写入新的Excel？
a.数字类型的变量 最后补充了一个0 这个要如何来处理？
b.对于日期类型的变量要怎么来处理呢？[2种方式]
xlrd.xldate_as_tuple(table.cell(2,2).value, 0)   #转化为元组形式
xlrd.xldate.xldate_as_datetime(table.cell(2,2).value, 1)   #直接转化为datetime对象

下一步问题的处理 关于excel的写入的各种问题
"""


# 打开excel文件
def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except FileNotFoundError:
        print("文件%s 不存在" % file)
        return None
    except Exception as e:
        print("str(Exception):\t", str(Exception))
        print("str(e):\t\t", str(e))
        print("repr(e):\t", repr(e))
        print("e.message:\t", e.message)
        print("traceback.print_exc():\t", traceback.print_exc())
        print("traceback.format_exc():\n%s" % traceback.format_exc())


# 遍历读取Excel内容
def read_excel(file_path, idx=0, assign=[], pre_num=0):
    data = open_excel(file_path)
    if data is None:
        return
    sheets = data.sheets()[idx]
    row_num = sheets.nrows
    col_num = sheets.ncols
    if pre_num > 0:
        row_num = pre_num
    for i in range(0, row_num):
        row_value = sheets.row_values(i)
        if assign is not None and len(assign) > 0:
            for j in assign:
                cell_value = int(row_value[j]) if type(row_value[j]) is float else row_value[j]
                print(cell_value, end=" ")
        else:
            for j in range(0, col_num):
                print(row_value[j], end=" ")

        print("\n")


# 读取excel列表
def read_excel_array(file_path, idx=0, frx=0, assign=["id","fi","se"], pre_num=0):
    data = open_excel(file_path)
    if data is None:
        return
    sheets = data.sheets()[idx]
    row_num = sheets.nrows
    col_num = sheets.ncols
    if pre_num > 0:
        row_num = pre_num

    result = []
    for i in range(frx, row_num):
        row_value = sheets.row_values(i)
        tu = {}
        for j in range(0, col_num):
            # print(row_value[j], end=" ")
            tu[assign[j]] = row_value[j]
        result.append(tu)

    return result

if __name__ == "__main__":
    # cursor = bm.get_mia_cursor()
    # columns = bm.get_columns("item_taxnumber_map", cursor)
    # for table in columns:
    #     print(table)

    read_excel("C:/Users/cuijiabin/Desktopdemo.xlsx", 0, [6], 10)
