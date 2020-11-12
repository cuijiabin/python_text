# coding=utf-8
import requests
import json


def test_item_online():
    r_data = {"item_id": 2020037235}
    r = requests.post("http://zuobaohui_dev.ums.intra.miyabaobei.com/report/pop_item_api/sync_item_status", data=r_data)
    print(r.content.decode("utf-8"))


def test_item_stock():
    r_data = {"quantity": "700", "method": "mia.item.update.stock", "size": "75F以上", "format": "json",
              "sign": "b6ecc3071ad15dbd3257cf0ecca4241c", "sku_id": "198309957", "item_barcode": "43re45re45ef",
              "version": "1.0", "vendor_key": "test_40", "timestamp": "1555501155"}
    r = requests.post("http://127.0.0.1:8080/openapi/app", data=r_data)
    print(r.content.decode("utf-8"))


def test_local_return_orders():
    r_data = {
        "end_date": "2019-02-28",
        "method": "mia.returns.list",
        "page": "1",
        "page_size": "100",
        "sign": "9a1af2cbacd70e732a4dc9576dcd700e",
        "start_date": "2017-02-28",
        "vendor_key": "test_40",
        "timestamp": "1565170433",
        "version": "1.0"
    }
    r = requests.post("http://172.16.96.119:8090/openapi/app", data=r_data)
    print(r.content.decode("utf-8"))


def test_return_order_get():
    r_data = {"format": "json", "method": "mia.returns.get", "page": "1",
              "page_size": "100",
              "return_state": "1,2,3", "start_date": "2019-05-26 10:00:00", "end_date": "2019-05-28 10:00:00",
              "sign": "ba90f8be6ca31e44bc244a5c37b4e54f", "timestamp": "1559033954",
              "vendor_key": "1E056688-223D-8A49-D9F5-850276CA018D", "version": "1.0"}
    r = requests.post("http://10.1.52.216:8080/openapi/app", data=r_data)
    print(r.content.decode("utf-8"))


def test_return_order_get2():
    r_data = {"platformBuyerId": "220107054", "buyerVerified": "true", "expressNo": "8765432", "majorBusiness": "10004",
              "expressCo": "33", "sellerName": "直邮仓商户测试公司", "sellerVerified": "true", "buyerName": "",
              "buyerCertNo": "610481198708270541", "platformSellerId": "1291", "platformOrderId": "1909207000026325",
              "sellerCertNo": "faafsdasd", "buyerContact": "13519183586",
              "extraInfo": "{\"unitPrice\":169,\"amount\":169,\"expressSendTime\":\"20190920173058\",\"payTime\":\"20190920172749\",\"sellerAddress\":\"应用\",\"refundCount90D\":0,\"orderCount90D\":0,\"itemNum\":1,\"refundCount180D\":0,\"buyerAddress\":\"科技二路西安软件园\",\"buyerCity\":\"西安市\",\"orderTime\":\"20190920172611\",\"payAmount\":169,\"orderCount180D\":0,\"goodsInfo\":[{\"itemId\":2020037225,\"itemName\":\"法式芝士月饼 金色 54寸\",\"itemCatagoryId\":14956,\"skuId\":0,\"skuNum\":\"1\"}]}"}
    r = requests.post("http://gaokaiwei_dev.oms.intra.miyabaobei.com/api/insurance/freightinsure?action=policyAdd",
                      data=r_data)
    print(r.content.decode("utf-8"))
    print(r)


# 获取订单列表 刷新预占redis锁 使用
def get_all_stock_list():
    ll = []
    ss = [2873150]
    for s in ss:
        ll.append({
            "itemId": s,
            "warehouseIds": [],
            "isExact": 0
        })
    r_data = {"paramJSON": json.dumps(ll)}
    r = requests.post("http://10.5.107.234:7777/getStockQtyForums.sc", data=r_data)
    content = json.loads(r.content.decode("utf-8"))
    print(content["result"])


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


# 修复用户蜜豆
def repair_mi_bean_list():
    user_ids = '10281386,10280380,31755103,6793590,26955482,29402741,27151827,16117210,26942019,1133480,16117210,28433617,15759101,13890964,4512376'
    r_data = {
        "userIds": user_ids,
        "write": True
    }
    r = requests.post("http://10.5.107.217:9999/userJob/batchRepairUserLevelInfo", data=r_data)
    print(r.content.decode("utf-8"))
    print(r.status_code)


# 扣减失败返还库存数量
def tradeStockRollback_repair():
    ll = [
        {
            "itemId": 2474342,
            "optPre": 0,
            "orderCode": "2003232311592843",
            "qty": 120,
            "stockItemId": 4998839,
            "superiorOrderCode": "202003232311592843",
            "userId": 0,
            "warehouseId": 6868
        },
        {
            "itemId": 2474565,
            "optPre": 0,
            "orderCode": "2003232311592843",
            "qty": 76,
            "stockItemId": 5001407,
            "superiorOrderCode": "202003232311592843",
            "userId": 0,
            "warehouseId": 6868
        },
        {
            "itemId": 2506746,
            "optPre": 0,
            "orderCode": "2003232311592843",
            "qty": 80,
            "stockItemId": 5018890,
            "superiorOrderCode": "202003232311592843",
            "userId": 0,
            "warehouseId": 6868
        },
        {
            "itemId": 2506748,
            "optPre": 0,
            "orderCode": "2003232311592843",
            "qty": 36,
            "stockItemId": 5030235,
            "superiorOrderCode": "202003232311592843",
            "userId": 0,
            "warehouseId": 6868
        },
        {
            "itemId": 2474573,
            "optPre": 0,
            "orderCode": "2003232311592843",
            "qty": 36,
            "stockItemId": 5040792,
            "superiorOrderCode": "202003232311592843",
            "userId": 0,
            "warehouseId": 6868
        }
    ]

    r_data = {"paramJSON": json.dumps(ll)}
    r = requests.post("http://10.5.107.234:7777/tradeStockRollback.sc", data=r_data)
    print(r.content.decode("utf-8"))
    print(r)


def delay_queue():
    r_data = {
        "topic": "task_a",
        "delayTime": 1585116600,
        "ttrTime": 600,
        "message": "hello2"
    }
    r = requests.post("http://127.0.0.1:8080/push", data=r_data)
    print(r.content.decode("utf-8"))
    print(r.status_code)


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


# 批量调取接口
def batch_get(uul):
    r = requests.get(uul)
    print(r.content.decode("utf-8"))


def test_autoCheckoutMulti():
    dd = {
        "canUseChannel": 1,
        "checkedCouponCodes": [
            "YXZAA2CAB9A6F7F"
        ],
        "platform": "Normal",
        "tContent": {
            "couponsSize": 0,
            "orderItems": [
                {
                    "balancePrice": "0",
                    "batchCodePlatform": "normal-200416-fa350c13c15834ee",
                    "brandId": 1,
                    "cashCouponPrice": "33.00",
                    "categoryId": 109,
                    "categoryIdNg": 15050,
                    "couponCode": "YXZAA2CAB9A6F7F",
                    "couponCodePlatform": "YXZAA2CAB9A6F7F",
                    "couponLimitType": 1,
                    "couponPrice": "0.00",
                    "couponPriceDetails": [
                        {
                            "batchCode": "normal-200416-fa350c13c15834ee",
                            "cashCouponPrice": "33.00",
                            "couponCode": "YXZAA2CAB9A6F7F",
                            "couponPrice": "0",
                            "type": 1
                        }
                    ],
                    "dealPrice": "45.00",
                    "giftType": 0,
                    "isPlusPack": 0,
                    "isSpu": 0,
                    "itemId": 20181201,
                    "itemName": "勿改--秋季暖心毛衣",
                    "itemSalePrice": "45.00",
                    "itemSize": "SINGLE",
                    "itemType": 0,
                    "nonPlatformCashCouponPrice": "0",
                    "nonPlatformCouponPrice": "0",
                    "parentCategoryId": 0,
                    "payPrice": "12.00",
                    "platformCashCouponPrice": "33.00",
                    "platformCouponPrice": "0",
                    "redbagPrice": "0",
                    "reducePrice": "0",
                    "seckill": 0,
                    "shipPrice": "0",
                    "shopId": 16,
                    "shopName": "蜜芽精选商家",
                    "spuSkus": [

                    ],
                    "supplierId": 1291,
                    "taxPrice": "0",
                    "uniqKey": "20181201-SINGLE-0",
                    "warehouseId": 1016,
                    "warehouseType": 5
                }
            ],
            "orders": {
                "balancePrice": "0",
                "cashCouponPrice": "33.00",
                "channel": "4",
                "ckSuperiorOrderCode": "202010211593889991005158400",
                "ckType": 2,
                "couponPrice": "0.00",
                "dealPrice": "45.00",
                "orderTime": "2020-10-21 11:43:16",
                "payPrice": "12.00",
                "salePrice": "45.00",
                "shipPrice": "0",
                "subChannel": "9.5.2|",
                "taxPrice": "0",
                "totalRedbagPrice": "0",
                "usedRedbagPrice": "0",
                "userId": 159388999
            }
        }
    }
    r_data = {
        "json": json.dumps(dd)
    }
    r = requests.post("http://127.0.0.1:8080/couponTrade/autoCheckoutMulti.sc", data=r_data)
    print(r.content.decode("utf-8"))


def test_useCoupon():
    dd = {
        "opUser": "order_transfer",
        "platform": "Normal",
        "uid": 159388999,
        "useRecords": [
            {
                "ckSuperiorOrderCode": "",
                "couponCode": "YXZAA2CAB9A6F7F",
                "orderCode": "",
                "superiorOrderCode": "202010219000026400"
            }
        ]
    }
    r_data = {
        "json": json.dumps(dd)
    }
    r = requests.post("http://127.0.0.1:8080/couponTrade/useCoupon.sc", data=r_data)
    print(r.content.decode("utf-8"))


def test_preUseCoupon():
    dd = {
        "ckSuperiorOrderCode": "202010211593889991005158400",
        "couponCodes": [
            "YXZAA2CAB9A6F7F"
        ],
        "opUser": "order",
        "platform": "Normal",
        "uid": 159388999
    }
    r_data = {
        "json": json.dumps(dd)
    }
    r = requests.post("http://127.0.0.1:8080/couponTrade/preUseCoupon.sc", data=r_data)
    print(r.content.decode("utf-8"))


def test_preUseCoupon_remote():
    dd = {
        "ckSuperiorOrderCode": "202010211593889991005158400",
        "couponCodes": [
            "YXZAA2CAB9A6F7F"
        ],
        "opUser": "order",
        "platform": "Normal",
        "uid": 159388999
    }
    r_data = {
        "json": json.dumps(dd)
    }
    r = requests.post("http://127.0.0.1:8889/coupon/preUseCoupon.sc", data=r_data)
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


def test_get_bmp_demo():
    r_data = {"msg": "xxxxxxxxxxxxxxxxxx"}
    r = requests.post("http://127.0.0.1:9089/stockTrade/sayHello", data=r_data)
    print(r.content.decode("utf-8"))


if __name__ == "__main__":
    # test_useCoupon()
    ll = ['http://10.5.105.104:9089/stock/resetStockPreQty?itemId=2991889&warehouseId=3364']
    for m in ll:
        batch_get(m)
    # test_get_bmp_demo()
    # test_preUseCoupon()
    # test_autoCheckoutMulti()
