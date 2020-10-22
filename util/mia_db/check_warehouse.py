import json

import util as bm
from string import Template

target_warehouse_map = {
    8100: 6868,
    8103: 7575,
    8104: 6868,
    8105: 3364,
    8106: 40,
    8117: 40,
    8131: 40,
    8132: 3364,
    8133: 6868,
    8134: 7575,
    8135: 40,
    8136: 3364,
    8137: 6868,
    8138: 7575,
    8156: 40,
    8157: 3364,
    8158: 6868,
    8159: 7575
}


# 根据仓库id获取可用库存列表
def get_order_list():
    cur = bm.get_mia_cursor("mia_mirror")
    sql = "select id,item_id,warehouse_id,stock_quantity from stock_item WHERE warehouse_id IN(40,96,3364,3928,6868,6869,7575,7576) AND status = 1 and modify_time > '2020-08-10 18:00' ORDER BY modify_time ASC"
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    return rows


# 库存信息查询
def get_bmp_stock(stock):
    cur = bm.get_mia_cursor("mia_bmp")
    sql = "SELECT id, stock_quantity FROM `brand_stock_item_channel` where item_id = " + str(
        stock["item_id"]) + " and  warehouse_id = " + str(stock["warehouse_id"]) + " and channel_id = 10"
    sql += " and status = 1"
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    print(stock, rows)


# 更新订单商品sql生成
def check_stock(stock_list):
    for stock in stock_list:
        get_bmp_stock(stock)


if __name__ == '__main__':
    # 正向验证
    stock_list = get_order_list()
    check_stock(stock_list)
