# coding=utf-8
import requests
import json


# 测试苏宁订单确认功能
def test_suning_order_confirm():
    r_json = json.dumps({
        "sn_request": {
            "sn_body": {
                "confirmOrder": {
                    "orderId": "1912117000036250",
                    "orderstatus": "02"
                }
            }
        }
    })

    post_data = {
        "method": "suning.online.order.confirm",
        "request_data": r_json
    }

    r = requests.post("https://gateway.mia.com/sngateway", data=post_data)
    print(r.content.decode("utf-8"))
    print(r)


# 测试苏宁订单支付结果通知
def test_suning_order_update():
    r_json = json.dumps({
        "sn_request": {
            "sn_body": {
                "updateOrder": {
                    "orderId": "1912027000032873",
                    "orderStatus": "04"
                }
            }
        }
    })

    post_data = {
        "method": "suning.online.order.update",
        "request_data": r_json
    }

    r = requests.post("https://gateway.mia.com/sngateway", data=post_data)
    print(r.content.decode("utf-8"))
    print(r)


# 测试苏宁订单确认收货接口
def test_suning_order_cmmdtyreceive():
    r_json = json.dumps({
        "sn_request": {
            "sn_body": {
                "confirmCmmdtyreceive": {
                    "orderItemInfo": [
                        {
                            "operateTime": "20191210101220",
                            "orderItemId": "2147483647",
                            "statusDesc": "0"
                        },
                        {
                            "operateTime": "20191210101220",
                            "orderItemId": "2147483647",
                            "statusDesc": "0"
                        },
                        {
                            "operateTime": "20191210101220",
                            "orderItemId": "2147483647",
                            "statusDesc": "0"
                        }

                    ]

                }
            }
        }
    })

    post_data = {
        "method": "suning.online.cmmdtyreceive.confirm",
        "request_data": r_json
    }

    r = requests.post("https://gateway.mia.com/sngateway", data=post_data)
    print(r.content.decode("utf-8"))
    print(r)


# 测试苏宁订单支付前取消
def test_suning_order_cancel():
    r_json = json.dumps({
        "sn_request": {
            "sn_body": {
                "cancelOrder": {
                    "orderId": "1912027000032873",
                    "orderStatus": "03",
                    "flag": "02"
                }
            }
        }
    })

    post_data = {
        "method": "suning.online.order.cancel",
        "request_data": r_json
    }

    r = requests.post("https://gateway.mia.com/sngateway", data=post_data)
    print(str(r.content.decode("utf-8")))
    print(r)


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
    businessParams = json.dumps({"warehouseId": 40,
                                 "userId": 9999,
                                 "sourceList": [{"itemId": 1001840, "tzItemId": 0, "brandChannel": 1, "qty": 1}],
                                 "targetList": [{"itemId": 1001840, "tzItemId": 0, "brandChannel": 222, "qty": 1}],
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


if __name__ == "__main__":
    # test_get_bmp_stock()
    get_third_order()
    # ll = []
    # for m in ll:
    #     batch_get(m)
