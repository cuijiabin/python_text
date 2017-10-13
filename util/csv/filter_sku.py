# coding=utf-8
import pymysql
# filterList = []
# with open("E:/work-text/list.txt") as ft:
#     line = ft.readline()
#     while line:
#         line = line.strip('\n')
#         size = line.strip(" ")
#         filterList.append(size)
#         line = ft.readline()
#     ft.close()
# for i in filterList:
#     print("初始数据", i)
def getMiaConn():
    conn = pymysql.connect(host="10.1.3.33", user="pop_cuijiabin", passwd="8dtx5EOUZASc", port=3306, charset="utf8")
    return conn

def filter_sku(txt_path="E:/db_sku.txt"):
    typeMap = {
        "889": "7",
        "2274": "5",
        "2408": "5",
        "3555": "3"
    }
    with open(txt_path) as of:
        line = of.readline()
        conn = getMiaConn()
        cur = conn.cursor()
        while line:
            line = line.strip('\n')
            size = line.split(" ")

            if size[1] == "2408":
                cur.execute(
                    "select i.item_id,i.warehouse_type from mia_mirror.item_user_map i "
                    "where i.item_id =" + str(int(size[0])) + " and i.status = 0")
                data = cur.fetchall()

                if data and len(data) > 0:
                    if typeMap[size[1]] != str(data[0][1]):
                        print(size[0])

            line = of.readline()

        of.close()

# 过滤sku
filter_sku("E:/origin_data.txt")
