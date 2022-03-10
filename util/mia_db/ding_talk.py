import json

import requests


# 钉钉群机器人
def ding_talk():
    headers = {
        "Content-Type": "application/json"
    }
    data = {"msgtype": "text",
            "text": {
                "content": "我就是我, 是不一样的烟火"
            }
            }
    json_data = json.dumps(data)
    requests.post(
        url='https://oapi.dingtalk.com/robot/send?access_token=35fd4b08dea143f19921121f0a6282dcb014ebb11dae72114ed569c9effe8e5e',
        data=json_data, headers=headers)


def jt_talk():
    headers = {
        "apiAccount": "365045451705032732",
        "digest": "rgfMVgqkUfywNMuAsD1OMw==",
        "timestamp": "1646730735000"
    }
    data = {"billCodes": "557080502147480"
            }
    json_data = json.dumps(data)
    r = requests.post(
        url='https://openapi.jtexpress.com.cn/webopenplatformapi/api/logistics/trace',
        data=json_data, headers=headers)

    print(r.content.decode("utf-8"))


if __name__ == '__main__':
    jt_talk()
