import requests


def re_send_mq(mq):
    r = requests.post("http://10.5.105.104:9089/stock/reSendMq", data=mq)

    print(r.content.decode("utf-8"))


if __name__ == '__main__':
    # ums_mq = {
    #     "stockItemId": 7572775,
    #     "itemId": 5288383,
    #     "warehouseId": 1319,
    #     "qty": -2,
    #     "userId": 9999,
    #     "stockType": 1,
    #     "timeStamp": 1557676800000,
    #     "opType": 9,
    #     "isTest": False
    # }

    api_mq = {
        "stockItemId": 4094746,
        "itemId": 1681779,
        "warehouseId": 3364,
        "qty": -8,
        "userId": 41074930,
        "stockType": 0,
        "timeStamp": 1557676800000,
        "opType": 10,
        "isTest": False,
        "orderCode": "2001082279774212",
        "superiorOrderCode": "202001082279773652",
        "isOperatePreQty": True
    }

    re_send_mq(api_mq)
