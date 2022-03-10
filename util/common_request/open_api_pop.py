# coding=utf-8
import datetime
import json
import time

import requests


# 根据子订单号解密订单
def common_order_decrypt(order_code):
    post_data = {
        "order_code": str(order_code)
    }
    r = requests.post("http://ums.intra.miyabaobei.com/server_api/order_api/getThirdOrderDecryptData", data=post_data)
    print(r.content.decode("utf-8"))


# 抖音订单解密
def decrypt_third_order(third_order_code):
    head = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Third-Token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJqd3RfYWRtaW4iLCJzdWIiOiJ1bXMifQ.NqYPhBsMWuoq8BZzOI7cF_QWXhBhTteJm0lUYeTePic"}
    post_data = {
        "third_order_code": str(third_order_code),
        "decrypt_field": [
            "phone", "name", "address"
        ]
    }
    r = requests.post("http://third-trade-api.miaidc.com/api/Tiktok_orders/tiktok_order_decrypt",
                      data=json.dumps(post_data), headers=head)
    print(r.content.decode("utf-8"))


def test_time_diff():
    begin_time = datetime.datetime.now()
    time.sleep(10)
    time_diff = (datetime.datetime.now() - begin_time).microseconds
    print(time_diff)


if __name__ == "__main__":
    order_code_list = []
    for order_code in order_code_list:
        common_order_decrypt(order_code)
