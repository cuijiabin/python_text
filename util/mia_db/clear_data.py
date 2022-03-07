import time

import pymysql
import requests
from itertools import groupby
from itertools import islice
from string import Template


def get_mia_cursor(db_name="mia_mirror"):
    conn = pymysql.connect(host="10.5.96.80",
                           port=3306,
                           user="pop_cuijiabin",
                           passwd="8dtx5EOUZASc#",
                           db=db_name,
                           charset="utf8")
    return conn.cursor()


def get_log_data(user_id_list):
    cur = get_mia_cursor("mia_mirror")
    sql_tmp = Template(
        "SELECT id,user_id FROM `user_mi_bean_log` "
        "WHERE user_id in ($user_ids) "
        "AND relation_type = 'expired_2020' and created_time = '2020-12-31 23:59:59'")
    sql = sql_tmp.substitute(user_ids=','.join(map(lambda x: str(x), user_id_list)))
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return rows


def get_remove_data(user_id_list):
    detail_list = get_log_data(user_id_list)
    result_list = []
    for k, g in groupby(detail_list, lambda x: x["user_id"]):
        sub_list = list(map(lambda x: x["id"], g))
        if len(sub_list) < 2:
            continue

        del (sub_list[0])
        result_list += sub_list

    return result_list


def l_read_file(filename, num, N):
    # a = open("E:/file/download/mibean/" + str(num) + ".txt", "w")

    with open(filename, 'r') as infile:
        lines_gen = islice(infile, N)
        ids = list(map(lambda x: x.split('\t')[0], lines_gen))
        while len(ids) > 0:
            detail_list = get_remove_data(ids)
            if len(detail_list) == 0:
                lines_gen = islice(infile, N)
                ids = list(map(lambda x: x.split('\t')[0], lines_gen))
                continue
            print(len(detail_list))
            r_data = {
                "logIds": ','.join(map(lambda x: str(x), detail_list))
            }
            r = requests.post("http://10.5.107.217:9999/userJob/batchDelLog", data=r_data)
            print(r.status_code)
            time.sleep(2)
            # sql = "DELETE FROM `user_mi_bean_log` WHERE id IN (" + ','.join(map(lambda x: str(x), detail_list)) + ");"
            # print(sql, filename=a)
            # a.write(sql + "\n")
            lines_gen = islice(infile, N)
            ids = list(map(lambda x: x.split('\t')[0], lines_gen))
    infile.close()
    # a.close()


def read_file(file_path):
    with open(file_path, 'r') as f:
        line = f.readline()
        num = 1
        while line:
            line = line.strip('\n')
            if len(line) == 0:
                continue
            requests.get("http://10.5.108.57:8080/orderTrailInit?thirdOrderCode=" + line)
            if num % 500 == 0:
                print(num, "休眠")
                time.sleep(3)
            num += 1
            line = f.readline()
        f.close()


if __name__ == '__main__':
    # for i in range(0, 133):
    # for i in range(0, 1):
    #     file_name = "E:/file/download/mibean/bean_total_" + str(i + 1) + ".txt"
    #     print(file_name)
    #     l_read_file(file_name, i, 500)
    #     time.sleep(1)
    read_file('E:/file/download/file_32.txt')
    # oo = [
    # ]
    # for o in oo:
    #     post_data = {
    #         "orderCode": str(o),
    #         "targetWarehouseId": 9769,
    #         # "confirmTime": "2021-10-21 14:00:00",
    #     }
    #
    #     r = requests.post("http://10.5.107.177:8082/order/changeOrderWarehouse.sc", data=post_data)
    #     print(str(o), r.content.decode("utf-8"))
