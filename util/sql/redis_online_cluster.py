from rediscluster import RedisCluster


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
    redis_client.delete("stock_" + str(itemId))
    redis_client.delete("stock_" + str(itemId) + "_incr")


def get_stock(itemId):
    redis_client = get_cluster_client()
    print(redis_client.hgetall("stock_" + str(itemId)))
    print(redis_client.hgetall("stock_" + str(itemId) + "_incr"))


if __name__ == '__main__':
    # delete_stock(5078083)
    print(get_stock(5078083))
