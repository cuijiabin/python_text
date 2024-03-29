"""
订单转仓过滤
"""
from collections import Counter
from string import Template

import util as bm


# 获取订单列表
def get_order_info(code_list):
    code_list = list(map(lambda x: "'" + str(x) + "'", code_list))
    code_list = ','.join(code_list)
    sql_tmp = Template(
        "select id,order_code,`status`,wdgj_status,oms_sync_status,warehouse_id,channel,brand_channel "
        "from orders WHERE order_code IN ($code_list)")
    sql = sql_tmp.substitute(code_list=code_list)

    return bm.get_mia_db_data(sql)


# 获取订单明细列表
def get_order_item_info(id_list):
    str_list = list(map(lambda x: str(x), id_list))
    sql_tmp = Template(
        "SELECT id,order_id,warehouse_id,item_id,spu_id "
        "from order_item WHERE order_id IN ($id_list)")
    sql = sql_tmp.substitute(id_list=','.join(str_list))

    return bm.get_mia_db_data(sql)


# bmp库存信息查询
def get_bmp_stock_info(channel_id, item_id, spu_id, warehouse_id):
    sql_tmp = Template(
        "SELECT * from brand_stock_item_channel WHERE channel_id = $channel_id and item_id = $item_id "
        "AND tz_item_id = $tz_item_id")
    sql = sql_tmp.substitute(channel_id=channel_id, item_id=item_id, tz_item_id=spu_id)
    if warehouse_id > 0:
        sql += " AND warehouse_id = " + str(warehouse_id)
        
    return bm.get_mia_db_data(sql, "mia_bmp")


# 默认渠道库存转仓
def gen_bmp_update_sql(item_list, order_code):
    # print("-- 默认渠道库存转仓")
    return_list = []
    bmp_map = dict()
    for item in item_list:
        default_bmp = get_bmp_stock_info(1, item['item_id'], 0, item['warehouse_id'])
        d_bmp = default_bmp[0]
        return_list.append(d_bmp['id'])
        bmp_map[d_bmp['id']] = d_bmp

    return_map = dict(Counter(return_list))
    # sql_tmp = Template("update brand_stock_item_channel set stock_quantity = stock_quantity$num where id = $id;")
    t_list = []
    w_set = set()
    for bmp_id, num in return_map.items():
        d_bmp = bmp_map.get(bmp_id)
        default_bmp = get_bmp_stock_info(1, d_bmp['item_id'], 0, 0)
        print("商品", d_bmp['item_id'], "处理")
        w_list = []
        for bb in default_bmp:
            if bb['id'] == bmp_id:
                continue
            msg = "库存不足" if bb['stock_quantity'] < num else "库存充足"
            if msg == "库存充足":
                w_list.append(bb['warehouse_id'])
            # reduce_sql = sql_tmp.substitute(id=str(bb['id']), num="-" + str(num))
            # print(bb['warehouse_id'], msg, reduce_sql, bb['stock_quantity'], bb['item_id'])
            print(bb['warehouse_id'], msg, bb['stock_quantity'], bb['item_id'])
            w_set.add(bb['warehouse_id'])

        t_list.append(w_list)

    print(t_list)
    for w in t_list:
        x = set(w)
        w_set = w_set & x
    if len(w_set) > 0:
        # print(w_set)
        print("---" + str(order_code) + "可以转仓")


# 原渠道库存转仓
def gen_original_bmp_update_sql(order_dict, item_list, order_code):
    # print("-- 原渠道库存转仓")
    return_list = []
    bmp_map = dict()
    for item in item_list:
        order_id = item['order_id']
        oo = order_dict.get(order_id)
        default_bmp = get_bmp_stock_info(oo['brand_channel'], item['item_id'], item['spu_id'], item['warehouse_id'])
        if len(default_bmp) < 1:
            # print("原路查询失败", item['item_id'], item['spu_id'], item['warehouse_id'], oo['brand_channel'])
            return
        d_bmp = default_bmp[0]
        return_list.append(d_bmp['id'])
        bmp_map[d_bmp['id']] = d_bmp

    return_map = dict(Counter(return_list))
    t_list = []
    w_set = set()
    # sql_tmp = Template("update brand_stock_item_channel set stock_quantity = stock_quantity$num where id = $id;")
    for bmp_id, num in return_map.items():
        d_bmp = bmp_map.get(bmp_id)
        default_bmp = get_bmp_stock_info(d_bmp['channel_id'], d_bmp['item_id'], d_bmp['tz_item_id'], 0)
        # print("商品", d_bmp['item_id'], d_bmp['tz_item_id'], "处理")
        w_list = []
        for bb in default_bmp:
            if bb['id'] == bmp_id:
                continue
            msg = "库存不足" if bb['stock_quantity'] < num else "库存充足"
            if msg == "库存充足":
                w_list.append(bb['warehouse_id'])
            # reduce_sql = sql_tmp.substitute(id=str(bb['id']), num="-" + str(num))
            # print(bb['warehouse_id'], msg, bb['stock_quantity'], bb['item_id'], bb['tz_item_id'])

        t_list.append(w_list)

    for w in t_list:
        x = set(w)
        w_set = w_set & x
    if len(w_set) > 0:
        # print(w_set)
        print("---" + str(order_code) + "可以转仓")


def check_convert_order(order_code):
    order_code_list = [str(order_code)]
    o_list = get_order_info(order_code_list)
    order_id_list = list(map(lambda x: x["id"], o_list))
    order_item_list = get_order_item_info(order_id_list)
    # 默认渠道库存转仓
    gen_bmp_update_sql(order_item_list, order_code)
    # 生成订单字典
    order_map = dict(zip(order_id_list, o_list))
    # 原渠道库存转仓
    gen_original_bmp_update_sql(order_map, order_item_list, order_code)


if __name__ == '__main__':
    order_list = [
        2203072489772363
    ]
    for order_code in order_list:
        print(order_code)
        check_convert_order(order_code)
