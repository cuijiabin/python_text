import pymysql
from string import Template

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
    conn = pymysql.connect(host="10.5.110.107",
                           port=3306,
                           user="coupon_mia_read",
                           passwd="xzpd857gyy3mo",
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


# 订单号	交易流水号	收货人	手机号	省	市	区	街道	地址	订单总支付金额	总邮费	总税费	商品ID	单个销售价	数量	单个税费	仓库id	身份证号	真实姓名	身份证正面	身份证反面	客户备注	支付方式
# GROUP_CONCAT
if __name__ == '__main__':
    print("订单号,交易流水号,收货人,手机号,省,市,区,街道,地址,订单总支付金额,总邮费,总税费,商品ID,单个销售价,数量,单个税费,仓库id,身份证号,真实姓名,身份证正面,身份证反面,客户备注,支付方式")
    get_gift_result()
