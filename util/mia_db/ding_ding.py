# coding=utf-8
# 利用 azkaban 调度监控 iyuansong 各个作业的执行情况
# 通过钉钉发送警告信息
import base64
import hashlib
import hmac
import json
import time
from datetime import date
from flask import Flask
import urllib

import requests
from numpy import long


def push_dingding(msg):
    # atMobiles
    p_s = {
        # '郭毅': '18101331762',
        # '刘浩东': '18392889968',
        # '梁自强': '18792694605',
        '崔佳彬': '18910358924'
    }
    warn_at = {
        1: [p_s['崔佳彬']],
        2: [p_s['崔佳彬']],
        3: [p_s['崔佳彬']],
        4: [p_s['崔佳彬']],
        5: [p_s['崔佳彬']],
        6: [p_s['崔佳彬']],
        7: [p_s['崔佳彬']]
    }
    atMobiles = warn_at[date.today().isoweekday()]
    #
    server = 'https://oapi.dingtalk.com/robot/send?access_token=a70d50c1ea55c372a60b0c4227f3c7aa4aa6b41e24e96c10c44efcc90bfc74a8'
    # 时间戳
    timestamp = long(round(time.time() * 1000))
    # 密钥
    secret = 'SEC3b2ef9cdfe925d27395c14096c46605d564939a585558070e0e2a116f601cf4e'
    # 密钥 utf-8 编码
    secret_enc = bytes(secret, encoding='utf-8')
    # 签名拼接
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    # 拼接后 utf-8 编码
    string_to_sign_enc = bytes(string_to_sign, encoding='utf-8')
    # HmacSHA256算法计算签名
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    # 先 Base64 encode ,再 url encode
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    url = "%s&timestamp=%s&sign=%s" % (server, timestamp, sign);
    sendMsg = {
        "msgtype": "text",
        "text": {"content": "iyaunsong 监控:\n" + msg},
        "at": {"atMobiles": atMobiles, "isAtAll": 0}
    }
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(sendMsg), headers=headers)


if __name__ == '__main__':
    push_dingding("钉钉消息测试")
