import requests
import json


# 通用库存接口请求
def common_stock_api(b_param, api_url):
    head = {"Content-Type": "application/json; charset=UTF-8", 'Connection': 'close'}
    business_params = json.dumps(b_param)
    common_params = json.dumps(
        {
            "appVersion": "1.0",
            "clientVersion": "1.0",
            "opUser": "pop",
            "requestId": "5c53da49-e075-4d82-b9c7-52edbc0e92dc",
            "timestamp": "1604561779971"
        }
    )
    post_data = {
        "businessParams": business_params,
        "commonParams": common_params
    }
    r = requests.post(api_url, data=json.dumps(post_data), headers=head)
    print(r.content.decode("utf-8"))
