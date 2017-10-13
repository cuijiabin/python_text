# coding=utf-8
import pymysql

"""
1.获取table名称
2.根据table名称 获取 字段信息
3.根据栏目信息进行 其他处理
"""


# 获取数据库游标
def get_mia_cursor(db_name="mia_mirror"):
    conn = pymysql.connect(host="10.1.3.33", port=3306, user="pop_cuijiabin", passwd="8dtx5EOUZASc", db=db_name,
                           charset="utf8")
    return conn.cursor()


# 获取数据库表
def get_table_list(table_name, db_cursor):
    sql = "show tables"
    if table_name.strip() != "":
        sql += " like \'%" + table_name + "%\'"
    db_cursor.execute(sql)
    data = db_cursor.fetchall()
    return list(map(lambda x: x[0], data))


# 获取表字段信息
def get_columns(db_table, db_cursor):
    sql = "select column_name,column_comment from information_schema.columns where table_name = '" + db_table + "'"
    db_cursor.execute(sql)
    column_data = db_cursor.fetchall()
    return list(map(lambda x: x[0] + "\t" + x[1], column_data))


if __name__ == "__main__":
    cursor = get_mia_cursor("db_pop")
    tables = get_table_list("item", cursor)
    for tb in tables:
        columns = get_columns(tb, cursor)
        has = False
        for table in columns:
            if "url" in table:
                has = True

        if has:
            print("======================"+tb)
            for table in columns:
                print(table)

            print("======================")
