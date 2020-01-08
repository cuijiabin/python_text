import time

from rediscluster import RedisCluster
import requests


def get_cluster_client():
    redis_nodes = [
        {'host': '172.16.96.189', 'port': 7000},
        {'host': '172.16.96.190', 'port': 7001},
        {'host': '172.16.96.191', 'port': 7002}
    ]

    return RedisCluster(startup_nodes=redis_nodes, decode_responses=True)


def test_match():
    redis_client = get_cluster_client()
    for key in redis_client.scan_iter("SynUmsError_*"):
        print(key)
        if redis_client.type(key) == 'string':
            print(redis_client.get(key))
        elif redis_client.type(key) == 'hash':
            print(redis_client.hgetall(key))


def delete_stock(itemId):
    redis_client = get_cluster_client()
    redis_client.delete("stock_" + str(itemId))
    redis_client.delete("stock_" + str(itemId) + "_incr")


def get_stock(itemId):
    redis_client = get_cluster_client()
    print(redis_client.hgetall("stock_" + str(itemId)))
    print(redis_client.hgetall("stock_" + str(itemId) + "_incr"))


def get_stock_test(itemId):
    redis_client = get_cluster_client()
    print(redis_client.hgetall("stock_" + str(itemId) + "_test"))
    print(redis_client.hgetall("stock_" + str(itemId) + "_test_incr"))


def test_queue():
    redis_client = get_cluster_client()
    m = redis_client.zadd("data_export", 1)
    print(m)
    print(redis_client.zscore("data_export", 1))


def run_export_data():
    data_list = ['2019-10-26', '2019-10-27', '2019-10-28', '2019-10-29', '2019-10-30', '2019-10-31', '2019-11-01',
                 '2019-11-02', '2019-11-03', '2019-11-04', '2019-11-05', '2019-11-06', '2019-11-07', '2019-11-08',
                 '2019-11-09', '2019-11-10', '2019-11-11', '2019-11-12', '2019-11-13', '2019-11-14', '2019-11-15',
                 '2019-11-16', '2019-11-17', '2019-11-18', '2019-11-19', '2019-11-20', '2019-11-21', '2019-11-22',
                 '2019-11-23', '2019-11-24', '2019-11-25', '2019-11-26', '2019-11-27', '2019-11-28', '2019-11-29',
                 '2019-11-30', '2019-12-01', '2019-12-02', '2019-12-03', '2019-12-04', '2019-12-05', '2019-12-06',
                 '2019-12-07', '2019-12-08', '2019-12-09', '2019-12-10', '2019-12-11', '2019-12-12', '2019-12-13',
                 '2019-12-14', '2019-12-15', '2019-12-16', '2019-12-17', '2019-12-18', '2019-12-19', '2019-12-20',
                 '2019-12-21', '2019-12-22', '2019-12-23', '2019-12-24']

    redis_client = get_cluster_client()
    for data in data_list:
        # create_value = redis_client.get("data_handel_create_lock:" + data)
        # while not create_value:
        #     requests.get("http://127.0.0.1:9093/runCreateExport?day=" + data)
        #     time.sleep(0.1)
        #     create_value = redis_client.get("data_handel_create_lock:" + data)
        # while not create_value == "1":
        #     time.sleep(0.1)
        #     create_value = redis_client.get("data_handel_create_lock:" + data)
        # print(data + "创单完成")
        #
        # pay_value = redis_client.get("data_handel_pay_lock:" + data)
        # while not pay_value:
        #     requests.get("http://127.0.0.1:9093/runPayExport?day=" + data)
        #     time.sleep(0.1)
        #     pay_value = redis_client.get("data_handel_pay_lock:" + data)
        # while not pay_value == "1":
        #     time.sleep(0.1)
        #     pay_value = redis_client.get("data_handel_pay_lock:" + data)
        # print(data + "支付完成")

        cancel_value = redis_client.get("data_handel_cancel_lock:" + data)
        while not cancel_value:
            requests.get("http://127.0.0.1:9093/runCancelExport?day=" + data)
            time.sleep(0.1)
            cancel_value = redis_client.get("data_handel_cancel_lock:" + data)
        while not cancel_value == "1":
            time.sleep(0.1)
            cancel_value = redis_client.get("data_handel_cancel_lock:" + data)
        print(data + "取消完成")


def clear_export_key():
    data_list = ['2019-10-26', '2019-10-27', '2019-10-28', '2019-10-29', '2019-10-30', '2019-10-31', '2019-11-01',
                 '2019-11-02', '2019-11-03', '2019-11-04', '2019-11-05', '2019-11-06', '2019-11-07', '2019-11-08',
                 '2019-11-09', '2019-11-10', '2019-11-11', '2019-11-12', '2019-11-13', '2019-11-14', '2019-11-15',
                 '2019-11-16', '2019-11-17', '2019-11-18', '2019-11-19', '2019-11-20', '2019-11-21', '2019-11-22',
                 '2019-11-23', '2019-11-24', '2019-11-25', '2019-11-26', '2019-11-27', '2019-11-28', '2019-11-29',
                 '2019-11-30', '2019-12-01', '2019-12-02', '2019-12-03', '2019-12-04', '2019-12-05', '2019-12-06',
                 '2019-12-07', '2019-12-08', '2019-12-09', '2019-12-10', '2019-12-11', '2019-12-12', '2019-12-13',
                 '2019-12-14', '2019-12-15', '2019-12-16', '2019-12-17', '2019-12-18', '2019-12-19', '2019-12-20',
                 '2019-12-21', '2019-12-22', '2019-12-23', '2019-12-24']

    redis_client = get_cluster_client()
    for data in data_list:
        redis_client.delete("data_handel_create_lock:" + data)
        redis_client.delete("data_handel_pay_lock:" + data)
        redis_client.delete("data_handel_cancel_lock:" + data)


if __name__ == '__main__':
    # run_export_data()
    # get_stock(10489)
    delete_stock(10489)
    # clear_export_key()
    # get_stock_test(1000133)
    # redis_client = get_cluster_client()
    # # print(redis_client.get("spu_sku_relation_2020037627"))
    # print(redis_client.get("stockPreCheckDailyRedisLock"))
    # redis_client.delete("stockPreCheckDailyRedisLock")
