# coding=utf-8

import package_demo

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

if __name__ == '__main__':
    package_demo.hi()

    cursor = package_demo.get_mia_cursor("db_pop")
    tables = get_table_list("item_specification_image_draft", cursor)
    for name in tables:
        columns = get_columns(name, cursor)

        print("表名" + name)
        for c in columns:
            print(c)

        print("======================")
