"""
订单转仓sql生成

-- 订单转仓
update orders set warehouse_id = 6868, wdgj_status = 1, oms_sync_status = 1 where id = 240678271 and warehouse_id = 7575 and wdgj_status = 2 and oms_sync_status = 3;
-- 订单明细转仓
update order_item set warehouse_id = 6868 where id = 679459348 and warehouse_id = 7575;
"""
from collections import Counter
from string import Template

import util as bm


def get_order_info(code_list):
    code_list = list(map(lambda x: "'" + str(x) + "'", code_list))
    code_list = ','.join(code_list)
    cur = bm.get_mia_cursor("mia")
    sql_tmp = Template(
        "select id,order_code,`status`,wdgj_status,oms_sync_status,warehouse_id,channel,brand_channel "
        "from orders WHERE order_code IN ($code_list)")
    sql = sql_tmp.substitute(code_list=code_list)
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return rows


def get_order_item_info(id_list):
    str_list = list(map(lambda x: str(x), id_list))
    cur = bm.get_mia_cursor("mia")
    sql_tmp = Template(
        "SELECT id,order_id,warehouse_id,item_id,spu_id "
        "from order_item WHERE order_id IN ($id_list)")
    sql = sql_tmp.substitute(id_list=','.join(str_list))
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return rows


def gen_update_order_sql(order_list, target_warehouse_id):
    print("-- 订单转仓")
    sql_tmp = Template(
        "update orders set warehouse_id = $target_warehouse, wdgj_status = 1, oms_sync_status = 1 where "
        "id = $order_id and warehouse_id = $pre_warehouse and wdgj_status = $ws and oms_sync_status = $os;")
    for order in order_list:
        sql = sql_tmp.substitute(target_warehouse=str(target_warehouse_id),
                                 order_id=str(order['id']),
                                 pre_warehouse=str(order['warehouse_id']),
                                 ws=str(order['wdgj_status']),
                                 os=str(order['oms_sync_status']))
        print(sql)


def gen_update_item_sql(item_list, target_warehouse_id):
    print("-- 订单明细转仓")
    sql_tmp = Template(
        "update order_item set warehouse_id = $target_warehouse "
        "where id = $order_item_id and warehouse_id = $pre_warehouse;")
    for item in item_list:
        sql = sql_tmp.substitute(target_warehouse=str(target_warehouse_id),
                                 order_item_id=str(item['id']),
                                 pre_warehouse=str(item['warehouse_id']))
        print(sql)


# bmp库存信息查询
def get_bmp_stock_info(channel_id, item_id, spu_id, warehouse_id):
    cur = bm.get_mia_cursor("mia_bmp")
    sql_tmp = Template(
        "SELECT * from brand_stock_item_channel WHERE channel_id = $channel_id and item_id = $item_id "
        "AND tz_item_id = $tz_item_id")
    sql = sql_tmp.substitute(channel_id=channel_id, item_id=item_id, tz_item_id=spu_id)
    if warehouse_id > 0:
        sql += " AND warehouse_id = " + str(warehouse_id)
    cur.execute(sql)
    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return rows


def gen_bmp_update_sql(item_list):
    print("-- bmp库存处理")
    print("-- 订单转仓")
    return_list = []
    bmp_map = dict()
    for item in item_list:
        default_bmp = get_bmp_stock_info(1, item['item_id'], 0, item['warehouse_id'])
        d_bmp = default_bmp[0]
        return_list.append(d_bmp['id'])
        bmp_map[d_bmp['id']] = d_bmp

    return_map = dict(Counter(return_list))
    sql_tmp = Template("update brand_stock_item_channel set stock_quantity = stock_quantity$num where id = $id;")
    for bmp_id, num in return_map.items():
        sql = sql_tmp.substitute(id=str(bmp_id), num="+" + str(num))
        # print(sql)
        print("默认扣减")
        d_bmp = bmp_map.get(bmp_id)
        default_bmp = get_bmp_stock_info(1, d_bmp['item_id'], 0, 0)
        for bb in default_bmp:
            if bb['id'] == bmp_id:
                continue
            msg = "库存不足" if bb['stock_quantity'] < num else "库存充足"
            reduce_sql = sql_tmp.substitute(id=str(bb['id']), num="-" + str(num))
            print(reduce_sql, msg, bb['warehouse_id'], bb['stock_quantity'], bb['item_id'], bb['tz_item_id'])


# 原路退还sql
def gen_original_bmp_update_sql(order_dict, item_list):
    print("-- bmp库存原路处理")
    print("-- 订单转仓")
    # print(order_dict)
    return_list = []
    bmp_map = dict()
    for item in item_list:
        order_id = item['order_id']
        oo = order_dict.get(order_id)
        default_bmp = get_bmp_stock_info(oo['brand_channel'], item['item_id'], item['spu_id'], item['warehouse_id'])
        if len(default_bmp) < 1:
            print("原路查询失败")
            return
        d_bmp = default_bmp[0]
        return_list.append(d_bmp['id'])
        bmp_map[d_bmp['id']] = d_bmp

    return_map = dict(Counter(return_list))
    sql_tmp = Template("update brand_stock_item_channel set stock_quantity = stock_quantity$num where id = $id;")
    for bmp_id, num in return_map.items():
        # sql = sql_tmp.substitute(id=str(bmp_id), num="+" + str(num))
        # print(sql)
        print("渠道扣减")
        d_bmp = bmp_map.get(bmp_id)
        default_bmp = get_bmp_stock_info(d_bmp['channel_id'], d_bmp['item_id'], d_bmp['tz_item_id'], 0)
        for bb in default_bmp:
            if bb['id'] == bmp_id:
                continue
            msg = "库存不足" if bb['stock_quantity'] < num else "库存充足"
            reduce_sql = sql_tmp.substitute(id=str(bb['id']), num="-" + str(num))
            print(reduce_sql, msg, bb['warehouse_id'], bb['stock_quantity'], bb['item_id'], bb['tz_item_id'])


if __name__ == '__main__':
    order_code_list = ['2111232466650093']
    # 获取订单列表
    o_list = get_order_info(order_code_list)
    # 获取明细列表
    order_id_list = list(map(lambda x: x["id"], o_list))
    order_item_list = get_order_item_info(order_id_list)
    # 默认渠道库存归还
    gen_bmp_update_sql(order_item_list)
    # 生成订单字典
    order_map = dict(zip(order_id_list, o_list))
    # 原路库存归还
    gen_original_bmp_update_sql(order_map, order_item_list)

    # 确定目标仓库后生成转仓sql
    # gen_update_order_sql(o_list, 6868)
    # gen_update_item_sql(order_item_list, 6868)
