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
    businessParams = json.dumps({"brandChannel": 228,
                                 "itemIdList": [1000002, 1001840],
                                 "warehouseId": 0
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
    r = requests.post("http://172.16.96.197:9999/order-stock-service-api/stockBmp/bmpTradeStockQty",
                      data=json.dumps(r_data), headers=head)
    print(r.content.decode("utf-8"))


# 批量调取接口
def batch_get(uul):
    r = requests.get(uul)
    print(r.content.decode("utf-8"))


if __name__ == "__main__":
    # test_useCoupon()
    ll = ['http://10.5.105.104:9089/stock/resetStockPreQty?itemId=5096240&warehouseId=3364',
          'http://10.5.105.104:9089/stock/resetStockPreQty?itemId=5096235&warehouseId=3364',
          'http://10.5.105.104:9089/stock/resetStockPreQty?itemId=5486199&warehouseId=3364',
          'http://10.5.105.104:9089/stock/resetStockPreQty?itemId=5489629&warehouseId=3364',
          'http://10.5.105.104:9089/stock/resetStockPreQty?itemId=5546644&warehouseId=3364',
          'http://10.5.105.104:9089/stock/resetStockPreQty?itemId=2838106&warehouseId=3364',
          'http://10.5.105.104:9089/stock/resetStockPreQty?itemId=2991891&warehouseId=3364',
          'http://10.5.105.104:9089/stock/resetStockPreQty?itemId=5461014&warehouseId=3364',
          'http://10.5.105.104:9089/stock/resetStockPreQty?itemId=5546643&warehouseId=3364',
          'http://10.5.105.104:9089/stock/resetStockPreQty?itemId=5546633&warehouseId=3364',
          'http://10.5.105.104:9089/stock/resetStockPreQty?itemId=5546639&warehouseId=3364',
          'http://10.5.105.104:9089/stock/resetStockPreQty?itemId=2991872&warehouseId=3364']
    for m in ll:
        batch_get(m)
