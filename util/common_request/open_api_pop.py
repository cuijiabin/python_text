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


def query_coupon_for_checkout_multi():
    # r_data = {"canUseChannel": 5, "checkedCouponCodes": [], "checkedCouponCodesSize": 0, "platform": "Normal",
    #           "tContent": {"couponsSize": 0, "orderItems": [
    #               {"balancePrice": "0", "brandId": 6769, "cashCouponPrice": "0", "categoryId": 0, "categoryIdNg": 12867,
    #                "couponCode": "0", "couponLimitType": 0, "couponPrice": "0", "couponPriceDetailsSize": 0,
    #                "dealPrice": "110.00", "giftType": 0, "isPlusPack": 0, "isSpu": 0, "itemId": 1000110,
    #                "itemName": " 限定版护翼日用卫生巾 23cm*20片", "itemSalePrice": "110.00", "itemSize": "SINGLE", "itemType": 0,
    #                "nonPlatformCashCouponPrice": "0", "nonPlatformCouponPrice": "0", "parentCategoryId": 0,
    #                "payPrice": "110.00", "platformCashCouponPrice": "0", "platformCouponPrice": "0", "redbagPrice": "0",
    #                "reducePrice": "0", "seckill": 0, "shipPrice": "0", "shopId": 1192, "shopName": "", "spuSkus": [],
    #                "spuSkusSize": 0, "supplierId": 0, "taxPrice": "0", "uniqKey": "0", "warehouseId": 0,
    #                "warehouseType": 6}], "orderItemsSize": 1,
    #                        "orders": {"balancePrice": "0", "cashCouponPrice": "0.00", "channel": "211",
    #                                   "ckSuperiorOrderCode": "", "ckType": 110, "couponPrice": "0.00",
    #                                   "dealPrice": "110.00", "orderTime": "2021-02-09 16:08:54", "payPrice": "110.00",
    #                                   "salePrice": "110.00", "shipPrice": "0", "subChannel": "0", "taxPrice": "0",
    #                                   "totalRedbagPrice": "0", "usedRedbagPrice": "0", "userId": 220111262}}}
    r_data = {"canUseChannel": 5, "checkedCouponCodes": [], "checkedCouponCodesSize": 0, "platform": "Normal",
              "tContent": {"couponsSize": 0, "orderItems": [
                  {"balancePrice": "0", "brandId": 6769, "cashCouponPrice": "0", "categoryId": 0,
                   "categoryIdNg": 12867, "couponCode": "0", "couponLimitType": 0, "couponPrice": "0",
                   "couponPriceDetailsSize": 0, "dealPrice": "99.10", "giftType": 0, "isPlusPack": 0, "isSpu": 0,
                   "itemId": 1000110, "itemName": " 限定版护翼日用卫生巾 23cm*20片", "itemSalePrice": "99.10",
                   "itemSize": "SINGLE", "itemType": 0, "nonPlatformCashCouponPrice": "0",
                   "nonPlatformCouponPrice": "0", "parentCategoryId": 0, "payPrice": "99.10",
                   "platformCashCouponPrice": "0", "platformCouponPrice": "0", "redbagPrice": "0",
                   "reducePrice": "0", "seckill": 0, "shipPrice": "0", "shopId": 1192, "shopName": "蜜芽自营",
                   "spuSkus": [], "spuSkusSize": 0, "supplierId": 0, "taxPrice": "0",
                   "uniqKey": "1000110-SINGLE-0", "warehouseId": 40, "warehouseType": 1}], "orderItemsSize": 1,
                           "orders": {"balancePrice": "0", "cashCouponPrice": "0", "channel": "211",
                                      "ckSuperiorOrderCode": "", "ckType": 112, "couponPrice": "0",
                                      "dealPrice": "99.10", "orderTime": "2021-02-09 16:08:10",
                                      "payPrice": "99.10", "salePrice": "99.10", "shipPrice": "0",
                                      "subChannel": "weixinxcx_pick", "taxPrice": "0", "totalRedbagPrice": "0",
                                      "usedRedbagPrice": "0", "userId": 220111262}}}
    r = requests.post("http://127.0.0.1:8080/couponTrade/queryCouponForCheckoutMulti",
                      data={"json": json.dumps(r_data)})
    print(r.content.decode("utf-8"))


def auto_checkout_multi():
    r_data = {"canUseChannel": 5, "platform": "Normal", "tContent": {"coupons": [
        {"afterCouponOrderMinPrice": "0.00", "allOk": True, "batchCode": "normal-201118-142674567ec14d5d",
         "bindTime": "2021.02.09", "bindUserId": 220111262, "businessId": 0, "businessType": 1, "canGroupon": 0,
         "canNormal": 1, "canSeckill": 0, "canVirtualItem": 0, "canXiaoHuan": 0, "couponCode": "UAB1A8913FC0E00",
         "couponDetailOk": True, "couponInfoOk": True, "expireTime": "2021.11.26", "isFreeShip": 0, "isGlobalUse": 1,
         "isPassword": 1, "isShowSearchLink": 0, "isUsable": 1, "itemOk": True, "leftUseNum": 1, "minPrice": "0.00",
         "minPriceOk": True, "mutexCouponItem": {}, "oneUsable": 1, "password_code": "", "selected": 1,
         "startTime": "2020.11.18", "superpositionType": 1, "timeValidType": 1, "title": "", "type": 1, "typeUse": 1,
         "useEndTime": "2021.11.26", "useRang": "无门槛", "useStartTime": "2020.11.18", "validDay": 0, "value": "9.90"}],
        "couponsSize": 1, "orderItems": [
            {"balancePrice": "0", "batchCodePlatform": "normal-201118-142674567ec14d5d", "brandId": 6769,
             "cashCouponPrice": "0.00", "categoryId": 0, "categoryIdNg": 12867, "couponCode": "UAB1A8913FC0E00",
             "couponCodePlatform": "UAB1A8913FC0E00", "couponLimitType": 1, "couponPrice": "9.90",
             "couponPriceDetailsSize": 0, "dealPrice": "111.11", "giftType": 0, "isPlusPack": 0, "isSpu": 0,
             "itemId": 1000112, "itemName": " 柔肤夜用护翼卫生巾 33cm*9片多花色红色红色红色红色红色红色红色红色", "itemSalePrice": "111.11",
             "itemSize": "SINGLE", "itemType": 0, "nonPlatformCashCouponPrice": "0", "nonPlatformCouponPrice": "0",
             "parentCategoryId": 0, "payPrice": "101.21", "platformCashCouponPrice": "0", "platformCouponPrice": "9.90",
             "redbagPrice": "0", "reducePrice": "0", "seckill": 0, "shipPrice": "0", "shopId": 1192, "shopName": "蜜芽自营",
             "spuSkus": [], "spuSkusSize": 0, "supplierId": 0, "taxPrice": "0", "uniqKey": "1000112-SINGLE-0",
             "warehouseId": 40, "warehouseType": 1}], "orderItemsSize": 1, "orders": {"balancePrice": "0",
                                                                                      "cashCouponPrice": "0.00",
                                                                                      "channel": "211",
                                                                                      "ckSuperiorOrderCode": "",
                                                                                      "ckType": 112,
                                                                                      "couponPrice": "9.90",
                                                                                      "dealPrice": "111.11",
                                                                                      "orderTime": "2021-02-18 17:47:04",
                                                                                      "payPrice": "101.21",
                                                                                      "salePrice": "111.11",
                                                                                      "shipPrice": "0",
                                                                                      "subChannel": "weixinxcx_pick",
                                                                                      "taxPrice": "0",
                                                                                      "totalRedbagPrice": "0",
                                                                                      "usedRedbagPrice": "0",
                                                                                      "userId": 220111262}}}
    r = requests.post("http://127.0.0.1:8080/couponTrade/autoCheckoutMulti",
                      data={"json": json.dumps(r_data)})
    print(r.content.decode("utf-8"))


def test_zero_bmp_stock():
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
    r = requests.post("http://172.16.96.197:9999/order-stock-service-api/stockBmp/bmpDistributeStockQty",
                      data=json.dumps(r_data), headers=head)
    print(r.content.decode("utf-8"))


if __name__ == "__main__":
    test_zero_bmp_stock()
