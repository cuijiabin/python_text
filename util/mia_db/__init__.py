# coding=utf-8
import util as bm


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
    sql = "select column_name,column_comment,data_type from information_schema.columns where table_name = '" + db_table + "'"
    db_cursor.execute(sql)
    column_data = db_cursor.fetchall()
    return list(map(lambda x: x[0] + "\t" + x[2] + "\t" + x[1], column_data))


def get_columns_name(db_table, db_cursor):
    sql = "select column_name from information_schema.columns where table_name = '" + db_table + "'"
    db_cursor.execute(sql)
    column_data = db_cursor.fetchall()
    return list(map(lambda x: x[0], column_data))


def get_sql_param(table_name, field, param):
    sql = "SELECT * FROM " + table_name + " WHERE " + field + " IN (%s)"
    condition = ", ".join(list(map(lambda x: "%s", param)))
    sql %= condition
    return sql


def get_db_group_info(table_name, field, param):
    cur = bm.get_mia_cursor("db_pop")
    sql = get_sql_param(table_name, field, param)
    cur.execute(sql, param)
    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    return rows


def get_mia_group_info(table_name, field, param):
    cur = bm.get_mia_cursor("mia_mirror")
    sql = get_sql_param(table_name, field, param)
    cur.execute(sql, param)
    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    return rows
