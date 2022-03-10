# coding=utf-8
import datetime
import decimal
import json
import traceback

import pymysql
import xlrd


class ExtendJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")

        return super(ExtendJSONEncoder, self).default(obj)


def get_mia_cursor(db_name="mia_mirror"):
    conn = pymysql.connect(host="10.5.96.80",
                           port=3306,
                           user="pop_cuijiabin",
                           passwd="8dtx5EOUZASc#",
                           db=db_name,
                           charset="utf8")
    return conn.cursor()


def get_log_cursor(db_name="log"):
    conn = pymysql.connect(host="10.1.103.19",
                           port=3306,
                           user="pop_cuijiabin",
                           passwd="8dtx5EOUZASc#",
                           db=db_name,
                           charset="utf8")
    return conn.cursor()


def get_mia_test_cursor(db_name="mia_test2"):
    conn = pymysql.connect(host="172.16.130.253",
                           port=3308,
                           user="write_user",
                           passwd="write_pwd",
                           db=db_name,
                           charset="utf8")
    return conn.cursor()


# 小驼峰转大驼峰
def camel_convert(input_string, space_character):
    input_list = str(input_string).split(space_character)
    first = input_list[0].lower()
    others = input_list[1:]

    others_capital = [word.capitalize() for word in others]
    others_capital[0:0] = [first]
    hump_string = ''.join(others_capital)

    return hump_string


# 字典数据生成sql
def gen_sql(tb_name, tb_data):
    ls = [(k, tb_data[k]) for k in tb_data if tb_data[k]]
    sentence = 'INSERT %s (' % tb_name + ','.join([i[0] for i in ls]) + \
               ') VALUES (' + ','.join(['%r' % i[1] for i in ls]) + ');'
    return sentence


# 判断是否为数字
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


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
