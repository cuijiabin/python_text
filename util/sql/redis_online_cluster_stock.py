import time

import requests
from rediscluster import RedisCluster


# # 库存redis集群
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


# 获取预占的filed
def gen_pre_qty_field(wid):
    return "wid_" + str(wid) + "_preQty"


# 根据itemId 删除redis库存
def delete_stock(item_id):
    redis_client = get_cluster_client()

    stock_key = gen_stock_key(item_id)
    change_key = gen_change_key(item_id)

    print(redis_client.hgetall(stock_key))
    print(redis_client.hgetall(change_key))

    redis_client.delete(stock_key)
    redis_client.delete(change_key)


# 根据itemId 获取redis库存
def get_stock(item_id):
    redis_client = get_cluster_client()
    stock_key = gen_stock_key(item_id)
    change_key = gen_change_key(item_id)

    print(redis_client.hgetall(stock_key))
    print(redis_client.hgetall(change_key))


# 增加预占库存
def pre_incr_stock(item_id, wid):
    redis_client = get_cluster_client()

    stock_key = gen_stock_key(item_id)
    change_key = gen_change_key(item_id)

    pre_qty_field = gen_pre_qty_field(wid)
    redis_client.hincrby(stock_key, pre_qty_field, 1)

    print(redis_client.hgetall(stock_key))
    print(redis_client.hgetall(change_key))


def hdel_incr_stock(itemId, wid):
    redis_client = get_cluster_client()
    s_key = "stock_" + str(itemId)
    s_field = "wid_" + str(wid) + "_preQty"
    redis_client.hdel(s_key, s_field)
    print(redis_client.hgetall("stock_" + str(itemId)))
    print(redis_client.hgetall("stock_" + str(itemId) + "_incr"))


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


'''
仓库数据检查 TODO
'''


def get_stock_test(item_id):
    redis_client = get_cluster_client()
    print(redis_client.hgetall("stock_" + str(item_id) + "_test"))
    print(redis_client.hgetall("stock_" + str(item_id) + "_test_incr"))


def test_tup():
    stock_list = [(1, 2), (4, 7)]
    for stock in stock_list:
        print(gen_pre_qty_lock_key(stock[0], stock[1]))


if __name__ == '__main__':
    # batch_delete_pre_init()
    # delete_stock(3070146)
    get_stock(3070005)

    # test_tup()
