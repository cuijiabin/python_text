import requests

# 订单转仓相关文件
if __name__ == '__main__':
    order_list = []
    for order_code in order_list:
        post_data = {
            "orderCode": str(order_code),
            # "targetWarehouseId": 6868,
            "confirmTime": "2021-10-21 14:00:00",
        }

        r = requests.post("http://10.5.107.177:8082/order/changeOrderWarehouse.sc", data=post_data)
        print(str(order_code), r.content.decode("utf-8"))
