import time

from rediscluster import RedisCluster
import requests


def get_cluster_client():
    redis_nodes = [
        {'host': '172.16.96.189', 'port': 7000},
        {'host': '172.16.96.190', 'port': 7001},
        {'host': '172.16.96.191', 'port': 7002}
        # {'host': '172.16.96.190', 'port': 7000},
        # {'host': '172.16.96.191', 'port': 7000}
    ]

    return RedisCluster(startup_nodes=redis_nodes, decode_responses=True)


def test_add_data():
    redis_client = get_cluster_client()

    # redis_client.hset("crm_uid_phone_relation:99", "159388999", "13651054199")
    # redis_client.hset("crm_uid_phone_relation:47", "220105847", "17600965516")
    # redis_client.hset("crm_uid_phone_relation:64", "1508764", "15011346605")
    # redis_client.hset("crm_uid_phone_relation:15", "220108515", "15100327518")
    # redis_client.hset("crm_uid_phone_relation:21", "13789821", "18611458501")
    # redis_client.hset("crm_uid_phone_relation:14", "220109414", "13629205802")
    # redis_client.hset("crm_uid_phone_relation:46", "220109446", "15691978761")
    # redis_client.hset("crm_uid_phone_relation:21", "220105921", "13572504251")
    # redis_client.hset("crm_uid_phone_relation:53", "220107053", "18602988591")
    # redis_client.hset("crm_uid_phone_relation:88", "220108488", "17310853906")
    # print(redis_client.hgetall("crm_upload_uid_phone_relation:424"))
    # print(redis_client.lrange("crm_upload_uid_phone_list:424", 0, -1))
    # print(redis_client.get("stock_spu_sku_relation_33356"))
    # print(redis_client.delete("stock_spu_sku_relation_20181229"))
    print(redis_client.delete("stock_spu_sku_relation_20200024"))
    # print(redis_client.delete("stock_self_bmp_warehouse"))


def test_match():
    redis_client = get_cluster_client()
    for key in redis_client.scan_iter("crm_uid_phone_relation*"):
        print(key)
        if redis_client.type(key) == 'string':
            print(redis_client.get(key))
        elif redis_client.type(key) == 'hash':
            print(redis_client.hgetall(key))


def delete_stock(itemId):
    redis_client = get_cluster_client()
    print(redis_client.hgetall("stock_" + str(itemId)))
    print(redis_client.hgetall("stock_" + str(itemId) + "_incr"))
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
    data_list = ['2019-12-24']

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
    data_list = ['2019-12-24']

    redis_client = get_cluster_client()
    for data in data_list:
        redis_client.delete("data_handel_create_lock:" + data)
        redis_client.delete("data_handel_pay_lock:" + data)
        redis_client.delete("data_handel_cancel_lock:" + data)


def get_set_info():
    r = get_cluster_client()
    # print(r.exists("crm_strategy_task_zset"))
    s = r.zscan("crm_strategy_task_zset", 20)
    print(s)
    print(r.zcard("crm_strategy_task_zset"))


if __name__ == '__main__':
    # delete_stock(2020038638)
    test_add_data()
    # get_stock(2065355)
    # d_list = [2020037710, 2020037663, 2020037662, 38765444, 2020037657]
    # for d in d_list:
    #     delete_stock(d)
    # clear_export_key()
    # get_stock_test(1000133)
    # redis_client = get_cluster_client()
    # # print(redis_client.get("spu_sku_relation_2020037627"))
    # print(redis_client.get("stockPreCheckDailyRedisLock"))
    # redis_client.delete("stockPreCheckDailyRedisLock")
