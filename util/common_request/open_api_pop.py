# coding=utf-8
import time
from datetime import datetime

import pymysql
import requests
import json


def test_get_bmp_stock():
    head = {"Content-Type": "application/json; charset=UTF-8", 'Connection': 'close'}
    businessParams = json.dumps({"warehouseId": 1016,
                                 "userId": 9999,
                                 "itemIdList": [2020037713],
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
    r = requests.post("http://127.0.0.1:9089/stockBmp/zeroClearing",
                      data=json.dumps(r_data), headers=head)
    print(r.content.decode("utf-8"))


# 批量调取接口
def batch_get(uul):
    r = requests.get(uul)
    print(r.content.decode("utf-8"))


def get_third_order():
    head = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Third-Token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJqd3RfYWRtaW4iLCJzdWIiOiJ1bXMifQ.NqYPhBsMWuoq8BZzOI7cF_QWXhBhTteJm0lUYeTePic"}
    r_data = {
        "open_id": 7977427,
        "third_order_code": "4734125129332012869A"
    }
    print(json.dumps(r_data))
    r = requests.post("https://third-trade-api.mia.com/api/Tiktok_orders/get_third_order_detail",
                      data=json.dumps(r_data), headers=head)
    print(r.content.decode("utf-8"))


def test_zero_bmp_stock():
    head = {"Content-Type": "application/json; charset=UTF-8", 'Connection': 'close'}
    businessParams = json.dumps({"warehouseId": 9757,
                                 "userId": 9999,
                                 "remark": "备8注测试无测试无备注测试无注测试无",
                                 "sourceList": [{
                                     "brandChannel": 1,
                                     "id": 42259,
                                     "itemId": 6056781,
                                     "qty": 1,
                                     "tzItemId": 0
                                 }],
                                 "targetList": [{
                                     "brandChannel": 264,
                                     "id": 43775,
                                     "itemId": 6056781,
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
    # print(json.dumps(r_data))
    r = requests.post("http://172.16.130.143:9999/order-stock-service-api/stockBmp/bmpDistributeStockQty",
                      data=json.dumps(r_data), headers=head)
    print(r.content.decode("utf-8"))


def order_decrypt(order_code):
    post_data = {
        "order_code": str(order_code)
    }
    r = requests.post("http://ums.intra.miyabaobei.com/server_api/order_api/getThirdOrderDecryptData", data=post_data)
    print(r.content.decode("utf-8"))


def get_mia_cursor(db_name="mia"):
    conn = pymysql.connect(host="10.5.96.80",
                           port=3306,
                           user="pop_cuijiabin",
                           passwd="8dtx5EOUZASc#",
                           db=db_name,
                           charset="utf8")
    return conn.cursor()


def get_return_process_order(s_code):
    cur = get_mia_cursor("mia")

    sql = "SELECT rp.id " + \
          "FROM open_order_channel ooc  " + \
          "LEFT JOIN orders o on ooc.superior_order_code = o.superior_order_code " + \
          "LEFT JOIN return_process rp on rp.order_code = o.order_code " + \
          "WHERE ooc.open_order_id  = '" + str(s_code) + "'"
    # print(sql)
    cur.execute(sql)
    result_data = cur.fetchall()
    if len(result_data) > 0 and result_data[0][0] is not None:
        # print(result_data[0])
        return "是"
    return "否"


def get_qimen_process_order(s_code):
    cur = get_mia_cursor("mia")

    sql = "SELECT id " + \
          "FROM qimen_return_item  " + \
          "WHERE open_order_id  = '" + str(s_code) + "'"
    cur.execute(sql)
    result_data = cur.fetchall()
    if len(result_data) > 0 and result_data[0][0] is not None:
        return "是"
    return "否"


# 根据mia子单号查询快递单号信息
def get_dst_sheet(order_code):
    cur = get_mia_cursor("mia")

    sql = "SELECT DISTINCT o.order_code,ec.name as express_name,ds.sheet_code,sw.`name` as warehouse_name " + \
          "FROM orders o LEFT JOIN parent_dst_sheet ds on o.id = ds.order_id " + \
          "LEFT JOIN express_company ec on ec.id = ds.express_id " + \
          "LEFT JOIN stock_warehouse sw on sw.id = o.warehouse_id " + \
          "WHERE o.order_code  = '" + str(order_code) + "'"
    cur.execute(sql)
    columns = [col[0] for col in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    cur.close()
    if len(rows) < 1:
        print("##")
    else:
        r = rows[0]
        express_name = r['express_name']
        sheet_code = r['sheet_code']
        warehouse_name = r['warehouse_name']
        result = ""
        if express_name is None:
            express_name = ""

        if sheet_code is None:
            sheet_code = ""

        if warehouse_name is None:
            warehouse_name = ""
        print(express_name + "\t" + sheet_code + "\t" + warehouse_name)


# 抖音订单解密
def decrypt_third_order(s_code):
    head = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Third-Token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJqd3RfYWRtaW4iLCJzdWIiOiJ1bXMifQ.NqYPhBsMWuoq8BZzOI7cF_QWXhBhTteJm0lUYeTePic"}
    r_data = {
        "third_order_code": str(s_code),
        "decrypt_field": [
            "phone", "name", "address"
        ]
    }
    print(json.dumps(r_data))
    r = requests.post("http://third-trade-api.miaidc.com/api/Tiktok_orders/tiktok_order_decrypt",
                      data=json.dumps(r_data), headers=head)
    print(r.content.decode("utf-8"))


def test_zero_http_stock():
    head = {"Content-Type": "application/json; charset=UTF-8", 'Connection': 'close'}
    businessParams = json.dumps({"isTest": 0,
                                 "items": [
                                     {"isExact": 0, "itemId": 1000176, "warehouseIds": [], "warehouseIdsSize": 0},
                                     {"isExact": 0, "itemId": 1000069, "warehouseIds": [], "warehouseIdsSize": 0},
                                     {"isExact": 0, "itemId": 1000067, "warehouseIds": [], "warehouseIdsSize": 0},
                                     {"isExact": 0, "itemId": 1000068, "warehouseIds": [], "warehouseIdsSize": 0},
                                     {"isExact": 0, "itemId": 11111, "warehouseIds": [], "warehouseIdsSize": 0},
                                     {"isExact": 0, "itemId": 1137666, "warehouseIds": [], "warehouseIdsSize": 0},
                                     {"isExact": 0, "itemId": 1048263, "warehouseIds": [], "warehouseIdsSize": 0},
                                     {"isExact": 0, "itemId": 1000150, "warehouseIds": [], "warehouseIdsSize": 0},
                                     {"isExact": 0, "itemId": 1000002, "warehouseIds": [], "warehouseIdsSize": 0},
                                     {"isExact": 0, "itemId": 123412, "warehouseIds": [], "warehouseIdsSize": 0},
                                     {"isExact": 0, "itemId": 888891, "warehouseIds": [], "warehouseIdsSize": 0},
                                     {"isExact": 0, "itemId": 1000113, "warehouseIds": [], "warehouseIdsSize": 0},
                                     {"isExact": 0, "itemId": 1000112, "warehouseIds": [], "warehouseIdsSize": 0},
                                     {"isExact": 0, "itemId": 1000111, "warehouseIds": [], "warehouseIdsSize": 0},
                                     {"isExact": 0, "itemId": 1000110, "warehouseIds": [], "warehouseIdsSize": 0},
                                     {"isExact": 0, "itemId": 4464708, "warehouseIds": [], "warehouseIdsSize": 0},
                                     {"isExact": 0, "itemId": 2377989, "warehouseIds": [], "warehouseIdsSize": 0},
                                     {"isExact": 0, "itemId": 2348459, "warehouseIds": [], "warehouseIdsSize": 0},
                                     {"isExact": 0, "itemId": 2065355, "warehouseIds": [], "warehouseIdsSize": 0},
                                     {"isExact": 0, "itemId": 33346, "warehouseIds": [], "warehouseIdsSize": 0},
                                 ]
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
    r = requests.post("http://172.16.130.143:9999/order-stock-service-api/stockTrade/stockQueryQty",
                      data=json.dumps(r_data), headers=head)
    print(r.content.decode("utf-8"))


def read_file(file_path):
    with open(file_path, 'r') as f:
        line = f.readline()
        num = 1
        while line:
            line = line.strip('\n')
            if len(line) == 0:
                continue
            requests.get("http://10.5.108.57:8080/orderTrailInit?thirdOrderCode=" + line)
            if num % 500 == 0:
                print(num, "休眠")
                time.sleep(8)
            num += 1
            line = f.readline()
        f.close()


if __name__ == "__main__":
    # a = datetime.now()
    # test_zero_http_stock()

    # test_zero_bmp_stock()
    # b = datetime.now()  # 获取当前时间
    # durn = (b - a).microseconds  # 两个时间差，并以秒显示出来
    # print(durn)
    ll = [
    ]
    for o in ll:
        # decrypt_third_order(str(o))
        order_decrypt(str(o))
    # read_file('E:/file/download/file_31.txt')
