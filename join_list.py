# coding=utf-8
import json


def exchagne(a, b):
    print(a, b)
    b, a = a, b
    print(a, b)


def deppp():
    with open("E:/file/download/paidCancelOrder.log", encoding="utf8") as f:
        line = f.readline()
        while line:
            line = line.strip('\n')
            p = json.loads(line)
            print(p["attrs"]["superior_order_code"])
            line = f.readline()
        f.close()


deppp()
