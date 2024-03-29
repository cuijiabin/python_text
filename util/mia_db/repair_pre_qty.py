# coding=utf-8
import datetime
from string import Template

import requests
import util as bm


def get_bmp_pre_stock_list(start_date, m_date):
    sql_tmp = Template(
        "select item_id,warehouse_id,pre_qty,lastmodified_date as modify_time from brand_stock_item_channel "
        "WHERE warehouse_id in (select id from stock_warehouse WHERE type in (1,6,8) and `status` = 1) "
        "AND channel_id = 1 and `status` =1 and pre_qty != 0 "
        "and lastmodified_date >= '$start_date' "
        "and lastmodified_date < '$lastmodified_date' ORDER BY pre_qty DESC")
    sql = sql_tmp.substitute(start_date=start_date, lastmodified_date=m_date)

    return bm.get_mia_db_data(sql, "mia_bmp")


def get_mia_pre_stock_list(start_date, m_date):
    sql_tmp = Template(
        "SELECT s.item_id AS item_id, s.warehouse_id AS warehouse_id, s.pre_qty AS pre_qty, s.modify_time as modify_time "
        "from stock_item s LEFT JOIN stock_warehouse sw on s.warehouse_id = sw.id  "
        "WHERE sw.type in (1,6,8) and s.`status` =1 and s.pre_qty != 0 "
        "and modify_time >= '$start_date' "
        "and modify_time < '$modify_time' ORDER BY s.pre_qty DESC")
    sql = sql_tmp.substitute(start_date=start_date, modify_time=m_date)

    return bm.get_mia_db_data(sql, "mia_mirror")


def get_order_pre_qty(info):
    sql_tmp = Template("SELECT COALESCE(SUM(oi.qty),0) AS preQty FROM orders os "
                       "INNER JOIN order_item oi ON oi.order_id = os.id "
                       "WHERE os.warehouse_id = $wid AND os.`status` IN (1, 2) AND oi.item_id = $item_id AND os.is_test = 0")
    sql = sql_tmp.substitute(wid=info["warehouse_id"], item_id=info["item_id"])
    cur = bm.get_mia_cursor("mia_mirror")
    cur.execute(sql)

    result_data = cur.fetchall()
    if not result_data[0][0] == info["pre_qty"]:
        wms_qty = get_wms_qty(info)
        url = "http://10.5.105.104:9089/stock/setPreQty?itemId=" + str(info["item_id"]) + "&warehouseId=" + str(
            info["warehouse_id"]) + "&preQty=" + str(result_data[0][0] + wms_qty)

        if info["pre_qty"] - result_data[0][0] - wms_qty != 0:
            print(url)
            requests.get(url)
        print(info, info["pre_qty"] - result_data[0][0], wms_qty)
    cur.close()
    return result_data[0][0]


def get_wms_qty(info):
    sql_tmp = Template("SELECT count(oi.item_id)AS preQty FROM oms_sync_delivery_order o "
                       "INNER JOIN oms_orders oo ON o.order_code = oo.order_code "
                       "INNER JOIN oms_order_item oi ON oo.order_id = oi.order_id "
                       "WHERE o.sync_order = 2 AND o.sync_stock = 1 AND o.warehouse_id = $wid AND oi.item_id = $item_id")
    sql = sql_tmp.substitute(wid=info["warehouse_id"], item_id=info["item_id"])

    return bm.get_mia_db_data(sql, "mia_wms")


def get_bmp_pre_stock_by_ids(bmp_ids):
    sql_tmp = Template(
        "select item_id,warehouse_id,pre_qty,lastmodified_date as modify_time from brand_stock_item_channel "
        "WHERE id in ($ids)")
    ids = ", ".join(list(map(lambda x: str(x), bmp_ids)))
    sql = sql_tmp.substitute(ids=ids)
    return bm.get_mia_db_data(sql, "mia_bmp")


mq = {
    "itemId": 5876098,
    "opType": 9,
    "operatePreQty": False,
    "orderCode": "10",
    "qty": -3,
    "stockItemId": 8242681,
    "stockType": 1,
    "superiorOrderCode": "",
    "test": False,
    "userId": 9999,
    "warehouseId": 3364
}


# 库存服务mq补发
def re_send_product_mq(mq):
    r = requests.post("http://10.5.105.104:9089/stock/reSendMq", data=mq)

    print(r.content.decode("utf-8"))


# 重置预占库存
# 地址 http://10.5.105.104:9089/stock/resetStockPreQty?itemId=5822719&warehouseId=3364
# 1440 2880 4320 5760 7200
if __name__ == '__main__':
    # start_date = (datetime.datetime.now() - datetime.timedelta(minutes=180)).strftime("%Y-%m-%d %H:%M")
    # end_date = (datetime.datetime.now() - datetime.timedelta(minutes=40)).strftime("%Y-%m-%d %H:%M")
    # print(start_date, end_date)
    # rows = get_bmp_pre_stock_list(start_date, end_date)
    ids = [44872]
    rows = get_bmp_pre_stock_by_ids(ids)
    for r in rows:
        get_order_pre_qty(r)

    # time.sleep(2)
    # print("mia 处理开始")
    # rows = get_mia_pre_stock_list(start_date, m_date)
    # for r in rows:
    #     get_order_pre_qty(r)

    # re_send_product_mq(mq)
