# coding=utf-8
from itertools import groupby
from string import Template

import util as bm
import util.common_request as crr


# bmp渠道库存分配
def test_zero_bmp_stock():
    b_param = {
        "warehouseId": 3364,
        "userId": 9999,
        "sourceList": [{
            "brandChannel": 10,
            "itemId": 6107864,
            "qty": 6,
            "tzItemId": 0
        }],
        "targetList": [{
            "brandChannel": 264,
            "itemId": 6107864,
            "qty": 6,
            "tzItemId": 0
        }]
    }
    api_url = "http://api.gateway.miaidc.com/order-stock-service-api/stockBmp/bmpDistributeStockQty"
    crr.common_stock_api(b_param, api_url)


# 渠道库存清零
def clear_bmp_stock(item_id, tz_item_id, warehouse_id, channel_id):
    sql_tmp = Template(
        "SELECT item_id,warehouse_id,channel_id,tz_item_id,stock_quantity,`status` "
        "from brand_stock_item_channel "
        "where channel_id = $channel_id and warehouse_id = $warehouse_id "
        "and item_id = $item_id and tz_item_id = $tz_item_id and stock_quantity > 0"
    )
    sql = sql_tmp.substitute(item_id=item_id, tz_item_id=tz_item_id, channel_id=channel_id, warehouse_id=warehouse_id)

    rows = bm.get_mia_db_data(sql, "mia_bmp")

    if len(rows) < 1:
        print("无相关数据")
        return

    source_list = []
    target_list = []
    for row in rows:
        qty = row["stock_quantity"]
        source_list.append({
            "brandChannel": channel_id,
            "itemId": row["item_id"],
            "qty": qty,
            "tzItemId": row["tz_item_id"]
        })

        target_list.append({
            "brandChannel": 1,
            "itemId": row["item_id"],
            "qty": qty,
            "tzItemId": 0
        })

    b_param = {
        "warehouseId": warehouse_id,
        "userId": 9999,
        "sourceList": source_list,
        "targetList": target_list
    }

    api_url = "http://api.gateway.miaidc.com/order-stock-service-api/stockBmp/bmpDistributeStockQty"
    crr.common_stock_api(b_param, api_url)
    return


'''
-- 未迁移的私域库存数据参数组装
SELECT concat("(",item_id,",",tz_item_id,",",warehouse_id,",",channel_id,")"),lastmodified_date,stock_quantity,item_id,tz_item_id,id
from brand_stock_item_channel 
WHERE channel_id IN (
228,229
) 
AND stock_quantity > 0 
AND `status` = 1
ORDER BY lastmodified_date DESC;

'''


def get_transfer_pd_list():
    sql_tmp = Template(
        "SELECT DISTINCT item_id,tz_item_id,warehouse_id,channel_id "
        "FROM brand_stock_item_channel "
        "WHERE channel_id != 1 "
        "AND stock_quantity = 0 AND `status` = 1 AND warehouse_id = 6868 ORDER BY lastmodified_date DESC"
    )
    sql = sql_tmp.substitute()
    return bm.get_mia_db_data(sql, "mia_bmp")


# bmp库存数据刷库相关的操作内容
if __name__ == "__main__":
    stock_list = get_transfer_pd_list()

    for k, g in groupby(stock_list, lambda x: x["channel_id"]):
        print(k)
        print(list(g))
