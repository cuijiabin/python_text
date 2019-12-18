# coding=utf-8
import json

import util as bm
import util.mia_db as mu
from threading import Timer
from rediscluster import RedisCluster

"""
获取spu的信息然后转换成字典对象
"""


def get_cluster_client():
    redis_nodes = [
        {'host': '10.5.96.169', 'port': 7012},
        {'host': '10.5.96.174', 'port': 7012},
        {'host': '10.5.96.181', 'port': 7012},
        {'host': '10.5.96.228', 'port': 7024},
        {'host': '10.5.97.18', 'port': 7024},
        {'host': '10.5.96.169', 'port': 7013}
    ]

    return RedisCluster(startup_nodes=redis_nodes, decode_responses=True)


"""
根据仓库id获取可用库存列表
"""


def get_stock_item(wid):
    cur = bm.get_mia_cursor("mia_mirror")
    sql = "SELECT * FROM stock_item WHERE warehouse_id = " + str(wid) + " AND status = 1 ORDER BY modify_time DESC"
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    return rows


def check_pre_qty(wid):
    stock_list = get_stock_item(wid)
    if len(stock_list) < 1:
        print("无库存服务")
        return

    redis_client = get_cluster_client()
    for s in stock_list:

        stock_key = "stock_" + str(s['item_id'])
        pre_qty_field = "wid_" + str(wid) + "_preQty"
        redis_pre_qty = redis_client.hget(stock_key, pre_qty_field)
        if redis_pre_qty is None:
            print(s['item_id'])
            continue

        amount = s['pre_qty'] - int(redis_pre_qty)
        if amount != 0:
            print(s)
            print(redis_pre_qty)
            redis_client.hincrby(stock_key, pre_qty_field, amount)


if __name__ == "__main__":
    check_pre_qty(2985)
    check_pre_qty(6789)
    check_pre_qty(7772)
    check_pre_qty(7922)
