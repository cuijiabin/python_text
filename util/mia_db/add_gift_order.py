import pymysql
from itertools import groupby, chain
from string import Template


def get_default_cursor():
    conn = pymysql.connect(host="10.5.96.80",
                           port=3306,
                           user="pop_cuijiabin",
                           passwd="8dtx5EOUZASc#",
                           charset="utf8")
    return conn.cursor()


def get_lock_phone_set():
    cur = get_default_cursor()
    sql = "SELECT DISTINCT o.dst_mobile " \
          "FROM mia_wms.`oms_intercept_policy_order_rels` r " \
          "INNER JOIN mia.orders o on r.order_id = o.id " \
          "WHERE r.policy_id = 41 and r.is_lock = 1 and o.`status` < 6"
    cur.execute(sql)

    rows = cur.fetchall()
    result_list = list(chain.from_iterable(rows))
    cur.close()
    return result_list


def get_unlock_phone_set(p_list):
    code_lists = ','.join(p_list)
    cur = get_default_cursor()
    sql = "SELECT distinct o.dst_mobile " \
          "FROM mia.orders o " \
          "INNER JOIN mia.order_item oi on o.id = oi.order_id " \
          "LEFT JOIN mia_wms.oms_intercept_policy_order_rels p on o.id = p.order_id " \
          "WHERE o.order_time > '2021-04-16 18:00' and o.`status` < 6 " \
          "AND o.channel = 211 AND o.brand_channel in (17,220,221,222,224,225,227,231,247) " \
          "AND oi.item_id in (5917239,5917240,5917241,5917242,5917243,5917249,5917250,5917251,5917252)  " \
          "AND o.dst_mobile in (" + code_lists + ")  " \
                                                 "AND (p.is_lock = 0 OR p.id is NULL)"
    cur.execute(sql)

    rows = cur.fetchall()
    result_list = list(chain.from_iterable(rows))
    cur.close()
    if len(result_list) < 1:
        return p_list

    p_list = list(set(p_list).difference(set(result_list)))

    return p_list


def get_unlock_order_set(p_list):
    code_lists = ','.join(p_list)
    cur = get_default_cursor()
    sql = "SELECT o.dst_mobile,o.superior_order_code,o.order_time,o.id,oc.third_order_time " \
          "FROM mia_wms.`oms_intercept_policy_order_rels` r " \
          "INNER JOIN mia.orders o on r.order_id = o.id " \
          "INNER JOIN mia.open_order_channel oc on oc.superior_order_code = o.superior_order_code " \
          "WHERE r.policy_id = 41 and r.is_lock = 1 and o.`status` < 6 " \
          "and o.dst_mobile in (" + code_lists + ")  " \
                                                 "ORDER BY oc.third_order_time ASC,o.id ASC "
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return rows


def stat_row_data(rows):
    # result_list = []
    for k, g in groupby(rows, lambda x: x["dst_mobile"]):
        print(k)
        print(g)
        # sub_list = list(map(lambda x: x["id"], g))
        # if len(sub_list) < 2:
        #     continue
        #
        # del (sub_list[0])
        # result_list += sub_list


"""
将集合均分，每份n个元素
:param list_collection:
:param n:
:return:返回的结果为评分后的每份可迭代对象
"""


def split_list_by_n(list_collection, n):
    for i in range(0, len(list_collection), n):
        yield list_collection[i: i + n]


if __name__ == '__main__':
    print("开始数据处理")
    # lock_phone_list = get_lock_phone_set()
    # lock_phone_list = split_list_by_n(lock_phone_list, 100)
    # for lock_phone in lock_phone_list:
    #     unlock_phone = get_unlock_phone_set(lock_phone)
    #     if len(unlock_phone) < 1:
    #         continue
    #     unlock_order = get_unlock_order_set(unlock_phone)
    #     for o in unlock_order:
    #         print(o["superior_order_code"], o["dst_mobile"], o["oc"])

    unlock_order = get_unlock_order_set(['13910915709', '15563141306', '15640811172'])
    stat_row_data(unlock_order)
    # for o in unlock_order:
    #     print(o["superior_order_code"], o["dst_mobile"], o["third_order_time"])
