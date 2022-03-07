import pymysql
from string import Template
from collections import Counter

global_spu_map = {
    5565870: 5676564,
    2485877: 5676564,
    2486004: 5676563,
    5767854: 5676562,
    5565871: 5676561,
    5766953: 5676564,
    2526700: 5676560,
    5766183: 5676559,
    5565877: 5676558
}

global_multi_spu_map = {
    5766952: [5096238, 5096239],
    5776537: [5096239, 5096240],
    5776042: [5096235, 5096236]
}


def get_mia_cursor(db_name="mia"):
    conn = pymysql.connect(host="10.5.96.80",
                           port=3306,
                           user="pop_cuijiabin",
                           passwd="8dtx5EOUZASc#",
                           db=db_name,
                           charset="utf8")
    return conn.cursor()


def get_superior_order_list():
    cur = get_mia_cursor("mia")

    sql = "SELECT tmp.user_id  AS userId , count(tmp.superior_order_code) as orderCount,GROUP_CONCAT(tmp.superior_order_code) as orderCodeList,  " + \
          "sum(tmp.orderItemNum) as orderItemNum,tmp.dst_info as dstInfo from  " + \
          "(SELECT o.superior_order_code, o.user_id, count(oi.id) AS orderItemNum,sum(oi.pay_price) AS pay_price, " + \
          "  CONCAT(o.user_id,o.dst_name,o.dst_mobile,o.dst_province,o.dst_city,o.dst_area,o.dst_street,o.dst_address) as dst_info " + \
          "FROM orders o LEFT JOIN order_item oi ON o.id = oi.order_id " + \
          "WHERE o.order_time > '2021-01-05 14:00' and o.`status` < 6  and o.channel = 211 " + \
          "AND oi.spu_id IN ( 5565870, 2485877, 2486004, 5767854, 5565871, 5766953, 5766952, 5776537, 2526700, 5766183, 5565877, 5776042) " + \
          "GROUP BY o.superior_order_code ORDER BY o.user_id ASC) tmp " + \
          "GROUP BY tmp.dst_info having orderItemNum >=8 ORDER BY orderCount DESC"
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()

    return rows


def get_gift_info(superior_order_code):
    cur = get_mia_cursor("mia")
    sql_tmp = Template(
        "select spu_id,count(id) DIV 4 as num from order_item WHERE order_id in "
        "(select id from orders WHERE superior_order_code in ($superior_order_code)) "
        "and spu_id in (5565870, 2485877, 2486004, 5767854, 5565871, 5766953, 5766952, 5776537, 2526700, 5766183, 5565877, 5776042) "
        "GROUP BY spu_id")
    sql = sql_tmp.substitute(superior_order_code=superior_order_code)
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return rows


def get_base_info(superior_order_code):
    cur = get_mia_cursor("mia")
    sql_tmp = Template(
        "SELECT DISTINCT oc.open_order_id AS open_order_id, o.superior_order_code, o.transaction_id, o.dst_name,o.dst_mobile,"
        "o.dst_province,o.dst_city,o.dst_area,o.dst_street,o.dst_address,o.warehouse_id,o.pay_mode "
        "from orders o LEFT JOIN open_order_channel oc on o.superior_order_code = oc.superior_order_code "
        "WHERE o.superior_order_code = $superior_order_code")
    sql = sql_tmp.substitute(superior_order_code=superior_order_code)
    cur.execute(sql)
    result_data = cur.fetchall()
    if len(result_data) > 0:
        return result_data[0]
    return None


def get_sub_base_info(superior_order_code):
    cur = get_mia_cursor("mia")
    sql_tmp = Template(
        "select GROUP_CONCAT(order_code) from orders "
        "WHERE superior_order_code in ($superior_order_code)")
    sql = sql_tmp.substitute(superior_order_code=superior_order_code)
    cur.execute(sql)
    result_data = cur.fetchall()
    if len(result_data) > 0:
        return result_data[0][0]
    return None


def get_gift_result():
    superior_order_list = get_superior_order_list()
    for superior_order in superior_order_list:
        superior_order_code = superior_order["orderCodeList"]
        s_list = list(map(lambda x: "'" + str(x) + "'", superior_order_code.split(",")))
        s_order_code = s_list[0]
        base_info = get_base_info(s_order_code)
        if base_info[0] is None:
            continue
        code_lists = ','.join(s_list)
        # sub_info = get_sub_base_info(code_lists)
        # convert_sub_info = sub_info.replace(",", "、")
        # t_code = base_info[0]
        # t_code = t_code + "B"
        # os_list = sub_info.split(",")
        # for os in os_list:
        #     print(os, ",", "2021-1-5抖音直播间购买拉拉裤/纸尿裤同地址超过8包补发赠品，补发新订单号抖音号：" + t_code + "； 同地址订单号：" + convert_sub_info)

        spu_list = get_gift_info(code_lists)
        for spu in spu_list:
            spu_id = spu["spu_id"]
            spu_num = spu["num"]
            if global_spu_map.get(spu_id) is not None:
                target_spu_id = global_spu_map[spu_id]
                convert_result(base_info, target_spu_id, spu_num)
            else:
                spu_id_list = global_multi_spu_map.get(spu_id)
                for target_spu_id in spu_id_list:
                    convert_result(base_info, target_spu_id, spu_num * 2)


def convert_result(base_info, target_spu_id, num):
    t_code = base_info[0]
    transaction_id = base_info[2]
    t_code = t_code + "B"
    transaction_id = transaction_id + "B"
    result = [t_code, transaction_id, base_info[3], base_info[4], base_info[5], base_info[6], base_info[7],
              base_info[8], base_info[9], "0", "0", "0", str(target_spu_id), "0", str(num), "0", "", "",
              "", "", "", "",
              str(base_info[11])]
    print(','.join(result))


def get_spu_info(superior_order_code):
    cur = get_mia_cursor("mia")
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
        "AND oi.spu_id in (6067463) "
        "GROUP BY oi.spu_id,oi.item_id "
        ") item_info "
        "GROUP BY item_info.spu_id "
        "ORDER BY item_id ASC")
    sql = sql_tmp.substitute(superior_order_code=superior_order_code)
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return rows


def get_all_info(superior_order_code):
    cur = get_mia_cursor("mia")
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


cal_map = {
    6067463: [5565956, 5565956, 5641519]
}


def get_tiktok_alliance_info(superior_order_code):
    cur = get_mia_cursor("mia")
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


def get_customer_alliance_info(superior_order_code):
    cur = get_mia_cursor("mia")
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


def get_warehouse_info(superior_order_code):
    cur = get_mia_cursor("mia")
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


def get_dst_info(order_code):
    cur = get_mia_cursor("mia")
    sql_tmp = Template(
        # "SELECT sw.id,sw.name,ec.name AS express_name,pds.sheet_code,o.order_code "
        # "SELECT tod.dst_address,sw.id,sw.name "
        "SELECT REPLACE(REPLACE(REPLACE(tod.dst_address,CHAR(9),''),CHAR(10),''),CHAR(13),'') as dst_address, sw.id "
        "FROM third_order_relation tor INNER JOIN orders o ON tor.order_code = o.order_code "
        "LEFT JOIN stock_warehouse sw on o.warehouse_id = sw.id "
        "LEFT JOIN third_order_decrypt tod on tod.third_order_code = tor.third_order_code "
        # "LEFT JOIN open_order_channel ooc on ooc.superior_order_code = o.superior_order_code "
        # "LEFT JOIN parent_dst_sheet pds on pds.order_id = o.id "
        # "LEFT JOIN express_company ec on ec.id = pds.express_id "
        # "WHERE o.order_code = '$order_code' limit 1"
        # "WHERE tor.third_child_order_code = '$order_code' limit 1"
        "WHERE tor.third_order_code = '$order_code' limit 1"
    )
    sql = sql_tmp.substitute(order_code=order_code)
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return rows


def get_channel_info(order_code):
    cur = get_mia_cursor("mia")
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


def get_third_dst_info(order_code):
    cur = get_mia_cursor("mia")
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
    # get_gift_result()
    ss = [
        '202112262473807353', '202112262473807053', '202112262473807463', '202112262473807233', '202112262473807423',
        '202112262473806983', '202112262473807073', '202112262473807083', '202112262473807753', '202112262473807323',
        '202112262473807743', '202112262473808013', '202112262473807593', '202112262473807913', '202112262473807413',
        '202112262473807693', '202112262473807873', '202112262473807833', '202112262473807393', '202112262473807103',
        '202112262473808083', '202112262473807603', '202112262473808123', '202112262473806863', '202112262473811753',
        '202112262473811773', '202112262473811853', '202112262473809363', '202112262473809253', '202112262473809373',
        '202112262473809773', '202112262473809703', '202112262473809673', '202112262473810613', '202112262473810743',
        '202112262473812093', '202112262473814053', '202112262473854503', '202112262473865503', '202112262473870703',
        '202112262473879413', '202112262473879563', '202112262473879523', '202112262473882273', '202112262473881973',
        '202112262473903043', '202112262473922733', '202112262473925243', '202112262473925803', '202112262473926703',
        '202112262473928013', '202112262473935633', '202112262473936663', '202112262473938753', '202112262473938593',
        '202112262473941463', '202112262473941363', '202112262473941243', '202112262473941283', '202112262473941473',
        '202112262473941823', '202112262473942083', '202112262473941833', '202112262473941933', '202112262473942183',
        '202112262473941753', '202112262473942043', '202112262473941973', '202112262473942303', '202112262473944693',
        '202112262473945423', '202112262473944913', '202112262473945353', '202112262473945003', '202112262473945483',
        '202112262473944733', '202112262473944883', '202112262473945033', '202112262473945093', '202112262473945113',
        '202112262473945063', '202112262473945213', '202112262473945613', '202112262473945743', '202112262473945563',
        '202112262473945693', '202112262473945723', '202112262473945943', '202112262473948173', '202112262473954813',
        '202112262473948393', '202112262473948423', '202112262473948223', '202112262473948483', '202112262473948183',
        '202112262473948263', '202112262473948233', '202112262473948743', '202112262473948853', '202112262473948603',
        '202112262473948373', '202112262473948523', '202112262473948463', '202112262473949053', '202112262473951783',
        '202112262473951493', '202112262473971373', '202112262473954973', '202112262473955343', '202112262473958543',
        '202112262473958733', '202112262473958983', '202112262473964903', '202112262473968323', '202112262473971383',
        '202112262473971583', '202112262473973293', '202112262473977383', '202112262473977373', '202112262473977523',
        '202112262473978483', '202112262473980833', '202112262473986313', '202112262473982773', '202112262473982903',
        '202112262473983903', '202112262473983893', '202112262473983993', '202112262473983643', '202112262473985723',
        '202112262473986393', '202112262473986443', '202112262473994713', '202112262474043836'
    ]
    for s in ss:
        spu_info = get_all_info(s)
        pay_price = 0.0
        gift_sku = []
        has_gift_sku = []
        for spp in spu_info:
            pay_price += spp["pay_price"]
            item_id = spp["item_id"]
            num = int(spp["item_count"])
            gf = cal_map.get(item_id)
            for i in range(num):
                if gf is None or len(gf) < 1:
                    has_gift_sku.append(item_id)
                else:
                    for g in gf:
                        gift_sku.append(g)

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
