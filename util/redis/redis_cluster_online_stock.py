# coding=utf-8
import util as bm


def gen_stock_key(item_id):
    return "stock_" + str(item_id)


def gen_change_key(item_id):
    return "stock_" + str(item_id) + "_incr"


def gen_pre_qty_lock_key(item_id, wid):
    return "stock_init_pre_qty_lock_" + str(item_id) + "_" + str(wid)


# 获取预占的filed
def gen_pre_qty_field(wid):
    return "wid_" + str(wid) + "_preQty"


# 获取库存数量的filed
def gen_qty_field(wid):
    return "wid_" + str(wid) + "_qty"


# 根据itemId 删除redis库存
def delete_stock(item_id):
    redis_client = bm.get_stock_cluster_client()

    stock_key = gen_stock_key(item_id)
    change_key = gen_change_key(item_id)

    print(redis_client.hgetall(stock_key))
    print(redis_client.hgetall(change_key))

    redis_client.delete(stock_key)
    redis_client.delete(change_key)


# 根据itemId 获取redis库存
def get_stock(item_id):
    redis_client = bm.get_stock_cluster_client()
    stock_key = gen_stock_key(item_id)
    change_key = gen_change_key(item_id)

    print(redis_client.hgetall(stock_key))
    print(redis_client.hgetall(change_key))


if __name__ == '__main__':
    # delete_stock(3070146)
    get_stock(3070005)
