from itertools import chain

import pymysql


# 获取数据库游标
def get_default_cursor():
    conn = pymysql.connect(host="10.5.96.80",
                           port=3306,
                           user="pop_cuijiabin",
                           passwd="8dtx5EOUZASc#",
                           charset="utf8")
    return conn.cursor()


# 获取最近锁定的手机号
def get_lock_phone_set():
    cur = get_default_cursor()
    sql = "SELECT DISTINCT o.dst_mobile " \
          "FROM mia_wms.`oms_intercept_policy_order_rels` r " \
          "INNER JOIN mia.orders o on r.order_id = o.id " \
          "WHERE r.policy_id = 41 and r.is_lock = 1 and o.`status` < 6 and o.is_lock = 1 and r.create_time > '2021-04-10 09:00' and r.create_time < '2021-05-27 00:00' "
    cur.execute(sql)

    rows = cur.fetchall()
    result_list = list(chain.from_iterable(rows))
    cur.close()
    return result_list


# 获取可被解锁的订单
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
    mobile_set = set(map(lambda x: str(x['dst_mobile']), rows))
    # 初始化
    result_map = dict()
    for m in mobile_set:
        result_map.setdefault(m, [])

    for r in rows:
        m = r['dst_mobile']
        result_map[m].append(r['superior_order_code'])

    return result_map


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

    # 也可以创建一个.doc的word文档
    unlock_file = open("E:\\file\\download\\unlock_order.txt", 'w', encoding='UTF-8')
    lock_file = open("E:\\file\\download\\lock_order.txt", 'w', encoding='UTF-8')
    # msg也就是下面的Hello world!
    unlock_file.write("手机号 待解锁父订单号 当前关联锁定订单数" + "\n")
    lock_file.write("手机号 锁定父订单号" + "\n")

    lock_phone_list = get_lock_phone_set()
    lock_phone_list = split_list_by_n(lock_phone_list, 100)
    for lock_phone in lock_phone_list:
        unlock_phone = get_unlock_phone_set(lock_phone)
        if len(unlock_phone) < 1:
            continue
        unlock_order = get_unlock_order_set(unlock_phone)
        mobile_map = stat_row_data(unlock_order)
        for dst_mobile in mobile_map:
            superior_list = mobile_map[dst_mobile]
            first_code = superior_list[0]
            superior_set = set(superior_list)
            superior_set.remove(first_code)

            unlock_file.write(dst_mobile + " " + first_code + " " + str(len(superior_set) + 1) + "\n")
            if len(superior_set) > 0:
                for c in superior_set:
                    lock_file.write(dst_mobile + " " + c + "\n")

    unlock_file.close()
    lock_file.close()
