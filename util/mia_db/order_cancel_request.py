import requests

# 订单强制取消
if __name__ == '__main__':
    order_list = [
    ]
    for o in order_list:
        post_data = {
            "orderCode": str(o[0]),
            "userId": o[1],
            "forceCancelType": 1,
            "operatorId": 10000,
            "remark": "与其他达人预售湿巾订单重合取消"
        }

        r = requests.post("http://10.5.107.177:8082/order/forceCancelSubOrder.sc", data=post_data)
        print(str(o[0]), r.content.decode("utf-8"))
