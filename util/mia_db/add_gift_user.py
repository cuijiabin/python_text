from collections import Counter
from string import Template

import util as bm


# 父单下商品统计
def get_all_info(superior_order_code):
    cur = bm.get_mia_cursor("mia")
    sql_tmp = Template(
        "SELECT "
        "IF(item_info.spu_id=0,0,1) AS is_spu, "
        "IF(item_info.spu_id=0, item_info.item_id, item_info.spu_id) AS item_id, "
        "IF(item_info.spu_id=0, item_info.qty, ROUND(item_info.qty/item_info.item_amount)) AS item_count, "
        "sum(item_info.pay_price) AS pay_price "
        "FROM ( "
        "SELECT oi.spu_id, oi.item_id,ssr.item_amount,count(oi.id) AS qty,sum(oi.pay_price) AS pay_price "
        "FROM orders o "
        "INNER JOIN order_item oi ON  o.id=oi.order_id "
        "LEFT JOIN spu_sku_relation ssr ON ssr.spu_id=oi.spu_id AND ssr.item_id=oi.item_id "
        "WHERE o.superior_order_code in( '$superior_order_code') AND o.status != 6 "
        "AND (oi.spu_id in (6200688, 6200689, 6200690, 6200691, 6200692, 6200693, 6200694, 6200695, 6200696, 6200697, 6200698, 6200699, 6200700, 6200701, 6200702, 6200703) "
        " OR (oi.item_id IN (123 ) AND oi.spu_id = 0) "
        ")"
        "GROUP BY oi.spu_id,oi.item_id "
        ") item_info "
        "GROUP BY item_info.spu_id "
        # "GROUP BY item_info.spu_id,item_info.item_id "
        "ORDER BY item_id ASC")
    sql = sql_tmp.substitute(superior_order_code=superior_order_code)
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return rows


# 达人名称获取
def get_tiktok_alliance_info(superior_order_code):
    cur = bm.get_mia_cursor("mia")
    sql_tmp = Template(
        "SELECT superior_order_code,author_id,author_account,room_id "
        "FROM third_tiktok_alliance_info "
        "WHERE superior_order_code = '$superior_order_code' AND author_id > 0"
    )
    sql = sql_tmp.substitute(superior_order_code=superior_order_code)
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return rows


# 客服备注获取
def get_customer_alliance_info(superior_order_code):
    cur = bm.get_mia_cursor("mia")
    sql_tmp = Template(
        "SELECT REPLACE(REPLACE(REPLACE(GROUP_CONCAT(l.dscrp),CHAR(9),''),CHAR(10),''),CHAR(13),'') AS dd FROM `order_dscrp_log` l "
        "LEFT JOIN orders o on l.order_code = o.order_code "
        "WHERE o.superior_order_code = '$superior_order_code' AND l.admin_id != 10000 GROUP BY o.superior_order_code"
    )
    sql = sql_tmp.substitute(superior_order_code=superior_order_code)
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return rows


# 仓库信息获取
def get_warehouse_info(superior_order_code):
    cur = bm.get_mia_cursor("mia")
    sql_tmp = Template(
        # "SELECT DISTINCT ooc.open_order_id,sw.id,sw.`name`,o.dst_province,o.dst_city,o.dst_area,o.order_time,o.push_time,pds.deliver_time "
        "SELECT DISTINCT ooc.open_order_id,sw.id,sw.`name` "
        "from open_order_channel ooc LEFT JOIN orders o on ooc.superior_order_code = o.superior_order_code "
        "LEFT JOIN stock_warehouse sw on o.warehouse_id = sw.id "
        # "LEFT JOIN parent_dst_sheet pds on pds.order_id = o.id "
        "WHERE ooc.open_order_id = '$superior_order_code' OR ooc.open_order_id = '$superior_order_code_b'"
    )
    sql = sql_tmp.substitute(superior_order_code=superior_order_code,
                             superior_order_code_b=str(superior_order_code) + 'A')
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return rows


# 订单渠道获取
def get_channel_info(order_code):
    cur = bm.get_mia_cursor("mia")
    sql_tmp = Template(
        "SELECT o.brand_channel,sw.channel_name,o.order_code "
        "FROM orders o "
        "LEFT JOIN mia_bmp.brand_order_channel sw on o.brand_channel = sw.channel_id "
        "WHERE o.order_code = '$order_code' limit 1"
    )
    sql = sql_tmp.substitute(order_code=order_code)
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return rows


# 订单物流单号获取
def get_third_dst_info(order_code):
    cur = bm.get_mia_cursor("mia")
    sql_tmp = Template(
        "SELECT tor.third_order_code, GROUP_CONCAT(DISTINCT o.order_code) as order_code,GROUP_CONCAT(DISTINCT pds.sheet_code) as sheet_code "
        "from third_order_relation tor "
        "LEFT JOIN orders o ON o.order_code = tor.order_code "
        "LEFT JOIN parent_dst_sheet pds ON o.id = pds.order_id "
        "WHERE tor.third_order_code = '$order_code' GROUP BY tor.third_order_code"
    )
    sql = sql_tmp.substitute(order_code=order_code)
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return rows


# 物流相关数据导出功能。
if __name__ == '__main__':
    # print("订单号,交易流水号,收货人,手机号,省,市,区,街道,地址,订单总支付金额,总邮费,总税费,商品ID,单个销售价,数量,单个税费,仓库id,身份证号,真实姓名,身份证正面,身份证反面,客户备注,支付方式")
    ss = [
        '202112262473807353'
    ]
    for s in ss:
        spu_info = get_all_info(s)
        pay_price = 0.0
        has_gift_sku = []
        for spp in spu_info:
            pay_price += spp["pay_price"]
            item_id = spp["item_id"]
            num = int(spp["item_count"])
            for i in range(num):
                has_gift_sku.append(item_id)

        print(str(dict(Counter(has_gift_sku))) + "\t" + str(pay_price) + "\t" + str(len(has_gift_sku)))
    # for s in ss:
    #     spu_info = get_tiktok_alliance_info(str(s))
    #     # spu_info = get_customer_alliance_info(str(s))
    #     if len(spu_info) > 0:
    #         info = spu_info[0]
    #         print(str(info['author_id']) + "\t" + str(info['author_account']))
    #         # print(str(info['dd']))
    #     else:
    #         print("\t")
    # # for s in ss:
    #     spu_info = get_warehouse_info(str(s))
    #     if len(spu_info) > 0:
    #         info = spu_info[0]
    #         # deliver_time = info['deliver_time']
    #         # if deliver_time is None:
    #         #     deliver_time = ""
    #         # print(str(info['dst_province']) + "\t" + str(info['dst_city']) + "\t" + str(info['dst_area']) + "\t" + str(
    #         #     info['order_time']) + "\t" + str(info['push_time']) + "\t" + str(deliver_time))
    #
    #         print(str(info['id']) + "\t" + str(info['name']))
    #     else:
    #         print("\t")

    # for s in ss:
    #     spu_info = get_third_dst_info(str(s))
    #     if len(spu_info) > 0:
    #         info = spu_info[0]
    #         order_code = info['order_code']
    #         sheet_code = info['sheet_code']
    #         if order_code is None:
    #             order_code = ""
    #
    #         if sheet_code is None:
    #             sheet_code = ""
    #         # print(str(info['id']) + "\t" + str(info['name']) + "\t" + str(express_name) + "\t" + str(sheet_code))
    #         # print(str(dst_address) + "\t" + str(info['id']) + "\t" + str(info['name']))
    #         print(str(order_code) + "\t" + str(sheet_code))
    #         # print(str(sheet_code))
    #     else:
    #         print("\t")

    # for s in ss:
    #     spu_info = get_channel_info(str(s))
    #     if len(spu_info) > 0:
    #         info = spu_info[0]
    #         print(str(info['brand_channel']) + "\t" + str(info['channel_name']))
    #         # print(str(sheet_code))
    #     else:
    #         print("\t")
