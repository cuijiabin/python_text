"""
店铺装修
"""

# coding=utf-8
import datetime
import time

import common_build_model as bm
import common_export_data as ced


# 获取mia主库供应商的基本信息
def get_pop_supplier_map(column=["distinct d.store_id", "d.templete_id", "d.supplier_id"]):
    cur = bm.get_mia_cursor()
    # column = ", ".join(list(map(lambda x: x, column)))
    # sql = "SELECT " + column + " FROM db_pop.store_decoration d WHERE d.type_id !=3 and d.supplier_id not in (SELECT t.supplier_id from db_pop.store_decoration t where t.type_id = 3)"

    sql = "SELECT t.id as sku, pxu.daily_price as '当前销售价'FROM item t left join customer_supplier a on t.supplier_id = a.id LEFT JOIN stock_warehouse b ON t.supplier_id = b.supplier_id LEFT JOIN procurement_contract c on t.supplier_id = c.supplier_id LEFT JOIN item_daily_price    pxu on t.id = pxu.sku WHERE a.pop_admin_id IN (SELECT user_id FROM sec_user_dep_map WHERE department_id IN (67,130) )and b.type in (3,5,7,10,11,12,13) and c.`status` = 2 and t.item_multiple_score >=3 and t.item_multiple_score <= 5 and t.status in (0,1) and pxu.start_time < NOW() and (pxu.end_time > NOW() or pxu.end_time = '0000-00-00 00:00:00')";
    cur.execute(sql)
    f_data = cur.fetchall()

    # 转成列表对象
    # f_data = list(map(lambda x: {"store_id": x[0], "templete_id": x[1], "supplier_id": x[2]}, f_data))
    # result = {}
    merfile = open("F:/project_dir/merge2.txt", "a", encoding="utf8")
    for sup in f_data:
        merfile.write(str(sup))
        merfile.write('\n')

    merfile.close()
    return


def get_day_nday_ago(date, n):
    t = time.strptime(date, "%Y-%m-%d")
    y, m, d = t[0:3]
    Date = str(datetime.datetime(y, m, d) - datetime.timedelta(n)).split()
    return Date[0]


def check_data_center(supplier_id, warehouse_id, info):
    cur = bm.get_mia_cursor()
    dp_cur = bm.get_mia_cursor("db_pop")
    for i in range(10, 0, -1):
        condition_day = get_day_nday_ago("2018-06-21", i)
        sql = "select count(oi.id) from orders o join order_item oi on o.id=oi.order_id where  o.`warehouse_id` = " + warehouse_id + " and " \
              "pay_time>='" + condition_day + " 00:00:00' and pay_time<='" + condition_day + " 23:59:59' and  o.is_paid=1 "

        db_sql = "SELECT deal_num FROM db_pop.data_supplier where supplier_id = " + supplier_id + " and add_date = '" + condition_day + "'"
        cur.execute(sql)
        dp_cur.execute(db_sql)

        f_data = cur.fetchall()
        d_data = dp_cur.fetchall()

        num = 0
        if len(d_data) > 0 :
            num = d_data[0][0]

        # merfile = open("F:\File\download\dd.txt", "a", encoding="utf8")
        if f_data[0][0] != num :
            print(info["id"], info["name"], condition_day, f_data[0][0], num)
            # new_str = str(info["id"]) + "," + info["name"] + "," + condition_day+ "," + str(f_data[0][0])+ "," + str(num)
        #     merfile.write(new_str)
        #     merfile.write('\n')
        # merfile.close()

if __name__ == "__main__":
    # get_pop_supplier_map()
    # check_data_center()

    # dp_cur = bm.get_mia_cursor("db_pop")
    # sql = "SELECT  supplier_id FROM db_pop.data_supplier where  add_date = '2018-06-19' GROUP BY supplier_id ORDER BY deal_num DESC limit 100"
    # dp_cur.execute(sql)
    # f_data = dp_cur.fetchall()
    # s_id = list(map(lambda x: x[0], f_data))
    s_id = [5460]
    # print(s_id)

    mp = ced.get_supplier_map(s_id)
    for i in mp:
        print(mp)
        check_data_center(str(mp[i]["id"]), str(mp[i]["w_id"]), mp[i])
