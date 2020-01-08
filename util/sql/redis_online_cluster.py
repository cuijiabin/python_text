import time

import requests
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


def delete_stock(itemId):
    redis_client = get_cluster_client()

    print(redis_client.hgetall("stock_" + str(itemId)))
    print(redis_client.hgetall("stock_" + str(itemId) + "_incr"))

    redis_client.delete("stock_" + str(itemId))
    redis_client.delete("stock_" + str(itemId) + "_incr")


def get_pre_qty_lock_key(item_id, wid):
    return "stock_init_pre_qty_lock_" + str(item_id) + "_" + str(wid)


def get_stock(itemId):
    redis_client = get_cluster_client()
    print(redis_client.hgetall("stock_" + str(itemId)))
    print(redis_client.hgetall("stock_" + str(itemId) + "_incr"))


def pre_incr_stock(itemId, wid):
    redis_client = get_cluster_client()
    s_key = "stock_" + str(itemId)
    s_field = "wid_" + str(wid) + "_preQty"
    redis_client.hincrby(s_key, s_field, 1)
    print(redis_client.hgetall("stock_" + str(itemId)))
    print(redis_client.hgetall("stock_" + str(itemId) + "_incr"))


def hdel_incr_stock(itemId, wid):
    redis_client = get_cluster_client()
    s_key = "stock_" + str(itemId)
    s_field = "wid_" + str(wid) + "_preQty"
    redis_client.hdel(s_key, s_field)
    print(redis_client.hgetall("stock_" + str(itemId)))
    print(redis_client.hgetall("stock_" + str(itemId) + "_incr"))


def batch_delete_pre_init():
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
    init_keys = ['2913685_6333']

    redis_client = get_cluster_client()
    for key in init_keys:
        lock_key = "stock_init_pre_qty_lock_" + key
        print(redis_client.get(lock_key))
        redis_client.delete(lock_key)


'''
检查6789仓库的数据
'''


def compare_wid_6789():
    print("")


def get_stock_test(itemId):
    redis_client = get_cluster_client()
    print(redis_client.hgetall("stock_" + str(itemId) + "_test"))
    print(redis_client.hgetall("stock_" + str(itemId) + "_test_incr"))


def run_export_data():
    data_list = ['2019-12-27']

    redis_client = get_cluster_client()
    for data in data_list:
        create_value = redis_client.get("data_handel_create_lock:" + data)
        while not create_value:
            requests.get("http://10.5.107.234:9093/runCreateExport?day=" + data)
            time.sleep(0.1)
            create_value = redis_client.get("data_handel_create_lock:" + data)
        while not create_value == "1":
            time.sleep(0.1)
            create_value = redis_client.get("data_handel_create_lock:" + data)
        print(data + "创单完成")

        pay_value = redis_client.get("data_handel_pay_lock:" + data)
        while not pay_value:
            requests.get("http://10.5.107.234:9093/runPayExport?day=" + data)
            time.sleep(0.1)
            pay_value = redis_client.get("data_handel_pay_lock:" + data)
        while not pay_value == "1":
            time.sleep(0.1)
            pay_value = redis_client.get("data_handel_pay_lock:" + data)
        print(data + "支付完成")

        cancel_value = redis_client.get("data_handel_cancel_lock:" + data)
        while not cancel_value:
            requests.get("http://10.5.107.234:9093/runCancelExport?day=" + data)
            time.sleep(0.1)
            cancel_value = redis_client.get("data_handel_cancel_lock:" + data)
        while not cancel_value == "1":
            time.sleep(0.1)
            cancel_value = redis_client.get("data_handel_cancel_lock:" + data)
        print(data + "取消完成")


def clear_export_key():
    data_list = ['2019-12-27']

    redis_client = get_cluster_client()
    for data in data_list:
        print(data, redis_client.get("data_handel_create_lock:" + data))
        print(data, redis_client.get("data_handel_pay_lock:" + data))
        print(data, redis_client.get("data_handel_cancel_lock:" + data))
        redis_client.delete("data_handel_create_lock:" + data)
        redis_client.delete("data_handel_pay_lock:" + data)
        redis_client.delete("data_handel_cancel_lock:" + data)


if __name__ == '__main__':
    # run_export_data()
    # clear_export_key()
    # get_stock_test(3070037)
    delete_stock(10489)
    # batch_delete_pre_init()
    # dd = [3072319]
    # for d in dd:
    #     delete_stock(d)
