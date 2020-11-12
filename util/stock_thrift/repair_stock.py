# coding=utf-8
import requests


# 批量调取接口 select DISTINCT item_id from brand_stock_item_channel where channel_id = 1 AND tz_item_id = 0 and `status` = 1;
def reset_pre_qty(item_list):
    r = requests.get("http://10.5.105.104:9089/stock/resetPreQty?itemIdList=" + item_list)
    print(r.content.decode("utf-8"))


# 修正锁定库存接口数据
def reset_lock_qty(item_list):
    r = requests.get("http://10.5.105.104:9089/stock/resetLockQty?itemIdList=" + item_list)
    print(r.content.decode("utf-8"))


def partition_list(input_list, num):
    return [input_list[i:i + num] for i in range(0, len(input_list), num)]


if __name__ == "__main__":
    # python 列表切割 select DISTINCT item_id from brand_stock_item_channel where channel_id = 1 AND tz_item_id = 0 and `status` = 1;
    input_list = [1223100, 2426338, 2474190, 2474219, 2474245, 2474252, 2474253, 2474342]
    p_list = partition_list(input_list, 10)
    for inner in p_list:
        inner = list(map(lambda x: str(x), inner))
        item_list = ",".join(inner)
        # reset_pre_qty(item_list)
        reset_lock_qty(item_list)
