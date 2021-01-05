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


def get_mia_cursor(db_name="mia_mirror"):
    conn = pymysql.connect(host="10.5.96.80",
                           port=3306,
                           user="pop_cuijiabin",
                           passwd="8dtx5EOUZASc#",
                           db=db_name,
                           charset="utf8")
    return conn.cursor()


def get_superior_order_list(order_time):
    cur = get_mia_cursor("mia_mirror")
    sql_tmp = Template(
        "select o.superior_order_code, count(oi.id) as orderItemNum,sum(oi.pay_price) as pay_price FROM orders o LEFT JOIN order_item oi on o.id = oi.order_id "
        "WHERE o.order_time > '$order_time' and o.`status` != 6 and oi.spu_id in (5565870, 2485877, 2486004, 5767854, 5565871, 5766953, 5766952, 5776537, 2526700, 5766183, 5565877, 5776042) "
        "GROUP BY o.superior_order_code "
        "HAVING orderItemNum > 4 AND pay_price >= 344 "
        "ORDER BY orderItemNum DESC")
    sql = sql_tmp.substitute(order_time=order_time)
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return rows


def get_gift_info(superior_order_code):
    cur = get_mia_cursor("mia_mirror")
    sql_tmp = Template(
        "select spu_id,count(id) DIV 4 as num from order_item WHERE order_id in "
        "(select id from orders WHERE superior_order_code = '$superior_order_code') "
        "and spu_id in (5565870, 2485877, 2486004, 5767854, 5565871, 5766953, 5766952, 5776537, 2526700, 5766183, 5565877, 5776042) "
        "GROUP BY spu_id")
    sql = sql_tmp.substitute(superior_order_code=superior_order_code)
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return rows


def get_gift_result():
    superior_order_list = get_superior_order_list("2021-01-05 14:00")
    for superior_order in superior_order_list:
        superior_order_code = superior_order["superior_order_code"]
        spu_list = get_gift_info(superior_order_code)
        for spu in spu_list:
            spu_id = spu["spu_id"]
            spu_num = spu["num"]
            if global_spu_map.get(spu_id) is not None:
                target_spu_id = global_spu_map[spu_id]
                print(superior_order_code, target_spu_id, spu_num)
            else:
                spu_id_list = global_multi_spu_map.get(spu_id)
                for target_spu_id in spu_id_list:
                    print(superior_order_code, target_spu_id, spu_num * 2)


if __name__ == '__main__':
    get_gift_result()
