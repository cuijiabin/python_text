# coding=utf-8
import pymysql
import requests
import json


def bindCouponByCode():
    r_data = {
        "orderCode": 1509180,
        "userId": "DD",
        "remark": "DD",
        "operatorId": 10000
    }
    r = requests.post("http://localhost:8080/coupon/bindCoupon.sc", data=r_data)
    print(r.content.decode("utf-8"))


def forceCancelOrder(orderCode, userId):
    r_data = {
        "orderCode": orderCode,
        "userId": userId,
        "remark": "不想要了",
        "operatorId": 10000
    }
    r = requests.post("http://10.5.107.177:8082/order/forceCancelSubOrder.sc", data=r_data)
    print(r.content.decode("utf-8"))


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
                                 "sourceList": [{
                                     "brandChannel": 1,
                                     "id": 42259,
                                     "itemId": 6056781,
                                     "qty": 4,
                                     "tzItemId": 0
                                 }],
                                 "targetList": [{
                                     "brandChannel": 264,
                                     "id": 43775,
                                     "itemId": 6056781,
                                     "qty": 4,
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
    r = requests.post("http://172.16.96.197:9999/order-stock-service-api/stockBmp/bmpDistributeStockQty",
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


# SELECT rp.id
# FROM open_order_channel ooc
# LEFT JOIN orders o on ooc.superior_order_code = o.superior_order_code
# LEFT JOIN return_process rp on rp.order_code = o.order_code
# WHERE ooc.open_order_id  = '210701-035481242541403';

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
        print("")
    else:
        print(rows[0])


if __name__ == "__main__":
    ll = ['2108182447165443']
    for o in ll:
        # print(get_return_process_order(o))
        get_dst_sheet(o)
