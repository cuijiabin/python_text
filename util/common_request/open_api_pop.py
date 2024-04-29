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


# 根据日期生成消耗记录
def gen_use_record(stat_date):
    head = {
        "Content-Type": "application/json;charset=UTF-8",
        "jnpf-origin": "pc",
        "Authorization": "bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpblR5cGUiOiJsb2dpbiIsImxvZ2luSWQiOiI1NDQ3OTYxNjg5NjI1MDM4MTMiLCJyblN0ciI6IlByVXp1cm9zMUxRQm9ZWG5HVG9HcUd0VldubERCS3RCIiwidXNlcl9pZCI6IjU0NDc5NjE2ODk2MjUwMzgxMyIsInVzZXJfbmFtZSI6ImN1aWppYWJpbkRldiIsInNpbmdsZUxvZ2luIjoyLCJleHAiOjE3MTg0MTQ0NDY1MzQsInRva2VuIjoibG9naW5fdG9rZW5fNTQ5ODQ4Mjc1MzY5NDE2MTMzIn0.UTjc-_AFzwSiSeEmeXivbznCIKPGlsJZqGB1R2uAUnc"}
    post_data = {
        "tenantId": "",
        "origin": "preview",
        "paramList": [
            {
                "field": "statDate",
                "fieldName": "统计日期",
                "dataType": "varchar",
                "required": 0,
                "defaultValue": str(stat_date)
            }
        ]
    }
    r = requests.post("http://127.0.0.1:3100/dev/api/system/DataInterface/547485512055725509/Actions/Preview",
                      data=json.dumps(post_data), headers=head)
    print(r.content.decode("utf-8"))


# 获取每天的日期字符串
# 参数1：begin_date_str，开始日期字符串，例如：2020-01-01
# 参数2：end_date_str，结束日期字符串，例如：2020-08-10
def get_every_day(begin_date_str, end_date_str):
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date_str, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list


if __name__ == "__main__":
    data = get_every_day("2023-10-01", "2024-04-15")
    for d in data:
        print(d)
        gen_use_record(d)
