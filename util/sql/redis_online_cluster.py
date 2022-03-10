import time

import requests
import json
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
        # {'host': '10.5.96.181', 'port': 7006},
        # {'host': '10.5.96.228', 'port': 7009},
        # {'host': '10.5.96.228', 'port': 7020},
        # {'host': '10.5.97.18', 'port': 7011},
        # {'host': '10.5.96.174', 'port': 7011},
        # {'host': '10.5.97.18', 'port': 7018}
    ]

    return RedisCluster(startup_nodes=redis_nodes, decode_responses=True)


def test_add_data():
    redis_client = get_cluster_client()

    print(redis_client.get("stock_self_bmp_warehouse"))
    # print(redis_client.delete("stock_self_bmp_warehouse"))


# def test_add_data(user_list):
#     redis_client = get_cluster_client()
#     for user_id in user_list:
#         mod = user_id % 100
#         print(redis_client.hget("crm_uid_phone_relation:" + str(mod), str(user_id)))


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
    print(itemId)
    print(redis_client.hgetall("stock_" + str(itemId)))
    # print(redis_client.hget("stock_" + str(itemId), "wid_3364_stockItemId"))
    # print(redis_client.hgetall("stock_" + str(itemId) + "_incr"))


def check_warehouse_num(itemId, num):
    redis_client = get_cluster_client()
    keys = redis_client.hgetall("stock_" + str(itemId))
    w_list = []
    for key in keys:
        # print(key)
        wid = key.split("_")[1]
        w_list.append(wid)

    w_num = len(set(w_list))
    if num != w_num:
        print(itemId, num, w_num)


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
    data_list = ['2020-04-06']

    redis_client = get_cluster_client()
    for data in data_list:
        print(data, redis_client.get("data_handel_create_lock:" + data))
        print(data, redis_client.get("data_handel_pay_lock:" + data))
        print(data, redis_client.get("data_handel_cancel_lock:" + data))
        redis_client.delete("data_handel_create_lock:" + data)
        redis_client.delete("data_handel_pay_lock:" + data)
        redis_client.delete("data_handel_cancel_lock:" + data)


def get_all_stock_list(itemId):
    ll = []
    ll.append({
        "itemId": itemId,
        "warehouseIds": [],
        "isExact": 0,
        "isTest": 1,
    })
    r_data = {"paramJSON": json.dumps(ll)}
    r = requests.post("http://10.5.107.234:7777/getStockQtyForums.sc", data=r_data)
    content = json.loads(r.content.decode("utf-8"))
    print(content["result"])


if __name__ == '__main__':
    # run_export_data()
    # clear_export_key()
    # get_stock_test(3070037)
    # 1000239 1000847
    # delete_stock(6161488)
    # batch_delete_pre_init()
    # test_add_data()
    item_list = [
        4210781, 4602847, 4602846, 5835062, 5831810, 5835046, 5835045, 5831762, 5384580, 5441593, 5441594, 5803367, 4408571, 3859778, 3859777, 3859776, 4341894, 5987542, 5982135, 3658173, 5372610, 5372611, 5372612, 4498025, 4210792, 4210793, 4210777, 4210778, 4210782, 4210783, 4151050, 4151049, 4151048, 5868481, 5565099, 5189348, 5189345, 5189346, 5189347, 5189342, 5189343, 5189344, 5189339, 5189341, 6137864, 5373135, 5403215, 5403216, 5847676, 5373137, 5403213, 5403214, 5819060
    ]
    for id in item_list:
        delete_stock(id)
        # check_warehouse_num(id[0], id[1])
    #     get_all_stock_list(id)
    # delete_stock(5641520)
    # redis_client = get_cluster_client()
    # print(redis_client.get("data_handel_create_lock:2020-06-29"))
    # print(redis_client.delete("data_handel_create_lock:2020-06-29"))
