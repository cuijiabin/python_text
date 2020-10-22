# coding=utf-8
import requests
import json


def test_open_order_create():
    params = {
        "thirdOrderCode": "342343453423242",
        "isUseThirdOrderCode": 0,
        "userId": 220110439,
        "operatorId": 0,
        "dstAddress": "国际港务区",
        "dstName": "课##",
        "dstMobile": "17629040836",
        "channel": 1,
        "openChannel": "1",
        "payMode": 1,
        "dstMode": 1,
        "isMinusStock": 1,
        "totalPayPrice": 430,
        "totalReducePrice": 0,
        "reducePriceType": 0,
        "totalShipPrice": 30,
        "totalTaxPrice": 0,
        "ip": "127.0.0.0",
        "warehouseId": "",
        "isZeroOrder": 0,
        "transactionId": "S20200817173832586",
        "payTime": "2020-08-17 17:38:32",
        "orderTime": "2020-08-17 17:36:26",
        "isLockOrder": 0,
        "storeCode": "",
        "dstTel": "",
        "pushOrder": 0,
        "dstProvince": "陕西省",
        "dstCity": "西安市",
        "dstArea": "灞桥区",
        "dstStreet": "",
        "orderItemBoList": [
            {
                "itemId": 1001152,
                "itemSize": "SINGLE",
                "quantity": 2,
                "itemSalePrice": 100
            },
            {
                "itemId": 1002035,
                "itemSize": "SINGLE",
                "quantity": 1,
                "itemSalePrice": 200
            }
        ]
    }

    r_data = {"paramJSON": json.dumps(params)}
    r = requests.post("http://127.0.0.1:8080/openOrderCreate", data=r_data)
    print(r.content.decode("utf-8"))


def test_cancel_order():
    params = {
        "orderCode": "2008118000000073",
        "userId": 1508764,
        "operatorId": 9999,
    }

    r_data = {"paramJSON": json.dumps(params)}
    r = requests.post("http://127.0.0.1:8080/cancelOrder", data=r_data)
    print(r.content.decode("utf-8"))


def test_cancel_third_order():
    r_data = {}
    r = requests.post("http://service.api.miyabaobei.com/tik_tok/tik_tok_open/agreeRefundTikTokOrders/202009252383089543", data=r_data)
    print(r.content.decode("utf-8"))


if __name__ == "__main__":
    test_cancel_third_order()
    # test_open_order_create()
