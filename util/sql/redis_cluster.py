from rediscluster import StrictRedisCluster


def get_cluster_client():
    redis_nodes = [
        {'host': '172.16.96.189', 'port': 7000},
        {'host': '172.16.96.190', 'port': 7001},
        {'host': '172.16.96.191', 'port': 7002}
    ]

    return StrictRedisCluster(startup_nodes=redis_nodes, max_connections=10)


if __name__ == '__main__':

    redisClient = get_cluster_client()
    for key in redisClient.scan_iter("pop:partner:*"):
        print(key)
        print(redisClient.get(key))
