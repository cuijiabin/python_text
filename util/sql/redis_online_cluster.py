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


if __name__ == '__main__':
    # delete_stock(5078083)
    # print(get_stock(5078083))

    # redis_client.delete("stock_init_pre_qty_lock_5210920_6773")
    # redis_client.delete("stock_init_pre_qty_lock_5063863_7836")
    # redis_client.delete("stock_init_pre_qty_lock_3215494_595")
    # redis_client.delete("stock_init_pre_qty_lock_5021462_6976")

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
    lock_key = get_pre_qty_lock_key(5021462, 6976)

    redis_client = get_cluster_client()
    print(redis_client.get(lock_key))
    redis_client.delete(lock_key)
