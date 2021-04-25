# coding=utf-8
import util as bm
import util.mia_db as mu

"""
1.获取table名称
2.根据table名称 获取 字段信息
3.根据栏目信息进行 其他处理
"""

if __name__ == "__main__":
    cursor = bm.get_mia_test_cursor()
    # tables = mu.get_table_list("order", cursor)
    tables = mu.get_all_table_name("mia_test2", cursor)
    for name in tables:
        columns = mu.get_columns_name(name, cursor)

        # print("表名" + name)
        for c in columns:
            if "channel" in c:
                print("表名" + name + " 字段" + c)

        # print("======================")
