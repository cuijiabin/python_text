"""
订单转仓过滤
"""
from collections import Counter
from string import Template

import pymysql


def get_mia_cursor(db_name="mia"):
    conn = pymysql.connect(host="10.5.96.80",
                           port=3306,
                           user="pop_cuijiabin",
                           passwd="8dtx5EOUZASc#",
                           db=db_name,
                           charset="utf8")
    return conn.cursor()


# 获取订单列表
def get_order_info(code_list):
    code_list = list(map(lambda x: "'" + str(x) + "'", code_list))
    code_list = ','.join(code_list)
    cur = get_mia_cursor("mia")
    sql_tmp = Template(
        "select id,order_code,`status`,wdgj_status,oms_sync_status,warehouse_id,channel,brand_channel "
        "from orders WHERE order_code IN ($code_list)")
    sql = sql_tmp.substitute(code_list=code_list)
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return rows


# 获取订单明细列表
def get_order_item_info(id_list):
    str_list = list(map(lambda x: str(x), id_list))
    cur = get_mia_cursor("mia")
    sql_tmp = Template(
        "SELECT id,order_id,warehouse_id,item_id,spu_id "
        "from order_item WHERE order_id IN ($id_list)")
    sql = sql_tmp.substitute(id_list=','.join(str_list))
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return rows


# bmp库存信息查询
def get_bmp_stock_info(channel_id, item_id, spu_id, warehouse_id):
    cur = get_mia_cursor("mia_bmp")
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


# 默认渠道库存转仓
def gen_bmp_update_sql(item_list):
    print("-- 默认渠道库存转仓")
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
        d_bmp = bmp_map.get(bmp_id)
        default_bmp = get_bmp_stock_info(1, d_bmp['item_id'], 0, 0)
        print("商品", d_bmp['item_id'], "处理")
        for bb in default_bmp:
            if bb['id'] == bmp_id:
                continue
            msg = "库存不足" if bb['stock_quantity'] < num else "库存充足"
            reduce_sql = sql_tmp.substitute(id=str(bb['id']), num="-" + str(num))
            print(bb['warehouse_id'], msg, reduce_sql, bb['stock_quantity'], bb['item_id'])


# 原渠道库存转仓
def gen_original_bmp_update_sql(order_dict, item_list):
    print("-- 原渠道库存转仓")
    return_list = []
    bmp_map = dict()
    for item in item_list:
        order_id = item['order_id']
        oo = order_dict.get(order_id)
        default_bmp = get_bmp_stock_info(oo['brand_channel'], item['item_id'], item['spu_id'], item['warehouse_id'])
        if len(default_bmp) < 1:
            print("原路查询失败", item['item_id'], item['spu_id'], item['warehouse_id'], oo['brand_channel'])
            return
        d_bmp = default_bmp[0]
        return_list.append(d_bmp['id'])
        bmp_map[d_bmp['id']] = d_bmp

    return_map = dict(Counter(return_list))
    sql_tmp = Template("update brand_stock_item_channel set stock_quantity = stock_quantity$num where id = $id;")
    for bmp_id, num in return_map.items():
        d_bmp = bmp_map.get(bmp_id)
        default_bmp = get_bmp_stock_info(d_bmp['channel_id'], d_bmp['item_id'], d_bmp['tz_item_id'], 0)
        print("商品", d_bmp['item_id'], d_bmp['tz_item_id'], "处理")
        for bb in default_bmp:
            if bb['id'] == bmp_id:
                continue
            msg = "库存不足" if bb['stock_quantity'] < num else "库存充足"
            reduce_sql = sql_tmp.substitute(id=str(bb['id']), num="-" + str(num))
            print(bb['warehouse_id'], msg, reduce_sql, bb['stock_quantity'], bb['item_id'], bb['tz_item_id'])


def check_convert_order(order_code):
    order_code_list = [str(order_code)]
    o_list = get_order_info(order_code_list)
    order_id_list = list(map(lambda x: x["id"], o_list))
    order_item_list = get_order_item_info(order_id_list)
    # 默认渠道库存转仓
    gen_bmp_update_sql(order_item_list)
    # 生成订单字典
    order_map = dict(zip(order_id_list, o_list))
    # 原渠道库存转仓
    gen_original_bmp_update_sql(order_map, order_item_list)


if __name__ == '__main__':
    order_list = [2111192465793983, 2111232466572251, 2111232466589393, 2111102463501095, 2111232466650093]
    for order_code in order_list:
        print(order_code)
        check_convert_order(order_code)
