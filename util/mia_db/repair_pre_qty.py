# coding=utf-8
import json
import time

import pymysql
import requests


def get_mia_cursor(db_name="mia_mirror"):
    conn = pymysql.connect(host="10.5.96.80",
                           port=3306,
                           user="pop_cuijiabin",
                           passwd="8dtx5EOUZASc#",
                           db=db_name,
                           charset="utf8")
    return conn.cursor()


def get_stock_item(wid):
    cur = get_mia_cursor("mia_mirror")
    sql = "SELECT id,item_id,pre_qty FROM stock_item WHERE warehouse_id = " + str(
        wid) + " AND status = 1 AND modify_time > ADDDATE(NOW(),INTERVAL -1 HOUR) ORDER BY modify_time DESC"
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    return rows


def check_warehouse_qty(wid_list=[7694, 7697]):
    while True:
        print(time.strftime('%Y-%m-%d %X', time.localtime()))
        ids = []
        for wid in wid_list:
            rows = get_stock_item(wid)
            tmp_ids = list(map(lambda x: x['id'], rows))
            for stock_id in tmp_ids:
                ids.append(str(stock_id))

        print(len(ids))
        if len(ids) > 0:
            stock_item_ids = ",".join(ids)
            r_data = {
                "stockItemIds": stock_item_ids,
                "type": 1
            }
            r = requests.post("http://10.5.107.234:7777/repairPreQty.sc", data=r_data)
            content = json.loads(r.content.decode("utf-8"))
            if len(content) > 0:
                for c in content:
                    if c["content"] == "预占库存与订单不一致" or c["content"] == "预占库存与redis不一致":
                        print(c)
        time.sleep(10 * 60)


if __name__ == '__main__':
    check_warehouse_qty()
