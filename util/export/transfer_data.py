# coding=utf-8
import sched
import time
import json
import requests
from datetime import datetime
from datetime import date
import common_build_model as bm


def get_record():
    # delta = date.today() - date(2014, 3, 2)
    # preDay = delta.days + 2
    preDay = 1500

    cur = bm.get_mia_cursor("mia_bigtable")

    is_next = True
    while preDay > 1:
        sql = "SELECT id FROM mia_bigtable.item_update_log a" \
              " WHERE a.typeid IN (106, 122, 6) AND a.updatetime BETWEEN " \
              "DATE_ADD(NOW(), INTERVAL -" + str(preDay) + " DAY) " \
                                                               "AND DATE_ADD(NOW(), INTERVAL-" + str(
            preDay-1) + " DAY) limit 60000"

        cur.execute(sql)
        f_data = cur.fetchall()
        f_data = list(map(lambda x: x[0], f_data))
        if len(f_data) < 60000:
            is_next = True
        else:
            is_next = False

        if len(f_data) == 0:
            print(preDay, "天前数据为空")
        else:
            print(preDay, "天前数据大小是：", len(f_data))

        for i in range(0, len(f_data), 500):
            transfer(f_data[i:i + 500])

        if is_next:
            preDay -= 1


def transfer(arr):
    param = {
        "pwd": "UITN25LMUQC436IM",
        "jsonParam": str(arr)
    }
    r = requests.get("http://shop.xiaowu58.com/item/transfer.html", params=param)
    if r.status_code == 200:
        return
    else:
        print("请求失败了")


if __name__ == "__main__":

    try:
        get_record()
    except Exception:
        print("意外出错")
        get_record()
