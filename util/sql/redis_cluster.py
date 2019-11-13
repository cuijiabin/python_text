from rediscluster import RedisCluster


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


if __name__ == '__main__':
    # get_stock(10489)
    redis_client = get_cluster_client()
    # print(redis_client.get("spu_sku_relation_2020037627"))
    print(redis_client.get("stockPreCheckDailyRedisLock"))
    redis_client.delete("stockPreCheckDailyRedisLock")
