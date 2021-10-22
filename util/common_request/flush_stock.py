# coding=utf-8
from string import Template
import pymysql
import requests
import json


def get_mia_cursor(db_name="mia"):
    conn = pymysql.connect(host="10.5.96.80",
                           port=3306,
                           user="pop_cuijiabin",
                           passwd="8dtx5EOUZASc#",
                           db=db_name,
                           charset="utf8")
    return conn.cursor()


# 10.5.1.10 api.gateway.miaidc.com
def test_zero_bmp_stock():
    head = {"Content-Type": "application/json; charset=UTF-8", 'Connection': 'close'}
    businessParams = json.dumps({"warehouseId": 3364,
                                 "userId": 9999,
                                 "sourceList": [{
                                     "brandChannel": 1,
                                     "itemId": 2474174,
                                     "qty": 1,
                                     "tzItemId": 0
                                 }],
                                 "targetList": [{
                                     "brandChannel": 10,
                                     "itemId": 2474174,
                                     "qty": 1,
                                     "tzItemId": 0
                                 }]
                                 })
    commonParams = json.dumps({"appVersion": "1.0",
                               "clientVersion": "1.0",
                               "opUser": "pop",
                               "requestId": "5c53da49-e075-4d82-b9c7-52edbc0e92dc",
                               "timestamp": "1604561779971"
                               })
    r_data = {
        "businessParams": businessParams,
        "commonParams": commonParams
    }
    r = requests.post("http://api.gateway.miaidc.com/order-stock-service-api/stockBmp/bmpDistributeStockQty",
                      data=json.dumps(r_data), headers=head)
    print(r.content.decode("utf-8"))


def get_bmp_stock_info(item_id):
    cur = get_mia_cursor("mia_bmp")
    sql_tmp = Template(
        "SELECT item_id,warehouse_id,channel_id,tz_item_id,stock_quantity,`status` from brand_stock_item_channel  "
        "where item_id = $item_id and tz_item_id = 0 and channel_id !=1 and stock_quantity > 0 and `status` = 1 and is_presale = 2"
    )
    sql = sql_tmp.substitute(item_id=item_id)
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return rows


def get_tz_stock_info(item_id):
    cur = get_mia_cursor("mia_bmp")
    sql_tmp = Template(
        "SELECT DISTINCT bsic.tz_item_id AS item_id ,bsic.warehouse_id,bsic.channel_id,ROUND(bsic.stock_quantity/ssr.item_amount) as stock_quantity "
        "from brand_stock_item_channel bsic "
        "LEFT JOIN mia.spu_sku_relation ssr ON ssr.spu_id=bsic.tz_item_id AND ssr.item_id=bsic.item_id "
        "WHERE bsic.tz_item_id = $item_id and bsic.channel_id !=1 and bsic.stock_quantity > 0 and bsic.`status` = 1 and bsic.is_presale = 2"
    )
    sql = sql_tmp.substitute(item_id=item_id)
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    return rows


def get_stock_turnover(item_id, channel_id, warehouse_id, stock_qty, fd_day):
    cur = get_mia_cursor("api_bi")
    sql_tmp = Template(
        "SELECT SUM(sale_cnt) AS sum_sale_count FROM api_bi.APP_PUSH_API_WH_ITEM_SALE "
        "WHERE stat_dd >= DATE_ADD(CURRENT_DATE,INTERVAL -30 DAY) AND stat_dd < CURRENT_DATE "
        "AND order_channel = $channel_id AND warehouse_id = $warehouse_id AND item_id = $item_id"
    )
    sql = sql_tmp.substitute(item_id=item_id, channel_id=channel_id, warehouse_id=warehouse_id)
    cur.execute(sql)
    sum_sale_count = cur.fetchall()[0][0]

    if sum_sale_count is None:
        return "30天零动销，库存需要清零"

    sql_tmp = Template(
        "SELECT COUNT(*) AS stat_num FROM api_bi.APP_PUSH_API_WH_ITEM_SALE "
        "WHERE stat_dd >= DATE_ADD(CURRENT_DATE,INTERVAL -30 DAY) AND stat_dd < CURRENT_DATE "
        "AND order_channel = $channel_id AND warehouse_id = $warehouse_id AND item_id = $item_id"
    )
    sql = sql_tmp.substitute(item_id=item_id, channel_id=channel_id, warehouse_id=warehouse_id)
    cur.execute(sql)
    stat_num = cur.fetchall()[0][0]
    cur.close()
    if stat_num < 30:
        return "未满30天销售，库存不做处理"

    # 周转指标
    turnover_day = stock_qty * 30 / sum_sale_count
    if turnover_day <= fd_day / 2.0:
        return "周转指标" + str(round(turnover_day, 2)) + "未高于其采购周期指标的一半" + str(round(fd_day / 2.0, 2)) + "，库存不做处理"

    # print("周转指标:" + str(round(turnover_day, 2)) + " 采购周期指标一半:" + str(round(fd_day / 2.0, 2)))

    return [int(fd_day * sum_sale_count / 60), round(turnover_day, 2), fd_day, round(fd_day / 2.0, 2)]


def clear_bmp_stock(item_id, warehouse_id, channel_id):
    cur = get_mia_cursor("mia_bmp")
    sql_tmp = Template(
        "SELECT item_id,warehouse_id,channel_id,tz_item_id,stock_quantity,`status` "
        "from brand_stock_item_channel "
        "where channel_id = $channel_id and warehouse_id = $warehouse_id "
        "and tz_item_id = $item_id and stock_quantity > 0"
    )
    sql = sql_tmp.substitute(item_id=item_id, channel_id=channel_id, warehouse_id=warehouse_id)
    cur.execute(sql)

    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()

    if len(rows) < 1:
        print("无相关数据")
        return

    sourceList = []
    targetList = []
    for row in rows:
        sourceList.append({
            "brandChannel": channel_id,
            "itemId": row["item_id"],
            "qty": row["stock_quantity"],
            "tzItemId": row["tz_item_id"]
        })

        targetList.append({
            "brandChannel": 1,
            "itemId": row["item_id"],
            "qty": row["stock_quantity"],
            "tzItemId": 0
        })

    head = {"Content-Type": "application/json; charset=UTF-8", 'Connection': 'close'}
    businessParams = json.dumps({"warehouseId": warehouse_id,
                                 "userId": 9999,
                                 "sourceList": sourceList,
                                 "targetList": targetList
                                 })
    commonParams = json.dumps({"appVersion": "1.0",
                               "clientVersion": "1.0",
                               "opUser": "pop",
                               "requestId": "5c53da49-e075-4d82-b9c7-52edbc0e92dc",
                               "timestamp": "1604561779971"
                               })
    r_data = {
        "businessParams": businessParams,
        "commonParams": commonParams
    }

    # print(json.dumps(r_data))
    r = requests.post("http://api.gateway.miaidc.com/order-stock-service-api/stockBmp/bmpDistributeStockQty",
                      data=json.dumps(r_data), headers=head)
    print(r.content.decode("utf-8"))
    return


# bmp库存数据刷库相关的操作内容
if __name__ == "__main__":
    # test_zero_bmp_stock()
    # tuple_list = []
    #
    # for item in tuple_list:
    #     rows = get_bmp_stock_info(item[0])
    #     for row in rows:
    #         num = get_stock_turnover(row['item_id'], row['channel_id'], row['warehouse_id'], row['stock_quantity'],
    #                                  item[1])
    #         if isinstance(num, list):
    #             s = 1 + 1
    #             print(str(row['item_id']) + "\t" + str(row['warehouse_id']) + "\t" + str(
    #                 row['channel_id']) + "\t" + str(num[1]) + "\t" + str(num[2]) + "\t" + str(num[3]) + "\t" + str(
    #                 num[0]))
    #         elif num == '30天零动销，库存需要清零':
    #             s = 1 + 1
    #             print(
    #                 str(row['item_id']) + "\t" + str(row['warehouse_id']) + "\t" + str(row['channel_id']) + "\t" + str(
    #                     num))
    #         else:
    #             s = 1 + 1
    #             print(
    #                 str(row['item_id']) + "\t" + str(row['warehouse_id']) + "\t" + str(row['channel_id']) + "\t" + str(
    #                     num))

    tuple_list = []
    for em in tuple_list:
        clear_bmp_stock(em[0], em[1], em[2])
