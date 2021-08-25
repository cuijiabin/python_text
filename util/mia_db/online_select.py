import pymysql
import requests
import time


def get_mia_cursor(db_name="mia"):
    conn = pymysql.connect(host="10.5.96.80",
                           port=3306,
                           user="pop_cuijiabin",
                           passwd="8dtx5EOUZASc#",
                           db=db_name,
                           charset="utf8")
    return conn.cursor()


def get_select_result():
    cur = get_mia_cursor("mia")

    sql = "select o.order_code as '订单号',u.cell_phone as '注册用户手机号',o.dst_name as '收件人',o.dst_mobile as '手机号码',o.dst_province as '所在省', " + \
          "o.dst_city as '所在市',o.dst_area as '所在区',o.dst_street as '详细地址',5137439 as '购买sku', " + \
          "1 as '购买数量',5888052 as '赠品sku',1 as '数量',o.order_time as '下单时间'  " + \
          "from orders o ,users u where o.user_id = u.id and o.superior_order_code in ( " + \
          "select gj.order_id from groupon_join_v2 gj where gj.groupon_son_id in ( " + \
          "select groupon_son_id from groupon_join_v2 gj where gj.groupon_son_id in ( " + \
          "SELECT DISTINCT o.relation_id FROM orders o,order_item t WHERE o.id = t.order_id " + \
          "AND IF (t.spu_id = 0,t.item_id,t.spu_id) IN (5137439) " + \
          "AND o.order_time >= '2021-01-11 11:00:00' AND o.from_type = 4 AND o.is_paid = 1 AND o.`status` < 6 " + \
          "AND o.wdgj_status = 2) " + \
          "and gj.is_pay = 2 and gj.order_status != 6 " + \
          "GROUP BY gj.groupon_son_id HAVING count(*) >= 4 and COUNT(*) < 10) " + \
          "and gj.order_id in ( " + \
          "SELECT DISTINCT o.superior_order_code FROM orders o,order_item t WHERE o.id = t.order_id " + \
          "AND IF (t.spu_id = 0,t.item_id,t.spu_id) IN (5137439) " + \
          "AND o.order_time >= '2021-01-11 11:00:00' AND o.from_type = 4 AND o.is_paid = 1 AND o.`status` < 6 " + \
          "AND o.wdgj_status = 2)) "
    cur.execute(sql)
    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return rows


def get_decrypt_order():
    cur = get_mia_cursor("mia")

    sql = "SELECT DISTINCT too.third_order_code " + \
          "FROM third_process_order too INNER JOIN open_order_channel ooc on ooc.open_order_id = too.third_order_code " + \
          "LEFT JOIN third_order_decrypt tod on ooc.superior_order_code = tod.mia_order_code " + \
          "WHERE too.third_order_time BETWEEN '2021-08-16 00:00' AND '2021-08-20 00:00' " + \
          "AND too.dst_phone_encrypt is not NULL " + \
          "AND tod.id is null LIMIT 500"
    cur.execute(sql)
    result_data = cur.fetchall()
    if len(result_data) > 0:
        f_data = list(map(lambda x: x[0], result_data))
        return f_data
    return []


if __name__ == '__main__':
    oo_list = [2107272442773593]
    for o in oo_list:
        post_data = {
            "orderCodes": str(o)
        }

        r = requests.post("http://10.5.107.177:8082/order/batchDecryptOrder.sc", data=post_data)
        print(r.content.decode("utf-8"))
        time.sleep(0.3)
