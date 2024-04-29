# coding=utf-8
import datetime
import decimal
import json
import traceback

import pandas
import pymysql
import redis
import xlrd
from rediscluster import RedisCluster


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


# 通过SQL获取mia库数据
def get_mia_db_data(sql, db_name="mia_mirror"):
    cur = get_mia_cursor(db_name)
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return rows


# 通过SQL获取测试库数据
def get_mia_test_cursor(db_name="mia_test2"):
    conn = pymysql.connect(host="172.16.130.253",
                           port=3308,
                           user="write_user",
                           passwd="write_pwd",
                           db=db_name,
                           charset="utf8")
    return conn.cursor()


def get_test_db_data(sql, db_name="mia_test2"):
    cur = get_mia_test_cursor(db_name)
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return rows


def get_cctd_cursor(db_name="java_boot_test"):
    conn = pymysql.connect(host="192.168.10.225",
                           port=3306,
                           user="root",
                           passwd="123456",
                           db=db_name,
                           charset="utf8")
    return conn.cursor()


# 通过SQL获取mia库数据
def get_cctd_db_data(sql, db_name="java_boot_test"):
    cur = get_cctd_cursor(db_name)
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return rows


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


# 获取测试环境redis集群client
def get_test_cluster_client():
    redis_nodes = [
        {'host': '172.16.130.100', 'port': 7001},
        {'host': '172.16.130.100', 'port': 7002},
        {'host': '172.16.130.100', 'port': 7003},
        {'host': '172.16.130.100', 'port': 7004},
        {'host': '172.16.130.100', 'port': 7005},
        {'host': '172.16.130.100', 'port': 7006}

    ]

    return RedisCluster(startup_nodes=redis_nodes, decode_responses=True)


# 获取线上库存redis集群client
def get_stock_cluster_client():
    redis_nodes = [
        {'host': '10.5.96.169', 'port': 7012},
        {'host': '10.5.96.174', 'port': 7012},
        {'host': '10.5.96.181', 'port': 7012},
        {'host': '10.5.96.228', 'port': 7024},
        {'host': '10.5.97.18', 'port': 7024},
        {'host': '10.5.96.169', 'port': 7013}
    ]

    return RedisCluster(startup_nodes=redis_nodes, decode_responses=True)


def get_single_redis_client(host="10.5.111.125"):
    return redis.StrictRedis(host=host, port=6379, db=0)


def read_sql_file(path):
    sql = ""
    with open(path, 'r', encoding="utf8") as file:

        line = file.readline()
        while line:
            line = line.strip('\n')
            if line.find("--") > -1 or len(line) < 1:
                line = file.readline()
                continue

            sql += line + " "
            line = file.readline()
    file.close()

    return sql


# 通用sql数据导出excel
def export_sql_excel(sql_path, excel_path):
    sql = read_sql_file(sql_path)
    print(sql)
    data_list = get_mia_db_data(sql, "mia")
    df = pandas.DataFrame(data_list)
    df.to_excel(excel_path, index=False)
