# coding=utf-8
import json

import requests

import util as bm
import util.mia_db as mu
from threading import Timer
from rediscluster import RedisCluster


# 库存redis集群
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


def gen_stock_key(item_id):
    return "stock_" + str(item_id)


def gen_change_key(item_id):
    return "stock_" + str(item_id) + "_incr"


def gen_pre_qty_lock_key(item_id, wid):
    return "stock_init_pre_qty_lock_" + str(item_id) + "_" + str(wid)


def gen_stock_test_key(item_id):
    return "stock_" + str(item_id) + "_test"


def gen_change_test_key(item_id):
    return "stock_" + str(item_id) + "_test_incr"


# 获取预占的filed
def gen_pre_qty_field(wid):
    return "wid_" + str(wid) + "_preQty"


# 获取库存数量的filed
def gen_qty_field(wid):
    return "wid_" + str(wid) + "_qty"


# 根据itemId 获取redis库存
def get_stock(item_id):
    redis_client = get_cluster_client()
    stock_key = gen_stock_key(item_id)
    change_key = gen_change_key(item_id)

    print(redis_client.hgetall(stock_key))
    print(redis_client.hgetall(change_key))


# 根据itemId 获取redis测试库存
def get_test_stock(item_id):
    redis_client = get_cluster_client()

    stock_key = gen_stock_test_key(item_id)
    change_key = gen_change_test_key(item_id)

    print(redis_client.hgetall(stock_key))
    print(redis_client.hgetall(change_key))


# 根据itemId 删除redis库存
def delete_stock(item_id):
    redis_client = get_cluster_client()

    stock_key = gen_stock_key(item_id)
    change_key = gen_change_key(item_id)

    print(redis_client.hgetall(stock_key))
    print(redis_client.hgetall(change_key))

    redis_client.delete(stock_key)
    redis_client.delete(change_key)


# 增加预占库存
def add_pre_qty_stock(item_id, wid):
    redis_client = get_cluster_client()

    stock_key = gen_stock_key(item_id)
    pre_qty_field = gen_pre_qty_field(wid)

    redis_client.hincrby(stock_key, pre_qty_field, 1)

    change_key = gen_change_key(item_id)
    print(redis_client.hgetall(stock_key))
    print(redis_client.hgetall(change_key))


'''
select * from stock_item WHERE item_id = 5021462;

select  count(oi.id) as number from order_item oi ,orders os
        where oi.order_id =os.id
        and os.warehouse_id= (select warehouse_id from stock_item WHERE item_id = 5021462)
        and os.status in(1,2)
        and os.wdgj_status=1
        and os.is_test=0
        and oi.stock_item_id= (select id from stock_item WHERE item_id = 5021462)
        group by oi.stock_item_id;
'''


def batch_delete_pre_init():
    init_keys = ['3070146_6789']

    redis_client = get_cluster_client()
    for key in init_keys:
        lock_key = "stock_init_pre_qty_lock_" + key
        print(redis_client.get(lock_key))
        redis_client.delete(lock_key)


def test_tup():
    stock_list = [(1, 2), (4, 7)]
    for stock in stock_list:
        print(gen_pre_qty_lock_key(stock[0], stock[1]))


# 根据仓库id获取可用库存列表
def get_stock_item(wid):
    cur = bm.get_mia_cursor("mia_mirror")
    sql = "SELECT * FROM stock_item WHERE warehouse_id = " + str(wid) + " AND status = 1 ORDER BY modify_time DESC"
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    return rows


# 根据仓库id检查预占库存
def check_pre_qty(wid):
    stock_list = get_stock_item(wid)
    if len(stock_list) < 1:
        print("可用库存列表为空 wid = ", wid)
        return

    redis_client = get_cluster_client()
    for stock in stock_list:
        item_id = stock['item_id']
        stock_key = gen_stock_key(item_id)
        pre_qty_field = gen_pre_qty_field(wid)
        redis_pre_qty = redis_client.hget(stock_key, pre_qty_field)
        if redis_pre_qty is None:
            print("预占库存不存在 stock_item_id = %d, item_id = %d, wid = %d " % (stock['id'], item_id, wid))
            continue

        amount = stock['pre_qty'] - int(redis_pre_qty)
        if amount != 0:
            print(
                "预占库存有差异 stock_item_id = %d, item_id = %d, wid = %d, amount= %d " % (stock['id'], item_id, wid, amount))


# 根据仓库id批量检查预占库存
def batch_check_pre_qty(wid_list=[]):
    if len(wid_list) == 0:
        wid_list = [6789]
    for wid in wid_list:
        check_pre_qty(wid)


'''
1.db 预占与 订单不一致 需要清理 init 库存
2.db 与 订单一致 但是与redis不一致 则只清理库存即可！
'''


# 通过接口获取库存列表详情
def get_all_stock_list(item_id_list=[3070022]):
    param_list = []
    for item_id in item_id_list:
        param_list.append({"itemId": item_id, "warehouseIds": [], "isExact": 0})

    r_data = {"paramJSON": json.dumps(param_list)}
    r = requests.post("http://10.5.107.234:7777/getStockQtyForums.sc", data=r_data)

    content = json.loads(r.content.decode("utf-8"))
    print(content["result"])


def check_all_by_stock_item_id(stock_item_id=5291074, is_modify=False):
    cur = bm.get_mia_cursor("mia_mirror")
    sql = "SELECT * FROM stock_item WHERE id = " + str(stock_item_id)
    cur.execute(sql)
    columns = [col[0] for col in cur.description]
    fetch = cur.fetchall()
    if len(fetch) == 0:
        print("数据库查询失败", stock_item_id)
        return
    db_item = dict(zip(columns, fetch[0]))

    item_id = db_item["item_id"]
    wid = db_item["warehouse_id"]

    order_sql = "select ifnull(count(oi.id), 0) as number " \
                "from order_item oi left join orders os on oi.order_id = os.id " + \
                "where os.warehouse_id= " + str(wid) + \
                " and os.status in(1,2) and os.wdgj_status=1 and os.is_test= 0 " + \
                "and oi.stock_item_id= " + str(db_item["id"]) + \
                " group by oi.stock_item_id"
    cur.execute(order_sql)
    fetch = cur.fetchall()
    order_count = (0 if (len(fetch) == 0) else fetch[0][0])

    redis_client = get_cluster_client()
    stock_key = gen_stock_key(item_id)
    pre_qty_field = gen_pre_qty_field(wid)
    redis_pre_qty = redis_client.hget(stock_key, pre_qty_field)
    if redis_pre_qty is None:
        print("预占库存不存在 stock_item_id = %d" % stock_item_id)
        return

    redis_pre_qty = int(redis_pre_qty)

    if order_count != db_item["pre_qty"]:
        print("预占库存与订单不一致 stock_item_id = %d, db_pre_qty = %d, order_count= %d"
              % (stock_item_id, db_item["pre_qty"], order_count))
        if is_modify:
            pre_qty_lock_key = gen_pre_qty_lock_key(item_id, wid)
            redis_client.delete(pre_qty_lock_key)
            redis_client.delete(stock_key)
            # 刷新
            param_list = [{"itemId": item_id, "warehouseIds": [wid], "isExact": 0}]
            r_data = {"paramJSON": json.dumps(param_list)}
            r = requests.post("http://10.5.107.234:7777/getStockQtyForums.sc", data=r_data)
            content = json.loads(r.content.decode("utf-8"))
            print(content["result"])

    elif redis_pre_qty != db_item["pre_qty"]:
        print("预占库存与redis不一致 stock_item_id = %d, db_pre_qty = %d, redis_pre_qty= %d"
              % (stock_item_id, db_item["pre_qty"], redis_pre_qty))
        if is_modify:
            redis_client.delete(stock_key)
            # 刷新
            param_list = [{"itemId": item_id, "warehouseIds": [wid], "isExact": 0}]
            r_data = {"paramJSON": json.dumps(param_list)}
            r = requests.post("http://10.5.107.234:7777/getStockQtyForums.sc", data=r_data)
            content = json.loads(r.content.decode("utf-8"))
            print(content["result"])


# 批量检查库存
def batch_check_all_by_stock_item_id(stock_id_list=[6985391], is_modify=False):
    cur = bm.get_mia_cursor("mia_mirror")
    for stock_item_id in stock_id_list:

        sql = "SELECT * FROM stock_item WHERE id = " + str(stock_item_id)
        cur.execute(sql)
        columns = [col[0] for col in cur.description]
        fetch = cur.fetchall()
        if len(fetch) == 0:
            print("数据库查询失败", stock_item_id)
            return
        db_item = dict(zip(columns, fetch[0]))

        item_id = db_item["item_id"]
        wid = db_item["warehouse_id"]

        order_sql = "select ifnull(count(oi.id), 0) as number " \
                    "from order_item oi left join orders os on oi.order_id = os.id " + \
                    "where os.warehouse_id= " + str(wid) + \
                    " and os.status in(1,2) and os.wdgj_status=1 and os.is_test= 0 " + \
                    "and oi.stock_item_id= " + str(db_item["id"]) + \
                    " group by oi.stock_item_id"
        cur.execute(order_sql)
        fetch = cur.fetchall()
        order_count = (0 if (len(fetch) == 0) else fetch[0][0])
        redis_client = get_cluster_client()
        stock_key = gen_stock_key(item_id)
        pre_qty_field = gen_pre_qty_field(wid)
        redis_pre_qty = redis_client.hget(stock_key, pre_qty_field)
        if redis_pre_qty is None:
            print("预占库存不存在 stock_item_id = %d" % stock_item_id)
            return

        redis_pre_qty = int(redis_pre_qty)

        if order_count != db_item["pre_qty"]:
            print("预占库存与订单不一致 stock_item_id = %d, db_pre_qty = %d, order_count= %d"
                  % (stock_item_id, db_item["pre_qty"], order_count))
            if is_modify:
                pre_qty_lock_key = gen_pre_qty_lock_key(item_id, wid)
                redis_client.delete(pre_qty_lock_key)
                redis_client.delete(stock_key)
                # 刷新
                param_list = [{"itemId": item_id, "warehouseIds": [wid], "isExact": 0}]
                r_data = {"paramJSON": json.dumps(param_list)}
                r = requests.post("http://10.5.107.234:7777/getStockQtyForums.sc", data=r_data)
                content = json.loads(r.content.decode("utf-8"))
                print(content["result"])

        elif redis_pre_qty != db_item["pre_qty"]:
            print("预占库存与redis不一致 stock_item_id = %d, db_pre_qty = %d, redis_pre_qty= %d"
                  % (stock_item_id, db_item["pre_qty"], redis_pre_qty))
            if is_modify:
                redis_client.delete(stock_key)
                # 刷新
                param_list = [{"itemId": item_id, "warehouseIds": [wid], "isExact": 0}]
                r_data = {"paramJSON": json.dumps(param_list)}
                r = requests.post("http://10.5.107.234:7777/getStockQtyForums.sc", data=r_data)
                content = json.loads(r.content.decode("utf-8"))
                print(content["result"])
    cur.close()


if __name__ == "__main__":
    # wid_list = [7254]
    # batch_check_pre_qty(wid_list)
    # get_all_stock_list(item_list)
    # get_stock(3070022)
    check_pre_qty(6789)

    # item_list = [6973212, 6985399]
    # batch_check_all_by_stock_item_id(item_list, True)
    # for item in item_list:
    #     # print("当前检查:", item)
    # check_all_by_stock_item_id(6449308, False)
