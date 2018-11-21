# coding=utf-8
import datetime
import decimal
import json

import pymysql


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
    conn = pymysql.connect(host="10.1.3.33",
                           port=3306,
                           user="pop_cuijiabin",
                           passwd="8dtx5EOUZASc#",
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
