import requests

# 订单转仓相关文件
if __name__ == '__main__':
    order_list = [
        2203072489772363
    ]
    for order_code in order_list:
        post_data = {
            "orderCode": str(order_code),
            "targetWarehouseId": 9769,
            # "remark": "兔头品牌订单西安仓撤仓"
            "confirmTime": "2022-03-08 16:30:00",
        }

        r = requests.post("http://10.5.107.177:8082/order/changeOrderWarehouse.sc", data=post_data)
        print(str(order_code), r.content.decode("utf-8"))
