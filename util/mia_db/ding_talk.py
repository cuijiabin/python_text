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


if __name__ == '__main__':
    ding_talk()
