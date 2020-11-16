# coding=utf-8
import datetime
import json
import time

import pymysql
import requests
from string import Template


def get_mia_cursor(db_name="mia_mirror"):
    conn = pymysql.connect(host="10.5.96.80",
                           port=3306,
                           user="pop_cuijiabin",
                           passwd="8dtx5EOUZASc#",
                           db=db_name,
                           charset="utf8")
    return conn.cursor()


def get_bmp_pre_stock_list(m_date):
    cur = get_mia_cursor("mia_bmp")
    sql_tmp = Template(
        "select item_id,warehouse_id,pre_qty,lastmodified_date as modify_time from brand_stock_item_channel "
        "WHERE warehouse_id in (select id from stock_warehouse WHERE type in (1,6,8) and `status` = 1) "
        "AND channel_id = 1 and `status` =1 and pre_qty != 0 "
        "and lastmodified_date < '$lastmodified_date' ORDER BY pre_qty DESC")
    sql = sql_tmp.substitute(lastmodified_date=m_date)
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return rows


def get_mia_pre_stock_list(m_date):
    cur = get_mia_cursor("mia_mirror")
    sql_tmp = Template(
        "SELECT s.item_id AS item_id, s.warehouse_id AS warehouse_id, s.pre_qty AS pre_qty, s.modify_time as modify_time "
        "from stock_item s LEFT JOIN stock_warehouse sw on s.warehouse_id = sw.id  "
        "WHERE sw.type in (1,6,8) and s.`status` =1 and s.pre_qty != 0 "
        "and modify_time < '$modify_time' ORDER BY s.pre_qty DESC")
    sql = sql_tmp.substitute(modify_time=m_date)
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return rows


def get_order_pre_qty(info):
    sql_tmp = Template("SELECT COALESCE(SUM(oi.qty),0) AS preQty FROM orders os "
                       "INNER JOIN order_item oi ON oi.order_id = os.id "
                       "WHERE os.warehouse_id = $wid AND os.`status` IN (1, 2) AND oi.item_id = $item_id AND os.is_test = 0")
    sql = sql_tmp.substitute(wid=info["warehouse_id"], item_id=info["item_id"])
    cur = get_mia_cursor("mia_mirror")
    cur.execute(sql)

    result_data = cur.fetchall()
    if not result_data[0][0] == info["pre_qty"]:
        url = "http://10.5.105.104:9089/stock/resetStockPreQty?itemId=" + str(info["item_id"]) + "&warehouseId=" + str(
            info["warehouse_id"])
        # requests.get(url)
        print(info, info["pre_qty"] - result_data[0][0])
    cur.close()
    return result_data[0][0]


# 重置预占库存
# 地址 http://10.5.105.104:9089/stock/resetStockPreQty?itemId=5822719&warehouseId=3364
if __name__ == '__main__':
    m_date = (datetime.datetime.now() - datetime.timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M")
    print(m_date)
    rows = get_bmp_pre_stock_list(m_date)
    for r in rows:
        get_order_pre_qty(r)

    print("mia 处理开始")
    rows = get_mia_pre_stock_list(m_date)
    for r in rows:
        get_order_pre_qty(r)
