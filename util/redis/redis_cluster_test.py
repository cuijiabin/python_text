# coding=utf-8
import util as bm


def get_spu_sku_relation():
    redis_client = bm.get_test_cluster_client()

    print(redis_client.get("stock_spu_sku_relation_5894918"))


def test_match():
    redis_client = bm.get_test_cluster_client()
    for key in redis_client.scan_iter("crm_uid_phone_relation*"):
        print(key)
        if redis_client.type(key) == 'string':
            print(redis_client.get(key))
        elif redis_client.type(key) == 'hash':
            print(redis_client.hgetall(key))


def delete_stock(itemId):
    redis_client = bm.get_test_cluster_client()
    print(redis_client.hgetall("stock_" + str(itemId)))
    print(redis_client.hgetall("stock_" + str(itemId) + "_incr"))
    redis_client.delete("stock_" + str(itemId))
    redis_client.delete("stock_" + str(itemId) + "_incr")


def get_stock(itemId):
    redis_client = bm.get_test_cluster_client()
    print(redis_client.hgetall("stock_" + str(itemId)))
    print(redis_client.hgetall("stock_" + str(itemId) + "_incr"))


def get_stock_test(itemId):
    redis_client = bm.get_test_cluster_client()
    print(redis_client.hgetall("stock_" + str(itemId) + "_test"))
    print(redis_client.hgetall("stock_" + str(itemId) + "_test_incr"))


def test_queue():
    redis_client = bm.get_test_cluster_client()
    m = redis_client.zadd("data_export", 1)
    print(m)
    print(redis_client.zscore("data_export", 1))


def clear_export_key():
    data_list = ['2019-12-24']

    redis_client = bm.get_test_cluster_client()
    for data in data_list:
        redis_client.delete("data_handel_create_lock:" + data)
        redis_client.delete("data_handel_pay_lock:" + data)
        redis_client.delete("data_handel_cancel_lock:" + data)


def get_set_info():
    r = bm.get_test_cluster_client()
    # print(r.exists("crm_strategy_task_zset"))
    s = r.zscan("crm_strategy_task_zset", 20)
    print(s)
    print(r.zcard("crm_strategy_task_zset"))


if __name__ == '__main__':
    # delete_stock(2020038638)
    get_spu_sku_relation()
    # get_stock(2065355)
