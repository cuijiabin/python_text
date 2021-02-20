import json

import util as bm
from string import Template

target_warehouse_map = {
    6868: 3364,
    7575: 3364
}


# 根据仓库id获取可用库存列表
def get_order_list():
    cur = bm.get_mia_cursor("mia_mirror")
    # sql = "select id, order_code, warehouse_id from orders WHERE order_code in ('2012052398902155') and `status` !=6"
    sql = "select DISTINCT o.id, o.order_code,o.warehouse_id from orders o LEFT JOIN order_item t on o.id = t.order_id " + \
          "where o.order_time>'2021-1-4' and t.spu_id=5876088 and o.`status`<3 AND o.warehouse_id in (6868,7575)"
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    return rows


# 更新订单sql生成
def gen_update_order_sql(rows):
    order_warehouse_map = {}
    sql_tmp = Template("update orders set warehouse_id = $wid where id = $id and warehouse_id = $pre_wid;")
    for o in rows:
        wid = target_warehouse_map[o["warehouse_id"]]
        order_warehouse_map.setdefault(o["order_code"], wid)
        print(sql_tmp.substitute(id=o["id"], wid=wid, pre_wid=o["warehouse_id"]))

    return order_warehouse_map


# 订单商品列表查询
def get_order_item_list(order_ids):
    cur = bm.get_mia_cursor("mia_mirror")
    sql = "select id,order_id,item_id,warehouse_id,stock_item_id from order_item where order_id in (%s)"
    condition = ", ".join(list(map(lambda x: str(x), order_ids)))
    sql %= condition
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    return rows


# 库存信息查询
def get_stock_item_list(item_ids):
    cur = bm.get_mia_cursor("mia_mirror")
    sql = "select id,item_id,warehouse_id from stock_item where item_id in (%s)"
    condition = ", ".join(list(map(lambda x: str(x), item_ids)))
    sql %= condition
    sql += " and status = 1"
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    stock_map = {}
    for x in rows:
        stock_map.setdefault(str(x["item_id"]) + "#" + str(x["warehouse_id"]), x["id"])
    return stock_map


# 更新订单商品sql生成
def gen_update_order_item_sql(order_item_list, stock_map):
    sql_tmp = Template(
        "update order_item set warehouse_id = $wid, stock_item_id = $stock_item_id where id = $id and warehouse_id = $pre_wid and stock_item_id = $pre_stock_id;")

    sql_tmp_zero = Template(
        "update order_item set warehouse_id = $wid where id = $id and warehouse_id = $pre_wid;")
    order_item_map = {}
    for order_item in order_item_list:
        item_id = order_item["item_id"]
        wid = target_warehouse_map[order_item["warehouse_id"]]

        if order_item["stock_item_id"] == 0:
            # print("item_id new stock_item_id is 0 " + json.dumps(order_item))
            print(sql_tmp_zero.substitute(id=order_item["id"], wid=wid, pre_wid=order_item["warehouse_id"]))
            continue
        else:
            stock_key = str(item_id) + "#" + str(wid)
            stock_item_id = stock_map.get(stock_key)
            if stock_item_id is None:
                print("item_id new stock_item_id is null " + json.dumps(order_item))
                continue
            else:
                print(sql_tmp.substitute(id=order_item["id"], wid=wid, stock_item_id=stock_item_id,
                                         pre_wid=order_item["warehouse_id"], pre_stock_id=order_item["stock_item_id"]))
                continue

        order_item_map.setdefault(order_item["id"], wid)

    return order_item_map


# 退货单列表查询
def get_returns_list(order_item_ids):
    cur = bm.get_mia_cursor("mia_mirror")
    sql = "select id, order_code, warehouse_id from returns where order_code in (%s)"
    condition = ", ".join(list(map(lambda x: "'" + str(x) + "'", order_item_ids)))
    sql %= condition
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    return rows


def gen_returns_sql(return_list, order_warehouse_map):
    sql_tmp = Template("update returns set warehouse_id = $wid where id = $id;")
    for o in return_list:
        wid = order_warehouse_map.get(o["order_code"])
        print(sql_tmp.substitute(id=o["id"], wid=wid))


# 预售商品查询
def get_order_presell_item_list(order_code_list):
    cur = bm.get_mia_cursor("mia_mirror")
    sql = "select id, order_item_id, warehouse_id from order_presell_item where order_item_id in (%s)"
    condition = ", ".join(list(map(lambda x: "'" + str(x) + "'", order_code_list)))
    sql %= condition
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    return rows


def get_return_items_list(order_code_list):
    cur = bm.get_mia_cursor("mia_mirror")
    sql = "select id, order_item_id, warehouse_id from return_items where order_item_id in (%s)"
    condition = ", ".join(list(map(lambda x: "'" + str(x) + "'", order_code_list)))
    sql %= condition
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    return rows


def get_return_process_item_list(order_code_list):
    cur = bm.get_mia_cursor("mia_mirror")
    sql = "select id, order_item_id, warehouse_id from return_process_item where order_item_id in (%s)"
    condition = ", ".join(list(map(lambda x: "'" + str(x) + "'", order_code_list)))
    sql %= condition
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    return rows


def gen_update_detail_sql(item_list, table_name, order_item_map):
    sql_tmp = Template("update " + table_name + " set warehouse_id = $wid where id = $id;")
    for o in item_list:
        wid = order_item_map.get(o["order_item_id"])
        print(sql_tmp.substitute(id=o["id"], wid=wid))


if __name__ == '__main__':
    order_list = get_order_list()
    order_ids = list(map(lambda x: x['id'], order_list))
    order_code_list = list(map(lambda x: x['order_code'], order_list))
    print("-- orders update sql")
    order_warehouse_map = gen_update_order_sql(order_list)

    order_item_list = get_order_item_list(order_ids)
    item_ids = list(map(lambda x: x['item_id'], order_item_list))
    stock_map = get_stock_item_list(item_ids)
    print("-- order_item update sql")
    order_item_map = gen_update_order_item_sql(order_item_list, stock_map)

    # order_item_ids = list(map(lambda x: x['id'], order_item_list))
    # # 预售商品查询
    # order_presell_item_list = get_order_presell_item_list(order_item_ids)
    # if len(order_presell_item_list) > 0:
    #     print("-- order_presell_item update sql")
    #     gen_update_detail_sql(order_presell_item_list, "order_presell_item", order_item_map)

    # 退货单查询
    # return_list = get_returns_list(order_code_list)
    # if len(return_list) > 0:
    #     print("-- returns update sql")
    #     gen_returns_sql(return_list, order_warehouse_map)

    # 退货商品查询
    # return_items_list = get_return_items_list(order_item_ids)
    # if len(return_items_list) > 0:
    #     print("-- return_items update sql")
    #     gen_update_detail_sql(return_items_list, "return_items", order_item_map)

    # 售后退货处理详细表查询
    # return_process_item_list = get_return_process_item_list(order_item_ids)
    # if len(return_process_item_list) > 0:
    #     print("-- return_process_item update sql")
    #     gen_update_detail_sql(return_process_item_list, "return_process_item", order_item_map)
