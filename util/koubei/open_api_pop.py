# coding=utf-8
import requests
import json


def test_orders_search():
    r_data = {"sign": "d4100a989bacf9bb5080b2edd88f0d11", "timestamp": "1553139791", "page_size": "1",
              "end_date": "2019-03-21 11:08:18", "vendor_key": "FE6C5185-0AB2-8D63-2A56-4CC3D236816E", "page": "1",
              "order_state": "2", "method": "mia.orders.search", "format": "json", "start_date": "2019-03-20 11:08:16",
              "version": "1.0"}
    r = requests.post("http://10.1.52.216:8080/openapi/app", data=r_data)
    print(r.content.decode("utf-8"))


def test_local_orders_search():
    r_data = {"end_date": "2019-02-05 21:58:54", "method": "mia.orders.search", "order_state": "1,2,3,4,5,6",
              "page": "1", "page_size": "50", "start_date": "2019-01-11 21:58:54",
              "sign": "72827353273082481cd00351ec1a7a33",
              "vendor_key": "3084DBCE-AC0F-8681-F9B3-4E45C35FA68C", "timestamp": "1552565070"}
    r = requests.post("http://127.0.0.1:8080/openapi/app", data=r_data)
    print(r.content.decode("utf-8"))


def test_local_orders_get():
    r_data = {
        "format": "json",
        "method": "mia.order.get",
        "order_id": "1901286216431212",
        "sign": "e97486ea0b141585204f5561203c0347",
        "timestamp": "1556184918",
        "vendor_key": "3084DBCE-AC0F-8681-F9B3-4E45C35FA68C",
        "version": "1.0"
    }
    r = requests.post("http://127.0.0.1:8080/openapi/app", data=r_data)
    print(r.content.decode("utf-8"))


def test_local_orders_confirm():
    r_data = {"method": "mia.order.get.identification", "order_id": "1902211810610281",
              "sign": "f7f80597c92f16d82d512da8685db3b9", "timestamp": "1552029591",
              "vendor_key": "1F9492FF-BF76-1599-F02E-FFB9FE29B215"}
    r = requests.post("http://127.0.0.1:8080/openapi/app", data=r_data)
    print(r.content.decode("utf-8"))


def test_local_order_deliver():
    r_data = {"method": "mia.new.order.deliver",
              "sheet_code_info": "[{\"logistics_id\":22,\"sheet_code\":\"3701554255553\"}]",
              "order_id": "1902256216433964",
              "sign": "cdffed690b228aea7cb1015ea226dd8f", "timestamp": "1552562045",
              "vendor_key": "3084DBCE-AC0F-8681-F9B3-4E45C35FA68C"}
    r = requests.post("http://127.0.0.1:8080/openapi/app", data=r_data)
    print(r.content.decode("utf-8"))


def test_api_order_get():
    r_data = {"format": "json", "method": "mia.order.get", "order_id": "1903111841552132",
              "sign": "2f6f8661f4c191f6ad850396fc3c29e3", "timestamp": "1552291441",
              "vendor_key": "9F3BBCBF-00C8-167A-47A8-E1B3E07A2C07", "version": "1.0"}
    r = requests.post("http://10.1.52.216:8080/openapi/app", data=r_data)
    print(r.content.decode("utf-8"))


# 保存运费规则
def test_freight_rule_save():
    r_data = {"ruleName": "海鲜加收百元", "categoryIdNg": 1445, "type": 1}
    r = requests.post("http://127.0.0.1:8090/freight/saveRule.ajax", data=r_data, cookies=cookies)
    print(r.content.decode("utf-8"))


# 保存运费规则
def test_freight_rule_saveii():
    r_data = {"end_date": "2019-03-13 09:00:00", "method": "mia.orders.search", "order_state": "2,4,5,6", "page": "6",
              "page_size": "100", "sign": "19804e4f4653625e4aecb648b3896d2b", "start_date": "2019-03-10 09:00:00",
              "timestamp": "1552446671", "vendor_key": "981C9124-C5D9-5AB6-230E-0111AAE07F54"}
    r = requests.post("http://10.1.50.76:8080/openapi/app", data=r_data)
    print(r.content.decode("utf-8"))


def test_local_item_search():
    r_data = {"method": "mia.item.list",
              "page": "1", "page_size": "50",
              "sign": "f1e0e2362e9397691c05afc092ad477a",
              "vendor_key": "3084DBCE-AC0F-8681-F9B3-4E45C35FA68C", "timestamp": "1553852910"}
    r = requests.post("http://127.0.0.1:8080/openapi/app", data=r_data)
    print(r.content.decode("utf-8"))


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


if __name__ == "__main__":
    # test_freight_rule_saveii()
    test_local_return_orders()
