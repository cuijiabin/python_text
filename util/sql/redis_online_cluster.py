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


def batch_delete():
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
    init_keys = ['33070202_6789']

    redis_client = get_cluster_client()
    for key in init_keys:
        lock_key = "stock_init_pre_qty_lock_" + key
        print(redis_client.get(lock_key))
        redis_client.delete(lock_key)


if __name__ == '__main__':
    print("")
    # get_stock(3070202)
    delete_stock(3070202)
    # pre_incr_stock(4880683, 6789)
    # batch_delete()
